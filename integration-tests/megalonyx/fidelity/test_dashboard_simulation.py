import asyncio
import os
import sys

# Ensure the core package is in the path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/core/src"))
)

from context import ExecutionContext
from control_plane import ControlPlane


async def main():
    print("Starting ControlPlane simulation with StatusManager...")
    try:
        cp = ControlPlane()
        # We need a mock context
        ctx = ExecutionContext()

        # Simulate a slash command
        prompt = "/bugfix fix the crash in auth.py"
        print(f"Simulating command: {prompt}")

        # In a real scenario, this would be called by the CLI.
        # We want to see the status manager updates in the terminal.
        # Since we are in a script, we'll manually trigger the steps.

        result = cp.process_intent(prompt)
        _job_set = result["job_set"]

        # Start the live dashboard in the background
        cp.status_manager.start()

        # Manually simulate the execution loop to see the dashboard updates
        print("Simulating execution loop...")

        # For simulation, we'll just run the workflow
        # (In reality, cp.execute would do this)
        cmd_id = "bugfix"
        workflow_result = cp.execute_workflow(cmd_id, prompt, "gpt-4", {}, None, ctx)

        print("\nWorkflow completed successfully.")
        print(f"Result: {workflow_result[:100]}...")

        # Let the dashboard settle
        await asyncio.sleep(2)
        cp.status_manager.stop()

    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"Simulation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
