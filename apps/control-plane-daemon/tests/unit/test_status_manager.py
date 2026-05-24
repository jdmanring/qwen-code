import asyncio
from pathlib import Path

# Add project root to sys.path to import local modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent

from control_plane_daemon.status_manager import StatusManager  # noqa: E402
from rich.console import Console  # noqa: E402


async def main():
    console = Console()
    sm = StatusManager(console=console)
    sm.start()

    sm.update_agent("Architect", "Designing system")
    sm.update_job_status("job_1", "Running", 10.0, "Step 1: Research")
    await asyncio.sleep(1)

    sm.update_job_status("job_1", "Running", 40.0, "Step 2: Planning")
    await asyncio.sleep(1)

    sm.update_agent("Developer", "Writing code")
    sm.update_job_status("job_1", "Running", 70.0, "Step 3: Implementation")
    await asyncio.sleep(1)

    sm.update_job_status("job_1", "Completed", 100.0, "Step 4: Verification")
    await asyncio.sleep(1)

    sm.stop()


if __name__ == "__main__":
    asyncio.run(main())
