import json
import sys

from .intent_classifier import IntentClassifier
from .policy_engine import PolicyEngine
from .skill_selector import SkillSelector


def main() -> None:
    orchestrator = SkillSelector()
    classifier = IntentClassifier()
    _policy_engine = PolicyEngine()

    # Default values
    current_file = None
    prompt_text = ""

    # Parse arguments
    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i] == "--file" and i + 1 < len(args):
            current_file = args[i + 1]
        elif args[i] == "--prompt" and i + 1 < len(args):
            prompt_text = args[i + 1]

    # 1. Strategic Triage: Classify the Intent
    intent_data = classifier.classify(prompt_text)
    intent_name = intent_data["intent"]

    # 2. Agent Selection: Find the best skill for this intent
    # We pass the prompt and file to the orchestrator as before
    active_skills = orchestrator.get_active_skills(
        current_file_path=current_file, prompt_text=prompt_text
    )

    if not active_skills:
        recommended_skill = "general-purpose"
        reason = "No specific skill triggered; falling back to general-purpose agent."
    else:
        skill = active_skills[0]
        recommended_skill = skill["name"]
        reason = f"Triggered by {skill['name']} skill configuration."

    # 3. Construct the Job Contract
    result = {
        "job_contract": {
            "intent": intent_name,
            "risk_profile": intent_data["risk_profile"],
            "recommended_skill": recommended_skill,
            "suggested_tool_chain": intent_data["suggested_tool_chain"],
            "reason": reason,
        },
        "model": "inherit",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
