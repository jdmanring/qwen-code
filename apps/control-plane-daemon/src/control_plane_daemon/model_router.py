import json
import sys

from .execution_profile_selector import ExecutionProfileSelector
from .intent_classifier import IntentClassifier
from .policy_engine import PolicyEngine


def main() -> None:
    profile_selector = ExecutionProfileSelector()
    classifier = IntentClassifier()
    _policy_engine = PolicyEngine()

    current_file = None
    prompt_text = ""

    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i] == "--file" and i + 1 < len(args):
            current_file = args[i + 1]
        elif args[i] == "--prompt" and i + 1 < len(args):
            prompt_text = args[i + 1]

    intent_data = classifier.classify(prompt_text)
    intent_name = intent_data["intent"]

    active_profiles = profile_selector.get_active_profiles(
        current_file_path=current_file,
        prompt_text=prompt_text,
        intent=intent_name,
    )

    if not active_profiles:
        recommended_profile = "general-purpose"
        reason = "No specific profile triggered; falling back to general-purpose agent."
    else:
        profile = active_profiles[0]
        recommended_profile = profile["name"]
        reason = f"Triggered by {profile['name']} execution profile."

    result = {
        "job_contract": {
            "intent": intent_name,
            "risk_profile": intent_data["risk_profile"],
            "recommended_skill": recommended_profile,
            "suggested_tool_chain": intent_data["suggested_tool_chain"],
            "reason": reason,
        },
        "model": "inherit",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
