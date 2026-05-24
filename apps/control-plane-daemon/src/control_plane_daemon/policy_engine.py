import json
import os
from typing import Any, TypedDict


class Policy(TypedDict):
    allowed_tools: list[str]
    allowed_paths: list[str]
    can_write: bool
    verification_level: str
    approval_required: bool


class PolicyEngine:
    def __init__(self, settings_path: str | None = None) -> None:
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        with open(settings_path) as f:
            self.settings = json.load(f)

        # --- Agent-Tool Mapping (The Unix Philosophy) ---
        # Defines which atomic tools are authorized for which micro-agent.
        self.agent_tool_map = {
            "logic-implementer": [
                "write_file",
                "edit",
                "symbol-rename",
                "wrap-in-try-catch",
                "git-commit-atomic",
                "run-mypy",
            ],
            "test-engineer": ["run-pytest", "run-mypy"],
            "performance-tuner": ["run-pytest", "edit", "read_file"],
            "security-hardener": [
                "grep_search",
                "read_file",
                "edit",
                "wrap-in-try-catch",
            ],
            "root-cause-diagnostician": [
                "read_file",
                "grep_search",
                "lsp_get_definitions",
            ],
            "doc-synchronizer": ["update-docstring", "write_file", "edit"],
            "structural-designer": ["symbol-rename", "read_file", "grep_search"],
            "general-purpose": ["todo_write", "read_file", "grep_search"],
            "explore": ["glob", "grep_search", "read_file"],
            "codebase-mapper": [
                "glob",
                "grep_search",
                "read_file",
                "lsp_get_definitions",
            ],
            "sota-synthesizer": ["read_file", "grep_search"],
            "logic-verifier": ["read_file", "grep_search"],
        }

    def get_permissions(
        self,
        intent: str,
        agent_name: str = "general-purpose",
        context: dict[str, Any] | None = None,
    ) -> Policy:
        """
        Returns the permissions and boundaries for a given intent and agent.
        """
        context = context or {}
        current_file = context.get("current_file")

        # 1. Base Intent Policy (General boundaries)
        policy: Policy = {
            "allowed_tools": ["glob", "grep_search", "read_file", "todo_write"],
            "allowed_paths": ["*"],
            "can_write": False,
            "verification_level": "Low",
            "approval_required": False,
        }

        if intent == "Exploratory Analysis":
            pass
        elif intent == "Surgical Correction":
            policy["can_write"] = True
            policy["verification_level"] = "Medium"
            if current_file:
                policy["allowed_paths"] = [str(current_file)]
            else:
                policy["approval_required"] = True
        elif intent == "Feature Synthesis":
            policy["can_write"] = True
            policy["verification_level"] = "High"
            policy["approval_required"] = True
        elif intent == "Structural Evolution":
            policy["can_write"] = True
            policy["verification_level"] = "Critical"
            policy["approval_required"] = True
        elif intent == "Adversarial Review":
            policy["verification_level"] = "Medium"
        elif intent == "Knowledge Sync":
            policy["can_write"] = True
            policy["allowed_paths"] = ["**/docs/**", "README.md", "QWEN.md"]
            policy["verification_level"] = "Low"

        # 2. Agent-Specific Tool Augmentation
        # Merge the agent's authorized tools into the policy
        agent_tools = self.agent_tool_map.get(agent_name, [])
        policy["allowed_tools"] = list(set(policy["allowed_tools"] + agent_tools))

        return policy


if __name__ == "__main__":
    engine = PolicyEngine()
    # Test a surgical fix on a specific file
    print(
        "Surgical Fix (with file): "
        + json.dumps(
            engine.get_permissions("Surgical Correction", context={"current_file": "/src/main.py"}),
            indent=2,
        )
    )
    # Test a feature synthesis
    print(f"Feature Synthesis: {json.dumps(engine.get_permissions('Feature Synthesis'), indent=2)}")
