import asyncio
import json
from pathlib import Path

import pytest

# Add project root to sys.path to import local modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent

from control_plane_daemon.agent_generator import AgentGeneratorService  # noqa: E402
from control_plane_daemon.tool_executor import load_settings  # noqa: E402


@pytest.mark.asyncio
async def test_agent_generation(monkeypatch):
    print("Starting Agent Generation Test...")

    # Mocking litellm.completion to avoid real network calls
    class MockResponse:
        def __init__(self) -> None:
            self.choices = [
                type(
                    "obj",
                    (object,),
                    {
                        "message": type(
                            "obj",
                            (object,),
                            {
                                "content": json.dumps(
                                    {
                                        "name": "test-agent",
                                        "description": "A test agent description",
                                        "systemPrompt": "A test system prompt",
                                    }
                                )
                            },
                        )()
                    },
                )
            ]

    monkeypatch.setattr(
        "control_plane_daemon.agent_generator.completion", lambda **kwargs: MockResponse()
    )

    settings = load_settings()
    gen_service = AgentGeneratorService(settings)

    test_description = "A security auditor who focuses on finding vulnerabilities in Python code."
    print(f"Generating agent for description: {test_description}")

    try:
        agent_data = await gen_service.generate(test_description)
        print("Agent generation successful!")
        print(f"Agent Name: {agent_data.get('name')}")

        # Verify the returned data
        assert agent_data["name"] == "test-agent"
        assert agent_data["description"] == "A test agent description"
        assert agent_data["systemPrompt"] == "A test system prompt"

    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"Agent generation failed with error: {e}")
        import traceback

        traceback.print_exc()
        raise e


if __name__ == "__main__":
    asyncio.run(test_agent_generation())
