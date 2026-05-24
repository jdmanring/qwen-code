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
from .system_watchdog import SystemWatchdog
from .vector_search_tool import VectorSearchTool

SETTINGS_PATH = os.path.expanduser("~/.qwen/settings.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTE_SCRIPT = os.path.join(SCRIPT_DIR, "model_router.py")
STACK_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

# Load environment variables from ~/.qwen/.env
load_dotenv(os.path.expanduser("~/.qwen/.env"))

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


def call_memory_server(method: str, args: dict[str, Any]) -> Any:
    """
    Calls the Memory Daemon via the Unix Domain Socket.
    """
    import asyncio

    from .mcp_manager import MCPManager

    socket_path = os.path.join(
        os.path.expanduser("~"), ".local/share/megalonyx/tmp/megalonyx_memory.sock"
    )

    async def _call() -> Any:
        mgr = MCPManager()
        mgr.register_server("memory", socket_path=socket_path)
        return await mgr.call_tool(server_name="memory", tool_name=method, arguments=args)

    try:
        return asyncio.run(_call())
    except (OSError, RuntimeError) as e:
        return {"error": f"Memory server call failed: {str(e)}"}


def execute_tool(
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

    # --- POLICY ENFORCEMENT ---
    if current_policy:
        # 1. Tool Permission Check
        if tool_name not in current_policy.get("allowed_tools", []):
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
        if not current_policy.get("can_write", False) and tool_name in [
            "write_file",
            "edit",
        ]:
            logger.warn(
                "policy_violation",
                {"tool": tool_name, "reason": "Write access denied by policy"},
            )
            return {"error": "Policy Violation: Write access is denied for this intent."}

    logger.info("tool_call", {"tool": tool_name, "args": args})

    def resolve_path(path: str | None) -> str | None:
        if not path:
            return None
        if os.path.isabs(path):
            return path
        return os.path.join(STACK_ROOT, path)

    try:
        if tool_name == "read_file":
            file_path = resolve_path(args.get("file_path"))
            if not file_path or not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            # --- CACHE LOOKUP ---
            if context:
                cached_content = context.file_cache.get(file_path)
                if cached_content:
                    logger.info("cache_hit", {"path": file_path})
                    return cached_content

            # Path Boundary Check
            if current_policy and "allowed_paths" in current_policy:
                allowed = current_policy["allowed_paths"]
                if "*" not in allowed and not any(
                    file_path.endswith(p.replace("**", "")) for p in allowed
                ):
                    return {"error": f"Policy Violation: Access to {file_path} is not permitted."}

            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # --- CACHE UPDATE ---
            if context:
                context.file_cache.set(file_path, content)

            return content

        if tool_name == "write_file":
            file_path = resolve_path(args.get("file_path"))
            content_val = args.get("content")
            if not file_path or not isinstance(content_val, str):
                return {"error": "Missing file_path or content (must be string) for write_file"}
            final_content: str = content_val

            # Path Boundary Check
            if current_policy and "allowed_paths" in current_policy:
                allowed = current_policy["allowed_paths"]
                if "*" not in allowed and not any(
                    file_path.endswith(p.replace("**", "")) for p in allowed
                ):
                    return {
                        "error": f"Policy Violation: Write access to {file_path} is not permitted."
                    }

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            # --- CACHE INVALIDATION ---
            if context:
                # We don't need to explicitly invalidate since FileReadCache checks mtime,
                # but we could clear it if we wanted to be aggressive.
                pass

            return f"Successfully wrote to {file_path}"

        if tool_name == "grep_search":
            pattern = args.get("pattern")
            path = resolve_path(args.get("path", "."))
            if not pattern or not path:
                return {"error": "Missing pattern or path for grep_search"}

            result = subprocess.run(
                ["rg", pattern, path], capture_output=True, text=True, encoding="utf-8"
            )
            return (
                result.stdout
                if result.returncode == 0
                else f"No matches found or error: {result.stderr}"
            )

        if tool_name == "semantic_search":
            query = args.get("query", "")
            limit = args.get("limit", 5)
            result = search_tool.semantic_search(query, limit)
            return result

        if tool_name == "memory_ingest":
            text = args.get("text")
            tier = args.get("tier", "auto")
            if not text:
                return {"error": "Missing 'text' argument for memory_ingest"}
            return call_memory_server("ingest", {"text": text, "tier": tier})

        if tool_name == "memory_search":
            query = args.get("query")
            tier = args.get("tier", "auto")
            if not query:
                return {"error": "Missing 'query' argument for memory_search"}
            return call_memory_server("search", {"query": query, "tier": tier})

        if tool_name == "memory_reflect":
            query = args.get("query")
            if not query:
                return {"error": "Missing 'query' argument for memory_reflect"}
            return call_memory_server("reflect", {"query": query})

        if tool_name == "create_agent":
            import asyncio

            from .agent_generator import AgentGenerator

            description = args.get("description")
            if not description:
                return {"error": "Missing 'description' argument for create_agent"}

            _agent_settings = load_settings()

            async def run_gen() -> Any:
                gen_service = AgentGenerator(_agent_settings)
                return await gen_service.generate(description)

            try:
                # In a real production app, we'd handle the event loop more gracefully.
                agent_data = asyncio.run(run_gen())
                return {"status": "success", "agent_data": agent_data}
            except (RuntimeError, ValueError) as e:
                return {"error": f"Agent generation failed: {str(e)}"}

        if tool_name == "archive_knowledge":
            key = args.get("key")
            if not key:
                return {"error": "Missing 'key' argument for archive_knowledge"}
            if not state_manager_inst:
                return {"error": "StateManager instance not available for archive_knowledge"}

            success = state_manager_inst.archive_item(key)
            if success:
                return {
                    "status": "success",
                    "message": f"Context for '{key}' archived successfully.",
                }
            else:
                return {"error": f"Key '{key}' not found in rag_context."}
        if tool_name in ["cron_create", "cron_delete", "cron_list"]:
            from agent_infra.cron_manager import CronManager

            cm = CronManager()
            try:
                if tool_name == "cron_create":
                    return cm.add_job(args["schedule"], args["command"], args["description"])
                elif tool_name == "cron_delete":
                    return cm.delete_job(args["description_part"])
                elif tool_name == "cron_list":
                    return cm.list_jobs()
            except (OSError, ValueError) as e:
                return {"error": str(e)}

        if tool_name in ["mcp_call_tool", "mcp_list_tools", "mcp_read_resource"]:
            import asyncio

            from .mcp_manager import MCPManager

            async def run_mcp_op() -> Any:
                mgr = MCPManager()
                server_name = args.get("server_name")
                if not server_name:
                    raise ValueError("Missing 'server_name' argument")

                # For the prototype, we'll assume a default command if not provided.
                command = args.get(
                    "command", ["npx", "-y", "@modelcontextprotocol/server-everything"]
                )
                mgr.register_server(server_name, command=command)

                if tool_name == "mcp_list_tools":
                    return await mgr.list_tools(server_name)
                elif tool_name == "mcp_call_tool":
                    return await mgr.call_tool(
                        server_name, args["tool_name"], args.get("arguments", {})
                    )
                elif tool_name == "mcp_read_resource":
                    return await mgr.read_resource(server_name, args["uri"])
                return None

            try:
                return asyncio.run(run_mcp_op())
            except (OSError, RuntimeError, ValueError) as e:
                return {"error": f"MCP operation failed: {str(e)}"}

        if tool_name in [
            "lsp_get_definitions",
            "lsp_get_references",
            "lsp_get_diagnostics",
            "lsp_hover",
        ]:
            import asyncio

            from .lsp_manager import LSPManager

            async def run_lsp_op() -> Any:
                mgr = LSPManager()
                file_path = args.get("file_path")
                if not file_path:
                    raise ValueError("Missing 'file_path' argument")

                if tool_name == "lsp_get_definitions":
                    symbol = args.get("symbol")
                    if not symbol:
                        raise ValueError("Missing 'symbol' argument")
                    return await mgr.get_definition(file_path, symbol)
                elif tool_name == "lsp_get_references":
                    symbol = args.get("symbol")
                    if not symbol:
                        raise ValueError("Missing 'symbol' argument")
                    return await mgr.get_references(file_path, symbol)
                elif tool_name == "lsp_get_diagnostics":
                    return await mgr.get_diagnostics(file_path)
                elif tool_name == "lsp_hover":
                    line = args.get("line")
                    column = args.get("column")
                    if line is None or column is None:
                        raise ValueError("Missing 'line' or 'column' argument")
                    return await mgr.hover(file_path, line, column)
                return None

            try:
                return asyncio.run(run_lsp_op())
            except (OSError, RuntimeError, ValueError) as e:
                return {"error": f"LSP operation failed: {str(e)}"}

        if tool_name in [
            "git_worktree_list",
            "git_worktree_add",
            "git_worktree_remove",
            "git_worktree_prune",
        ]:
            import asyncio

            from agent_infra.git_worktree_manager import GitWorktreeManager

            async def run_git_op() -> Any:
                mgr = GitWorktreeManager(STACK_ROOT)
                if tool_name == "git_worktree_list":
                    return await mgr.list_worktrees()
                elif tool_name == "git_worktree_add":
                    return await mgr.add_worktree(args["branch"], args["path"])
                elif tool_name == "git_worktree_remove":
                    return await mgr.remove_worktree(args["path"])
                elif tool_name == "git_worktree_prune":
                    return await mgr.prune_worktrees()
                return None

            try:
                return asyncio.run(run_git_op())
            except (OSError, RuntimeError) as e:
                return {"error": f"Git-worktree operation failed: {str(e)}"}

        if tool_name == "run-pytest":
            test_path = resolve_path(args.get("path", "tests"))
            if not test_path:
                return {"error": "Could not resolve test path"}
            result = subprocess.run(
                ["pytest", test_path], capture_output=True, text=True, encoding="utf-8"
            )
            return (
                result.stdout
                if result.returncode == 0
                else f"Tests failed:\n{result.stdout}\n{result.stderr}"
            )

        if tool_name == "run-mypy":
            target_path = resolve_path(args.get("path", "."))
            if not target_path:
                return {"error": "Could not resolve target path"}
            result = subprocess.run(
                ["mypy", target_path], capture_output=True, text=True, encoding="utf-8"
            )
            return (
                result.stdout if result.returncode == 0 else f"Type errors found:\n{result.stdout}"
            )

        if tool_name == "git-commit-atomic":
            message = args.get("message", "Atomic commit")
            file_path = resolve_path(args.get("file_path"))
            if not file_path:
                return {"error": "Missing 'file_path' for git-commit-atomic"}

            try:
                subprocess.run(["git", "add", file_path], check=True)
                result = subprocess.run(
                    ["git", "commit", "-m", message],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                return (
                    result.stdout if result.returncode == 0 else f"Commit failed: {result.stderr}"
                )
            except subprocess.CalledProcessError as e:
                return {"error": f"Git operation failed: {e}"}

        logger.warn("tool_not_implemented", {"tool": tool_name})
    except (OSError, RuntimeError, ValueError) as e:
        # Last Resort: Top-level tool execution error handler
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


def run_job_execution(
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
            result = execute_tool(
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
    final_response = control_plane.execute(
        prompt=args.prompt,
        model_id=model_id,
        settings=settings,
        search_tool=search_tool_inst,
        root_context=root_context,
    )

    print(final_response)


if __name__ == "__main__":
    main()
