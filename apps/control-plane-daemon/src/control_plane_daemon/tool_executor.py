import argparse
import json
import os
import subprocess
import sys
from typing import Any, cast

from agent_infra.system_logger import SystemLogger
from dotenv import load_dotenv
from litellm import completion

from .execution_context import ExecutionContext
from .models import Policy
from .registry import ToolRegistry
from .system_watchdog import SystemWatchdog
from .vector_search_tool import VectorSearchTool

SETTINGS_PATH = os.path.expanduser("~/.qwen/settings.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTE_SCRIPT = os.path.join(SCRIPT_DIR, "model_router.py")
STACK_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

# Load environment variables from ~/.qwen/.env
load_dotenv(os.path.expanduser("~/.qwen/.env"))

# Initialize the Tool Registry
registry = ToolRegistry()

# --- Resilience Configuration ---
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds
TIMEOUT_CONFIG = {
    "high": 300,  # 5 mins for 480B models
    "mid": 120,  # 2 mins for 120B models
    "low": 60,  # 1 min for 7B models
}
FALLBACK_MODELS = {
    "qwen/qwen3-coder-480b-a35b-instruct:free": "openai/gpt-oss-120b:free",
    "openai/gpt-oss-120b:free": "nvidia/deepseek-ai/deepseek-v4-pro",
}


def load_settings() -> dict[str, Any]:
    try:
        with open(SETTINGS_PATH) as f:
            return cast(dict[str, Any], json.load(f))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error loading settings: {e}")
        sys.exit(1)


def get_route(prompt: str) -> dict[str, Any]:
    if not os.path.exists(ROUTE_SCRIPT):
        print(f"Routing Error: Route script not found at {ROUTE_SCRIPT}")
        sys.exit(1)

    result = subprocess.run(
        ["python3", ROUTE_SCRIPT, "--prompt", prompt], capture_output=True, text=True
    )

    if result.returncode != 0:
        print(
            f"Routing Error: model_router.py failed with exit code {result.returncode}. "
            f"Stderr: {result.stderr}"
        )
        sys.exit(1)

    try:
        return cast(dict[str, Any], json.loads(result.stdout))
    except json.JSONDecodeError:
        print(f"Routing Error: Could not parse JSON from model_router.py. Stdout: {result.stdout}")
        sys.exit(1)


def call_model(
    model_id: str,
    prompt: str,
    settings: dict[str, Any],
    skill_config: dict[str, Any] | None = None,
    state_manager_inst: Any | None = None,
    history: list[dict[str, str]] | None = None,
) -> str:
    logger = SystemLogger()

    # --- DYNAMIC PROMPT RESOLUTION ---
    sys_prompt = ""
    if skill_config and "system_prompt" in skill_config:
        sys_prompt = skill_config["system_prompt"]
    else:
        agent_name = "general-purpose"
        for persona in [
            "architect",
            "developer",
            "researcher",
            "reviewer",
            "security-auditor",
            "troubleshooter",
        ]:
            if persona in model_id.lower():
                agent_name = persona
                break

        # FIX: Use config/agents/{agent_name}/persona.md
        prompt_path = os.path.join(STACK_ROOT, "config", "agents", agent_name.upper(), "persona.md")
        if os.path.exists(prompt_path):
            with open(prompt_path) as f:
                sys_prompt = f.read()

    if state_manager_inst and sys_prompt:
        # JobStateManager wraps StateManager in self.sm
        sm = state_manager_inst.sm if hasattr(state_manager_inst, "sm") else state_manager_inst
        phase = sm.get("active_phase", "UNKNOWN")
        todos = sm.get("todo_list", [])
        todo_str = "\\n".join([f"- [{t['status']}] {t['content']}" for t in todos])
        state_context = f"\\n\\n# STATE\\n- **Phase**: {phase}\\n- **Todos**:\\n{todo_str}"
        sys_prompt += state_context

    def resolve_model_config(mid: str) -> tuple[str, str, str]:
        """Helper to find provider group, baseUrl, and envKey from settings.json"""
        for group, models in settings.get("modelProviders", {}).items():
            for m in models:
                if m["id"] == mid:
                    return (
                        group,
                        m.get("baseUrl", ""),
                        m.get("envKey", "OPENAI_API_KEY"),
                    )
        return "openai", "", "OPENAI_API_KEY"

    group, api_base, env_key = resolve_model_config(model_id)
    current_model = f"{group}/{model_id}"

    timeout = TIMEOUT_CONFIG["low"]
    if "480b" in model_id.lower():
        timeout = TIMEOUT_CONFIG["high"]
    elif "120b" in model_id.lower():
        timeout = TIMEOUT_CONFIG["mid"]

    try:
        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})

        if history:
            messages.extend(history)
        else:
            messages.append({"role": "user", "content": prompt})

        # Explicitly pass the API key from the environment based on settings.json
        api_key = os.environ.get(env_key)

        response = completion(
            model=current_model,
            messages=messages,
            temperature=0.2,
            timeout=timeout,
            api_base=api_base,
            api_key=api_key,
        )
        content = response.choices[0].message.content
        if content is None:
            logger.warn("model_returned_none", {"model": current_model})
            return "Error: Model returned empty response."

        logger.info(
            "model_response",
            {"model": current_model, "attempt": 1, "status": "success"},
        )
        return cast(str, content)
    except (RuntimeError, ValueError) as e:
        logger.error("model_failure", {"model": current_model, "attempt": 1, "error": str(e)})
        return f"Fatal API Error: {e}"


