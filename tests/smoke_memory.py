import asyncio

from control_plane_daemon.execution_context import ExecutionContext
from control_plane_daemon.handlers import MemoryHandler
from control_plane_daemon.models import Policy
from control_plane_daemon.registry import ToolRegistry


async def test_memory_handler():
    # Setup
    registry = ToolRegistry()
    memory_handler = MemoryHandler()
    registry.register(
        ["memory_ingest", "memory_search", "memory_reflect", "archive_knowledge"], memory_handler
    )

    context = ExecutionContext()
    policy = Policy(allowed_tools=["memory_ingest", "memory_search"], allowed_paths=["*"])

    # We need a mock state manager for archive_knowledge
    class MockStateManager:
        def archive_item(self, key):
            return True

    sm = MockStateManager()

    # 1. Test memory_ingest
    print("Testing memory_ingest...")
    res = await memory_handler.execute(
        "memory_ingest", {"text": "The quick brown fox", "tier": "auto"}, context, policy, None, sm
    )
    print(f"Result: {res.content}")
    assert res.success is True

    # 2. Test memory_search
    print("Testing memory_search...")
    res = await memory_handler.execute(
        "memory_search", {"query": "brown fox"}, context, policy, None, sm
    )
    print(f"Result: {res.content}")
    assert res.success is True

    # 3. Test archive_knowledge
    print("Testing archive_knowledge...")
    res = await memory_handler.execute(
        "archive_knowledge", {"key": "test_key"}, context, policy, None, sm
    )
    print(f"Result: {res.content}")
    assert res.success is True

    print("All memory handler tests passed!")


if __name__ == "__main__":
    asyncio.run(test_memory_handler())
