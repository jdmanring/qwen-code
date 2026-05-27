import asyncio

from control_plane_daemon.execution_context import ExecutionContext
from control_plane_daemon.handlers import AgentHandler
from control_plane_daemon.models import Policy
from control_plane_daemon.registry import ToolRegistry


async def test_agent_handler():
    # Setup
    registry = ToolRegistry()
    agent_handler = AgentHandler()
    registry.register(["create_agent"], agent_handler)

    context = ExecutionContext()
    policy = Policy(allowed_tools=["create_agent"], allowed_paths=["*"])

    # Test create_agent
    print("Testing create_agent...")
    res = await agent_handler.execute(
        "create_agent",
        {"description": "A helpful agent that explains quantum physics to five year olds"},
        context,
        policy,
        None,
        None,
    )
    print(f"Result success: {res.success}")
    if res.success:
        print(f"Agent data: {res.content}")
        assert "agent_data" in res.content
    else:
        print(f"Error: {res.error}")

    assert res.success is True

    print("Agent handler smoke test passed!")


if __name__ == "__main__":
    asyncio.run(test_agent_handler())
