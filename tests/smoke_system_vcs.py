import asyncio

from control_plane_daemon.execution_context import ExecutionContext
from control_plane_daemon.handlers import SystemHandler, VCSHandler
from control_plane_daemon.models import Policy
from control_plane_daemon.registry import ToolRegistry


async def test_system_vcs_handlers():
    # Setup
    stack_root = "/home/james/projects/megalonyx-monorepo"
    registry = ToolRegistry()

    sys_handler = SystemHandler(stack_root)
    vcs_handler = VCSHandler(stack_root)

    registry.register(["run-pytest", "run-mypy", "git-commit-atomic"], sys_handler)
    registry.register(["git_worktree_list", "git_worktree_add"], vcs_handler)

    context = ExecutionContext()
    policy = Policy(
        allowed_tools=["run-pytest", "run-mypy", "git_worktree_list"], allowed_paths=["*"]
    )

    # 1. Test run-mypy
    print("Testing run-mypy...")
    res = await sys_handler.execute(
        "run-mypy",
        {"path": "apps/control-plane-daemon/src/control_plane_daemon/models.py"},
        context,
        policy,
        None,
        None,
    )
    print(f"Result success: {res.success}")
    if not res.success:
        print(f"Error: {res.error}")
    assert res.success is True

    # 2. Test git_worktree_list
    print("Testing git_worktree_list...")
    res = await vcs_handler.execute("git_worktree_list", {}, context, policy, None, None)
    print(f"Result success: {res.success}")
    if not res.success:
        print(f"Error: {res.error}")
    assert res.success is True
    print("System & VCS handler smoke tests passed!")


if __name__ == "__main__":
    asyncio.run(test_system_vcs_handlers())
