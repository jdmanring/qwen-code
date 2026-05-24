import asyncio


class GitError(Exception):
    """Custom exception for Git operations."""

    pass


class GitWorktreeManager:
    def __init__(self, repo_path: str) -> None:
        self.repo_path = repo_path

    async def _run_git(self, args: list[str]) -> str:
        """Runs a git command and returns the output."""
        process = await asyncio.create_subprocess_exec(
            "git",
            "-C",
            self.repo_path,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise GitError(f"Git command failed: {stderr.decode().strip()}")

        return stdout.decode().strip()

    async def list_worktrees(self) -> list[dict[str, str]]:
        """Lists all active worktrees."""
        output = await self._run_git(["worktree", "list", "--porcelain"])
        worktrees = []
        current_worktree: dict[str, str] = {}

        for line in output.splitlines():
            if line.startswith("worktree "):
                if current_worktree:
                    worktrees.append(current_worktree)
                current_worktree = {"path": line.split(" ", 1)[1]}
            elif line.startswith("branch "):
                current_worktree["branch"] = line.split(" ", 1)[1]
            elif line == "":
                if current_worktree:
                    worktrees.append(current_worktree)
                    current_worktree = {}

        if current_worktree:
            worktrees.append(current_worktree)

        return worktrees

    async def add_worktree(self, branch: str, path: str) -> str:
        """Adds a new worktree for a specific branch."""
        return await self._run_git(["worktree", "add", "-b", branch, path])

    async def remove_worktree(self, path: str) -> str:
        """Removes an existing worktree."""
        return await self._run_git(["worktree", "remove", path])

    async def prune_worktrees(self) -> str:
        """Prunes stale worktree information."""
        return await self._run_git(["worktree", "prune"])


if __name__ == "__main__":
    import os
    import sys

    async def test() -> None:
        repo_dir = os.getcwd()
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            print("Error: Current directory is not a git repository.", file=sys.stderr)
            return

        mgr = GitWorktreeManager(repo_dir)
        try:
            print("Listing worktrees...", file=sys.stderr)
            worktrees = await mgr.list_worktrees()
            print(worktrees, file=sys.stderr)
        except GitError as e:
            print(f"Error: {e}", file=sys.stderr)

    asyncio.run(test())
