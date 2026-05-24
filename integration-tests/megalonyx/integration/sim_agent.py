import asyncio
import os

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Environment Setup
if os.environ.get("QWEN_STACK_ROOT"):
    STACK_ROOT = os.environ.get("QWEN_STACK_ROOT")
else:
    INSTALLED_STACK = os.path.expanduser("~/.local/share/megalonyx")
    LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    STACK_ROOT = (
        INSTALLED_STACK
        if os.path.exists(os.path.join(INSTALLED_STACK, "py/venv"))
        else LOCAL_STACK
    )

VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")

MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


class SimAgent:
    """
    Simulates the cognitive loop of Qwen Code regarding memory.
    It does NOT use a real LLM for decision making in this test,
    but instead uses a 'Decision Matrix' to simulate correct agent behavior.
    """

    def __init__(self, session: ClientSession) -> None:
        self.session = session

    async def handle_prompt(self, prompt: str):
        print(f"\n[User]: {prompt}")

        # Simulation of the Agent's 'Thought' process
        # In a real scenario, the LLM would decide this.
        if any(
            k in prompt.lower()
            for k in ["remember", "note that", "preference is", "architecture is"]
        ):
            print(
                "[Agent Thought]: This sounds like a fact I should remember. Calling 'ingest'..."
            )
            # Simulate the agent extracting the core fact
            fact = prompt.replace("Remember that ", "").replace("Note that ", "")

            # The agent must decide the tier (simulating MemoryAuthority's signal logic)
            tier = (
                "cloud"
                if any(
                    k in fact.lower() for k in ["architecture", "policy", "standard"]
                )
                else "local"
            )

            res = await self.session.call_tool("ingest", {"text": fact, "tier": tier})
            print(
                f"[Agent Action]: ingest({fact}, tier={tier}) -> {res.content[0].text}"
            )
            return res

        elif any(
            k in prompt.lower()
            for k in ["what", "recall", "search", "preference", "architecture"]
        ):
            print(
                "[Agent Thought]: I need to retrieve information to answer this. Calling 'search'..."
            )
            query = prompt.replace("What is ", "").replace("Recall ", "")

            res = await self.session.call_tool(
                "search", {"query": query, "tier": "auto"}
            )
            print(f"[Agent Action]: search({query}) -> {res.content[0].text}")
            return res

        else:
            print("[Agent Thought]: No memory tools needed for this prompt.")
            return None


async def run_usage_scenario():
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = SimAgent(session)

            # Scenario 1: Memory Ingestion
            await agent.handle_prompt(
                "Remember that the project architecture uses a 4-layer model."
            )
            await asyncio.sleep(1)

            # Scenario 2: Memory Recall
            await agent.handle_prompt("What is the project architecture?")
            await asyncio.sleep(1)

            # Scenario 3: Local Preference
            await agent.handle_prompt(
                "Note that I prefer using async/await for all network calls."
            )
            await asyncio.sleep(1)

            # Scenario 4: Local Recall
            await agent.handle_prompt("What is my preference for network calls?")


if __name__ == "__main__":
    asyncio.run(run_usage_scenario())