async def call_memory_server(method: str, args: dict[str, Any]) -> Any:
    """
    Calls the Memory Daemon via the Unix Domain Socket.
    """
    from .mcp_manager import MCPManager

    socket_path = os.path.join(
        os.path.expanduser("~"), ".local/share/megalonyx/sockets/megalonyx_memory.sock"
    )

    mgr = MCPManager()
    mgr.register_server("memory", socket_path=socket_path)
    try:
        return await mgr.call_tool(server_name="memory", tool_name=method, arguments=args)
    except (OSError, RuntimeError) as e:
        return {"error": f"Memory server call failed: {str(e)}"}


async def execute_tool(
    tool_name: str,
    args: dict[str, Any],
    search_tool: Any,
    current_policy: dict[str, Any] | None = None,
    context: ExecutionContext | None = None,
    state_manager_inst: Any | None = None,
) -> Any:
    """Executes a specialized tool and returns the result.
    Enforces boundaries defined in the current_policy.
    """
    logger = SystemLogger()
    print(f"  [TOOL: {tool_name}] Executing with args: {args}...")

    # Ensure context is never None
    exec_context = context or ExecutionContext()

    # Convert policy dict to Policy model for type safety
    policy_model = (
        Policy(**current_policy)
        if current_policy
        else Policy(allowed_tools=[], allowed_paths=[], can_write=False)
    )

    # --- POLICY ENFORCEMENT ---
    if current_policy:
        # 1. Tool Permission Check
        if tool_name not in policy_model.allowed_tools:
            logger.warn(
                "policy_violation",
                {
                    "tool": tool_name,
                    "reason": "Tool not allowed by current intent policy",
                },
            )
            return {
                "error": f"Policy Violation: Tool '{tool_name}' is not permitted for this intent."
            }

        # 2. Write Permission Check
        if not policy_model.can_write and tool_name in [
            "write_file",
            "edit",
        ]:
            logger.warn(
                "policy_violation",
                {"tool": tool_name, "reason": "Write access denied by policy"},
            )
            return {"error": "Policy Violation: Write access is denied for this intent."}

    logger.info("tool_call", {"tool": tool_name, "args": args})

    try:
        # Dispatch to the registered handler
        handler = registry.get_handler(tool_name)

        # We wrap the result in a ToolResponse to maintain backward compatibility
        # with the existing execute_tool return types (which are mixed Any/dict)
        # The handlers already return ToolResponse.
        response = await handler.execute(
            tool_name=tool_name,
            args=args,
            context=exec_context,
            policy=policy_model,
            search_tool=search_tool,
            state_manager=state_manager_inst,
        )

        # For now, return the content to avoid breaking callers expecting the raw result
        return response.content if response.success else {"error": response.error}

    except (OSError, RuntimeError, ValueError) as e:
        logger.exception("tool_failure", {"tool": tool_name, "error": str(e)})
        return {"error": f"Tool {tool_name} failed: {e}"}


