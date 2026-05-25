import json
import os
from typing import Any, cast

from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.qwen/.env"))

# --- Taxonomy Definition ---
INTENT_TAXONOMY = {
    "Exploratory Analysis": {
        "description": "Read-only investigation to understand system behavior, data flow, or locate specific logic.",
        "goal": "A verified mental model or a set of identified file paths/symbols.",
        "tool_chain": ["glob", "grep_search", "codebase-mapper", "read_file"],
        "risk_profile": "Low",
        "verification": "Low",
    },
    "Targeted Bugfix": {
        "description": "Targeted fix for a known bug or a specific logic error in a localized area of the code.",
        "goal": "The bug is resolved; existing tests pass; no regressions introduced in the local scope.",
        "tool_chain": ["read_file", "edit", "test-coverage-max"],
        "risk_profile": "Low-Med",
        "verification": "Medium",
    },
    "Feature Implementation": {
        "description": "Implementation of new functionality based on a design specification or user requirement.",
        "goal": "New logic is implemented and verified against the spec; new tests cover the happy path and edge cases.",
        "tool_chain": ["todo_write", "read_file", "edit", "test-coverage-max"],
        "risk_profile": "Med",
        "verification": "High",
    },
    "Architectural Refactor": {
        "description": "Systemic refactoring to improve maintainability, performance, or architecture without changing external behavior.",
        "goal": "Code is reorganized; architectural debt is reduced; behavior is identical (verified by regression tests).",
        "tool_chain": ["grep_search", "refactor-safe", "batch", "review"],
        "risk_profile": "High",
        "verification": "Critical",
    },
    "System Audit": {
        "description": "Proactive search for vulnerabilities, race conditions, memory leaks, or performance bottlenecks.",
        "goal": "A documented list of flaws with evidence; proposed remediation paths.",
        "tool_chain": ["review", "root-cause-hunter", "grep_search"],
        "risk_profile": "Low",
        "verification": "Medium",
    },
    "Knowledge Sync": {
        "description": "Aligning documentation, READMEs, or type definitions with the actual current implementation.",
        "goal": "Documentation is a truthful reflection of the code; no discrepancy between 'what it says' and 'what it does'.",
        "tool_chain": ["read_file", "doc-sync", "edit"],
        "risk_profile": "Low",
        "verification": "Low",
    },
}


class IntentClassifier:
    def __init__(self, settings_path: str | None = None) -> None:
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        with open(settings_path) as f:
            self.settings = json.load(f)

        # Use a fast model for classification to minimize latency
        self.model_id = self.settings.get("fastModel", "gemini-2.5-flash-lite")
        self.model_config = self._resolve_model_config(self.model_id)

    def _resolve_model_config(self, mid: str) -> dict[str, Any]:
        """Helper to find provider, baseUrl, and envKey from settings.json"""
        for provider_group, models in self.settings.get("modelProviders", {}).items():
            for m in models:
                if m["id"] == mid:
                    return {
                        "group": provider_group,  # e.g., 'openai'
                        "model_id": mid,
                        "base_url": m.get("baseUrl", ""),
                        "env_key": m.get("envKey", "OPENAI_API_KEY"),
                    }
        return {
            "group": "openai",
            "model_id": mid,
            "base_url": "",
            "env_key": "OPENAI_API_KEY",
        }

    def classify(self, prompt: str) -> dict[str, Any]:
        """
        Classifies a user prompt into one of the predefined intents using the taxonomy.
        """
        system_prompt = f"""You are the Mega Code Intent Classifier. Your sole purpose is to categorize a user's request into one of the following intents based on the provided taxonomy.

TAXONOMY:
{json.dumps(INTENT_TAXONOMY, indent=2)}

DECISION TREE:
1. Mutation Check: Is the intent to change executable code?
   - NO -> Read-Only/Meta Triage:
     - Goal is to find/understand? -> Exploratory Analysis
     - Goal is to find flaws/security holes? -> Adversarial Review
     - Goal is to update docs/non-executable text? -> Knowledge Sync
   - YES -> Mutation Triage:
     - Additive (New Feature)? -> Feature Synthesis
     - Corrective (Bug Fix)? -> Surgical Correction
     - Structural (Refactor/Cleanup)? -> Structural Evolution

OUTPUT FORMAT:
You must return ONLY a JSON object with the following keys:
{{
  "intent": "Intent Name",
  "reasoning": "Brief explanation of why this intent was chosen",
  "risk_profile": "Low|Med|High",
  "suggested_tool_chain": ["tool1", "tool2"]
}}
"""

        try:
            # Use LiteLLM to call the fast model
            from litellm import completion

            # Resolve configuration from settings.json
            config = self.model_config
            group = config["group"]
            model_id = config["model_id"]
            api_base = config["base_url"]
            env_key = config["env_key"]

            # Explicitly fetch the key from the environment
            api_key = os.environ.get(env_key)

            response = completion(
                model=f"{group}/{model_id}",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                api_base=api_base,
                api_key=api_key,
                response_format={"type": "json_object"},
            )

            return cast(dict[str, Any], json.loads(response.choices[0].message.content))
        except (json.JSONDecodeError, RuntimeError, ValueError) as e:
            print(f"Classification Error: {e}")
            # Fallback to a safe default
            return {
                "intent": "Exploratory Analysis",
                "reasoning": "Fallback due to classification error.",
                "risk_profile": "Low",
                "suggested_tool_chain": ["glob", "grep_search", "read_file"],
            }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('Usage: python intent_classifier.py "User prompt here"')
        sys.exit(1)

    classifier = IntentClassifier()
    result = classifier.classify(sys.argv[1])
    print(json.dumps(result, indent=2))
