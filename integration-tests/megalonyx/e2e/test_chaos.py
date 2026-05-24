import os
import sys
from unittest.mock import MagicMock, patch

# Add the skills directory to sys.path for imports
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.qwen/skills"))
)

from skill_bridge import MAX_RETRIES, call_model

# Mock settings
MOCK_SETTINGS = {
    "env": {"API_KEY": "test_key"},
    "model": {"name": "qwen/qwen3-coder-480b-a35b-instruct:free"},
}


def test_exponential_backoff_on_transient_error() -> None:
    """Verify that the system retries on transient errors."""
    with patch("skill_bridge.completion") as mock_completion:
        # Simulate a 500 error for the first two calls, then success
        mock_completion.side_effect = [
            Exception("Internal Server Error 500"),
            Exception("Internal Server Error 500"),
            MagicMock(choices=[MagicMock(message=MagicMock(content="Success!"))]),
        ]

        # We use a small backoff for testing speed
        with patch("time.sleep", return_value=None):
            result = call_model(
                "qwen/qwen3-coder-480b-a35b-instruct:free", "Hello", MOCK_SETTINGS
            )

        assert result == "Success!"
        assert mock_completion.call_count == 3


def test_model_fallback_on_persistent_failure() -> None:
    """Verify that the system downshifts to a fallback model after MAX_RETRIES."""
    with patch("skill_bridge.completion") as mock_completion:
        # Always fail with a 500 error
        mock_completion.side_effect = Exception("Internal Server Error 500")

        with patch("time.sleep", return_value=None):
            # This should eventually fail or fallback
            # Since we have a fallback chain: 480B -> 120B -> 7B
            # It should try 480B (3x), then 120B (3x), then 7B (3x)
            result = call_model(
                "qwen/qwen3-coder-480b-a35b-instruct:free", "Hello", MOCK_SETTINGS
            )

        # It should eventually return the Fatal API Error after all fallbacks are exhausted
        assert "Fatal API Error" in result
        # Total calls = MAX_RETRIES * number of models in fallback chain (3 models * 3 retries = 9)
        assert mock_completion.call_count == MAX_RETRIES * 3


def test_timeout_handling() -> None:
    """Verify that timeouts trigger the retry/fallback logic."""
    with patch("skill_bridge.completion") as mock_completion:
        # Simulate a Body Timeout Error
        mock_completion.side_effect = Exception(
            "terminated (cause: Body Timeout Error)"
        )

        with patch("time.sleep", return_value=None):
            result = call_model(
                "qwen/qwen3-coder-480b-a35b-instruct:free", "Hello", MOCK_SETTINGS
            )

        assert "Fatal API Error" in result
        assert mock_completion.call_count == MAX_RETRIES * 3
