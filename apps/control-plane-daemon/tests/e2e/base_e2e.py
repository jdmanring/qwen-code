import json
import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch

from control_plane_daemon.control_plane import ControlPlane


class E2EBase:
    """
    Base class for End-to-End tests of the Control Plane.
    Handles environment isolation and common setup.
    """

    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-e2e-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.setup_environment()

    def setup_environment(self):
        # Default mock settings
        settings = {
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
        with open(self.settings_path, "w") as f:
            json.dump(settings, f)

    def create_file(self, relative_path: str, content: str):
        full_path = os.path.join(self.test_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return full_path

    def cleanup(self):
        shutil.rmtree(self.test_dir)

    def get_control_plane(self) -> ControlPlane:
        return ControlPlane(settings_path=self.settings_path)

    async def run_scenario(self, prompt: str, mock_intent: dict, mock_execution_results: list[str]):
        """
        Runs a full ControlPlane cycle with mocked LLM responses.
        """
        cp = self.get_control_plane()

        # Mock root context
        mock_context = MagicMock()
        mock_context.clone.return_value = mock_context
        mock_search_tool = MagicMock()

        with (
            patch("litellm.completion") as mock_completion,
            patch("control_plane_daemon.tool_executor.run_job_execution") as mock_executor,
            patch.object(cp.ve, "verify_job") as mock_verify,
        ):
            # 1. Mock Intent Classification
            mock_completion.return_value.choices[0].message.content = json.dumps(mock_intent)

            # 2. Mock Job Execution (sequential results for multiple jobs)
            mock_executor.side_effect = mock_execution_results

            # 3. Mock Verification to always succeed
            mock_v_result = MagicMock()
            mock_v_result.is_success = True
            mock_verify.return_value = mock_v_result

            # Process intent and execute
            cp.process_intent(prompt)
            result = cp.execute(
                prompt=prompt,
                model_id="gemini-2.5-flash-lite",
                settings=json.load(open(self.settings_path)),
                search_tool=mock_search_tool,
                root_context=mock_context,
            )

            return result, cp
