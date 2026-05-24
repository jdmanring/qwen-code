import asyncio
import sys

from control_plane_daemon.control_plane import ControlPlane
from control_plane_daemon.execution_context import ExecutionContext


async def main():
    print("Starting ControlPlane simulation with StatusManager...")
    try:
        cp = ControlPlane()
        ctx = ExecutionContext()

        prompt = "/bugfix fix the crash in auth.py"
        print(f"Simulating command: {prompt}")

        result = cp.process_intent(prompt)
        _job_set = result["job_set"]

        cp.status_manager.start()

        print("Simulating execution loop...")

        cmd_id = "bugfix"
        workflow_result = cp.execute_workflow(cmd_id, prompt, "gpt-4", {}, None, ctx)

        print("\nWorkflow completed successfully.")
        print(f"Result: {workflow_result[:100]}...")

        await asyncio.sleep(2)
        cp.status_manager.stop()

    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"Simulation failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