def strip_orphaned_user_entries(history: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Surgically removes 'orphaned' user entries from history.
    An entry is orphaned if it is a user message that simply notifies the agent
    of a failure (e.g., 'No, you failed. Fix it.'), and is immediately followed
    by a more detailed failure log or correction prompt.
    """
    if not history:
        return []

    cleaned_history = []
    for i in range(len(history)):
        msg = history[i]
        if msg["role"] == "user":
            # Check if this is a failure notification
            content = msg["content"].lower()
            is_failure_note = any(
                phrase in content for phrase in ["you failed", "incorrect", "fix it", "not correct"]
            )

            # If it's a failure note, check if the next message is a more detailed log
            if is_failure_note and i + 1 < len(history):
                next_msg = history[i + 1]
                if (
                    next_msg["role"] == "user"
                    and "verification failure logs" in next_msg["content"].lower()
                ):
                    # Skip this orphaned entry
                    continue

        cleaned_history.append(msg)

    return cleaned_history


async def run_job_execution(
    job: dict[str, Any],
    prompt: str,
    skill_config: dict[str, Any] | None,
    model_id: str,
    settings: dict[str, Any],
    state_manager_inst: Any,
    search_tool: Any,
    policy_engine_inst: Any,
    intent_name: str,
    context: ExecutionContext,
    history: list[dict[str, str]] | None = None,
) -> str:
    """Helper to execute a job and handle tool calls with isolated context and surgical history."""
    # Resolve granular policy for this specific agent and intent
    current_policy = policy_engine_inst.get_permissions(
        intent=intent_name, agent_name=job["assigned_skill"]
    )

    # Apply Surgical History Pruning
    if history:
        history = strip_orphaned_user_entries(history)

    response = call_model(
        model_id,
        prompt,
        settings,
        skill_config=skill_config,
        state_manager_inst=state_manager_inst,
        history=history,
    )

    # Handle tool calls within the job
    import re

    tool_call_match = re.search(
        r'\{"tool":\s*"([^"]+)",\s*"args":\s*(\{.*?\})\}', response, re.DOTALL
    )
    if tool_call_match:
        tool_name = tool_call_match.group(1)
        try:
            tool_args = json.loads(tool_call_match.group(2))
            result = await execute_tool(
                tool_name,
                tool_args,
                search_tool,
                current_policy=current_policy,
                context=context,
                state_manager_inst=state_manager_inst,
            )
            response += f"\\n\\nTool Result ({tool_name}): {result}"
        except (RuntimeError, ValueError, OSError) as e:
            response += f"\\n\\nTool Error: {e}"
    return response


def main() -> None:
    from .control_plane import ControlPlane

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", help="Override the routed model (e.g., 'inherit')")
    args = parser.parse_args()

    settings = load_settings()
    control_plane = ControlPlane()
    search_tool_inst = VectorSearchTool()
    # Watchdog monitors the JobStateManager within the Control Plane
    _watchdog = SystemWatchdog(control_plane.jsm)
    logger = SystemLogger()

    # Initialize the Control Plane with the user prompt
    control_plane.process_intent(args.prompt)

    # Force the use of the global main model from settings.json
    model_id = settings.get("model", {}).get("name")
    if not model_id:
        print("Error: No global main model defined in settings.json")
        sys.exit(1)

    logger.info(
        "control_plane_activation",
        {
            "model": model_id,
            "job_count": len(control_plane.jsm.sm.get("active_job_set", {}).get("jobs", {})),
        },
    )

    # --- STRATEGIC EXECUTION LOOP ---
    root_context = ExecutionContext()

    import asyncio

    try:
        final_response: str = asyncio.run(
            control_plane.execute(
                prompt=args.prompt,
                model_id=model_id,
                settings=settings,
                search_tool=search_tool_inst,
                root_context=root_context,
            )
        )
        print(final_response)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
