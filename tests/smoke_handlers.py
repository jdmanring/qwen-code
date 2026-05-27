import asyncio

from control_plane_daemon.execution_context import ExecutionContext
from control_plane_daemon.handlers import FileHandler, SearchHandler
from control_plane_daemon.models import Policy
from control_plane_daemon.registry import ToolRegistry


def test_handlers():
    # Setup
    stack_root = "/home/james/projects/megalonyx-monorepo"
    registry = ToolRegistry()

    file_handler = FileHandler(stack_root)
    search_handler = SearchHandler(stack_root)

    registry.register(["read_file", "write_file"], file_handler)
    registry.register(["grep_search", "semantic_search"], search_handler)

    context = ExecutionContext()
    policy = Policy(allowed_tools=["read_file", "write_file", "grep_search"], allowed_paths=["*"])

    # 1. Test write_file
    print("Testing write_file...")
    res = asyncio.run(
        file_handler.execute(
            "write_file",
            {"file_path": "tests/registry_test.txt", "content": "Hello Registry"},
            context,
            policy,
            None,
            None,
        )
    )
    print(f"Result: {res.content}")
    assert res.success is True

    # 2. Test read_file
    print("Testing read_file...")
    res = asyncio.run(
        file_handler.execute(
            "read_file", {"file_path": "tests/registry_test.txt"}, context, policy, None, None
        )
    )
    print(f"Result: {res.content}")
    assert res.success is True
    assert res.content == "Hello Registry"

    # 3. Test grep_search
    print("Testing grep_search...")
    res = asyncio.run(
        search_handler.execute(
            "grep_search",
            {"pattern": "Hello Registry", "path": "tests/registry_test.txt"},
            context,
            policy,
            None,
            None,
        )
    )
    print(f"Result: {res.content}")
    assert res.success is True
    assert "Hello Registry" in res.content

    print("All handler smoke tests passed!")


if __name__ == "__main__":
    test_handlers()
