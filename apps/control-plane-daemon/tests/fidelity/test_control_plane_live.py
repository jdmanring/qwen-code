import asyncio
import json
import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch

from control_plane_daemon.control_plane import ControlPlane

# --- Mock Data ---
MOCK_SETTINGS = {
    "fastModel": "gemini-2.5-flash-lite",
    "modelProviders": {
        "google": [
            {
                "id": "gemini-2.5-flash-lite",
                "baseUrl": "https://generativelanguage.googleapis.com",
                "envKey": "GOOGLE_API_KEY",
            }
        ]
    },
}

MOCK_INTENT_RESPONSE = {
    "intent": "Targeted Bugfix",
    "reasoning": "The user wants to fix a bug in a specific file.",
    "risk_profile": "Low",
    "suggested_tool_chain": ["read_file", "edit"],
}

MOCK_AGENT_RESPONSE = "I have fixed the bug in main.py by changing 'x = 1' to 'x = 2'."


async def run_fidelity_test():
    # 1. Setup Temporary Environment
    test_dir = tempfile.mkdtemp(prefix="megalonyx-fidelity-")
    print(f"Using temporary directory: {test_dir}")

    # Create a dummy file to be "fixed"
    target_file = os.path.join(test_dir, "main.py")
    with open(target_file, "w") as f:
        f.write("def add(a, b):\n    return a - b  # BUG: should be +\n")

    # Create temporary settings.json
    settings_path = os.path.join(test_dir, "settings.json")
    with open(settings_path, "w") as f:
        json.dump(MOCK_SETTINGS, f)

    try:
        # 2. Initialize ControlPlane
        # We use the real ControlPlane class
        cp = ControlPlane(settings_path=settings_path)

        # 3. Mock the external dependencies to avoid network calls and costs
        # but keep the internal logic real.
        with (
            patch("litellm.completion") as mock_completion,
            patch("control_plane_daemon.tool_executor.run_job_execution") as mock_executor,
        ):
            # Mock LLM Intent Classification
            mock_completion.return_value.choices[0].message.content = json.dumps(
                MOCK_INTENT_RESPONSE
            )

            # Mock Job Execution result
            mock_executor.return_value = MOCK_AGENT_RESPONSE

            # Mock Verification Engine to always succeed
            with patch.object(cp.ve, "verify_job") as mock_verify:
                # Create a mock verification result
                mock_v_result = MagicMock()
                mock_v_result.is_success = True
                mock_verify.return_value = mock_v_result

                # Mock Root Context
                mock_context = MagicMock()
                mock_context.clone.return_value = mock_context

                # Mock Search Tool
                mock_search_tool = MagicMock()

                print("Executing ControlPlane flow...")
                prompt = "Fix the bug in main.py where add() subtracts instead of adds."

                # First, process the intent to populate the JobStateManager
                cp.process_intent(prompt)

                # Run the execute loop
                result = cp.execute(
                    prompt=prompt,
                    model_id="gemini-2.5-flash-lite",
                    settings=MOCK_SETTINGS,
                    search_tool=mock_search_tool,
                    root_context=mock_context,
                )

                # 4. Verifications
                print("\n--- Verifying Results ---")

                # A. Check if the result contains the mock response
                assert MOCK_AGENT_RESPONSE in result, (
                    f"The final response should contain the agent's output. Got: {result}"
                )
                print("✅ Aggregated response verified.")

                # B. Check if IntentClassifier was called
                assert mock_completion.called, (
                    "The LLM should have been called for intent classification."
                )
                print("✅ Intent classification triggered.")

                # C. Check if JobStateManager is in completed state
                assert cp.is_complete(), (
                    "The ControlPlane should report that all jobs are complete."
                )
                print("✅ Job set completion verified.")

                # D. Check if run_job_execution was called
                assert mock_executor.called, "The tool executor should have been invoked."
                print("✅ Job execution triggered.")

                print("\n✨ Fidelity Test Passed Successfully! ✨")

    finally:
        # Cleanup
        shutil.rmtree(test_dir)
        print(f"\nCleaned up {test_dir}")


if __name__ == "__main__":
    asyncio.run(run_fidelity_test())
