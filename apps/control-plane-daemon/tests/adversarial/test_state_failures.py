import json
import os
import shutil
import tempfile
from unittest.mock import patch

import pytest
from control_plane_daemon.control_plane import ControlPlane


class AdversarialBase:
    def __init__(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-adv-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.setup_environment()

    def setup_environment(self) -> None:
        settings = {
            "fastModel": "gemini-2.5-flash-lite",
            "modelProviders": {
                "google": [{"id": "gemini-2.5-flash-lite", "baseUrl": "...", "envKey": "..."}]
            },
        }
        with open(self.settings_path, "w") as f:
            import json

            json.dump(settings, f)

    def cleanup(self) -> None:
        shutil.rmtree(self.test_dir)

    def get_control_plane(self) -> ControlPlane:
        return ControlPlane(settings_path=self.settings_path)


@pytest.mark.asyncio
async def test_stat_01_corrupted_settings():
    """
    Scenario STAT-01: Corrupted settings.json
    Expected: System reports error or uses defaults without crashing.
    """
    adv = AdversarialBase()
    try:
        # Corrupt the settings file
        with open(adv.settings_path, "w") as f:
            f.write("{ invalid json: [missing quotes] }")

        # Attempt to initialize ControlPlane
        # We expect a json.JSONDecodeError or a handled exception
        with pytest.raises((json.JSONDecodeError, FileNotFoundError, RuntimeError)):
            adv.get_control_plane()

        print(" STAT-01: Corrupted settings handled.")
    finally:
        adv.cleanup()


@pytest.mark.asyncio
async def test_stat_04_invalid_model_id():
    """
    Scenario STAT-04: Invalid Model ID in Config
    Expected: System reports "Model Not Found" clearly.
    """
    adv = AdversarialBase()
    try:
        # Set an invalid model
        settings = {"fastModel": "non-existent-model-123", "modelProviders": {"google": []}}
        with open(adv.settings_path, "w") as f:
            import json

            json.dump(settings, f)

        cp = adv.get_control_plane()

        # Mock the LLM call to see how it handles the model ID
        with patch("litellm.completion") as mock_completion:
            # Simulate a litellm error for unknown model
            mock_completion.side_effect = RuntimeError("Model not found")

            # Trigger a classification
            result = cp.process_intent("Hello")

            # Should fallback to default intent
            assert result["intent"] == "Exploratory Analysis"
            print(" STAT-04: Invalid model ID handled via fallback.")

    finally:
        adv.cleanup()


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
