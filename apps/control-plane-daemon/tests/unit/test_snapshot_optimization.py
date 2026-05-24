import os
import sys
from typing import Any

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from control_plane_daemon.state_manager import StateManager
from control_plane_daemon.tool_executor import call_model


class MockSettings:
    def get(self, key: str, default: Any = None) -> Any:
        if key == "model":
            return {"name": "qwen/qwen3-coder-480b-a35b-instruct:free"}
        return default


def test_state_manager_archive() -> None:
    # Use a temporary state file for testing
    state_file = ".qwen/test_state.json"
    os.makedirs(os.path.dirname(state_file), exist_ok=True)

    sm = StateManager(state_file=state_file)
    sm.set("rag_context", {"test_key": "test_value"})

    # Verify it's in rag_context
    assert sm.get("rag_context")["test_key"] == "test_value"

    # Perform archive
    success = sm.archive_item("test_key")

    assert success is True
    assert "test_key" not in sm.get("rag_context")
    assert len(sm.get("archive")) == 1
    assert sm.get("archive")[0]["key"] == "test_key"
    assert sm.get("archive")[0]["content"] == "test_value"

    # Cleanup
    if os.path.exists(state_file):
        os.remove(state_file)


def test_skill_bridge_prompt_assembly(monkeypatch: Any) -> None:
    # Mocking litellm.completion
    class MockResponse:
        def __init__(self) -> None:
            self.choices = [
                type(
                    "obj",
                    (object,),
                    {"message": type("obj", (object,), {"content": "AI Response"})()},
                )
            ]

    monkeypatch.setattr(
        "control_plane_daemon.tool_executor.completion", lambda **kwargs: MockResponse()
    )

    # Mocking SystemLogger to avoid print/log issues
    monkeypatch.setattr(
        "control_plane_daemon.tool_executor.SystemLogger",
        lambda: type(
            "obj",
            (object,),
            {
                "info": lambda *a, **k: None,
                "error": lambda *a, **k: None,
                "warn": lambda *a, **k: None,
            },
        )(),
    )

    # Setup StateManager
    state_file = ".qwen/test_state_prompt.json"
    sm = StateManager(state_file=state_file)
    sm.set("active_phase", "TEST_PHASE")
    sm.set("todo_list", [{"id": "1", "status": "pending", "content": "test task"}])

    settings = MockSettings()
    model_id = "qwen/qwen3-coder-480b-a35b-instruct:free"
    prompt = "Hello"

    # We need to capture the sys_prompt passed to completion
    # We'll use a list to capture the calls
    captured_messages = []

    def mock_completion_with_capture(**kwargs) -> None:
        captured_messages.append(kwargs["messages"])
        return MockResponse()

    monkeypatch.setattr(
        "control_plane_daemon.tool_executor.completion", mock_completion_with_capture
    )

    call_model(
        model_id,
        prompt,
        settings,
        skill_config={"system_prompt": "Mock Sys Prompt"},
        state_manager_inst=sm,
    )

    # Verify the system message
    assert len(captured_messages) > 0
    messages = captured_messages[0]
    system_message = next((m for m in messages if m["role"] == "system"), None)

    assert system_message is not None
    assert "# STATE" in system_message["content"]
    assert "TEST_PHASE" in system_message["content"]
    assert "test task" in system_message["content"]

    # Cleanup
    if os.path.exists(state_file):
        os.remove(state_file)
