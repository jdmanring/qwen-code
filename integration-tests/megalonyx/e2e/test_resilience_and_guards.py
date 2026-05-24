import os
import sys
import unittest
from unittest.mock import MagicMock

# Add the skills directory to path to import bridge components
sys.path.append(os.path.join(os.getcwd(), ".qwen/skills"))

from skill_bridge import execute_tool
from state_manager import StateManager


class TestResilienceAndGuards(unittest.TestCase):
    def setUp(self) -> None:
        # Reset state manager before each test
        self.sm = StateManager()
        self.sm.set("read_cache", [])
        self.mock_rag = MagicMock()

    def test_read_before_edit_blocked(self) -> None:
        """Verify that editing a file without reading it first is blocked."""
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file_path = tmp.name
        try:
            args = {"file_path": file_path}
            result = execute_tool("edit", args, self.mock_rag)

            self.assertIn("error", result)
            self.assertIn("CRITICAL ERROR: Tool-Level Guard Triggered", result["error"])
            print("✅ Test Passed: Edit without read was blocked.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_read_then_edit_allowed(self) -> None:
        """Verify that reading a file allows a subsequent edit."""
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file_path = tmp.name
        try:
            # 1. Perform the read
            read_args = {"file_path": file_path}
            execute_tool("read_file", read_args, self.mock_rag)

            # 2. Attempt the edit
            edit_args = {"file_path": file_path}
            result = execute_tool("edit", edit_args, self.mock_rag)

            # It should return the "not implemented" error, which signals the CLI to proceed
            self.assertIn("error", result)
            self.assertIn("not implemented in bridge", result["error"])
            print("✅ Test Passed: Edit after read was allowed (passed to CLI).")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_semantic_search_execution(self) -> None:
        """Verify that specialized tools are actually executed by the bridge."""
        self.mock_rag.semantic_search.return_value = "Found relevant code"
        args = {"query": "auth logic", "limit": 1}
        result = execute_tool("semantic_search", args, self.mock_rag)

        self.assertEqual(result, "Found relevant code")
        self.mock_rag.semantic_search.assert_called_once()
        print("✅ Test Passed: Specialized tool executed correctly.")


if __name__ == "__main__":
    unittest.main()
