import os
import re
from typing import Any, TypedDict

import yaml

from .state_manager import StateManager


class AnalysisResult(TypedDict):
    confidence: float
    next_step: str | None
    needs_review: bool


class SkillSelector:
    def __init__(self, services_dir: str | None = None) -> None:
        if services_dir is None:
            # Default to the deployed skills directory in the user's home
            services_dir = os.path.expanduser("~/.qwen/skills")
        self.services_dir = services_dir
        self.skills: dict[
            str, dict[str, Any]
        ] = {}  # Keeping the name 'skills' for compatibility during migration
        self.state_manager = StateManager()
        self.load_services()

    def load_services(self) -> None:
        """Loads all service configurations from the services directory."""
        from pathlib import Path

        # Search for both .yaml files and SKILL.md files
        yaml_files = list(Path(self.services_dir).rglob("*.yaml"))
        md_files = list(Path(self.services_dir).rglob("**/SKILL.md"))

        for file_path in yaml_files + md_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                    if file_path.suffix == ".md":
                        # Parse YAML frontmatter from Markdown
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                config = yaml.safe_load(parts[1])
                            else:
                                continue
                        else:
                            continue
                    else:
                        # Standard YAML file
                        config = yaml.safe_load(content)

                    if config and "name" in config:
                        # Flatten the config for the existing scoring logic
                        triggers = config.get("triggers", {})
                        if "capabilities" in config:
                            triggers.update(config["capabilities"].get("triggers", {}))

                        flattened = {
                            "name": config["name"],
                            "description": config.get("description", ""),
                            "triggers": triggers,
                            "tools": config.get("capabilities", {}).get("tools", []),
                            "model": config.get("capabilities", {}).get("model", "inherit"),
                            "system_prompt": config.get("persona", {}).get("system_prompt", ""),
                            "reporting_schema": config.get("persona", {}).get(
                                "reporting_schema", ""
                            ),
                        }
                        self.skills[config["name"]] = flattened
            except (OSError, UnicodeDecodeError, yaml.YAMLError):
                pass

    def analyze_report(self, report_text: str) -> AnalysisResult:
        """
        Parses a sub-agent's structured report to extract confidence and next steps.
        """
        analysis: AnalysisResult = {
            "confidence": 1.0,
            "next_step": None,
            "needs_review": False,
        }

        conf_match = re.search(r"CONFIDENCE:\s*([\d.]+)", report_text, re.IGNORECASE)
        if conf_match:
            analysis["confidence"] = float(conf_match.group(1))
            if analysis["confidence"] < 0.7:
                analysis["needs_review"] = True

        next_match = re.search(r"NEXT STEP:\s*(.*)", report_text, re.IGNORECASE)
        if next_match:
            analysis["next_step"] = next_match.group(1).strip()

        return analysis

    def _calculate_score(
        self,
        skill_name: str,
        config: dict[str, Any],
        prompt_text: str,
        current_file_path: str | None,
    ) -> float:
        """
        STRMAC-inspired scoring function to determine the best agent for the current state.
        """
        score = 0.0
        phase = self.state_manager.get("active_phase", "PLANNING")

        # 1. Capability Match (Keywords/Extensions)
        triggers = config.get("triggers", {})
        if "keywords" in triggers:
            if any(kw.lower() in prompt_text.lower() for kw in triggers["keywords"]):
                score += 2.0  # Increased weight for keywords

        if current_file_path:
            ext = os.path.splitext(current_file_path)[1]
            if "file_extensions" in triggers and ext in triggers["file_extensions"]:
                score += 0.5  # Lower weight for extensions

        # 2. Phase Match (Role Alignment)
        phase_map = {
            "PLANNING": ["architect", "scout", "researcher"],
            "IMPLEMENTATION": ["developer"],
            "VERIFICATION": ["reviewer", "qa_lead"],
            "OPTIMIZATION": ["system_optimizer"],
        }
        if skill_name in phase_map.get(phase, []):
            score += 1.5

        # 3. Confidence Penalty / Reviewer Boost
        last_agent = self.state_manager.get("last_agent")
        if skill_name == "reviewer" and last_agent != "reviewer":
            if phase == "VERIFICATION":
                score += 1.0

        return score

    def get_active_skills(
        self,
        current_file_path: str | None = None,
        prompt_text: str = "",
        report_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Determines the best skill using state-aware scoring.
        """
        scores = {}

        for name, config in self.skills.items():
            scores[name] = self._calculate_score(name, config, prompt_text, current_file_path)

        if report_context and report_context.get("next_step"):
            next_step = report_context["next_step"].lower()
            for name in scores:
                if name.lower() in next_step:
                    scores[name] += 2.0

        if report_context and report_context.get("needs_review"):
            if "reviewer" in scores:
                scores["reviewer"] += 3.0

        sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        active_skills = []
        for name, score in sorted_skills:
            if score > 0:
                active_skills.append(self.skills[name])

        return active_skills


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["list", "check", "check_prompt"])
    parser.add_argument("--services_dir", type=str, help="Directory to load skills from")
    parser.add_argument("arg", nargs="?", help="Argument for check/check_prompt")

    args = parser.parse_args()

    orchestrator = SkillSelector(services_dir=args.services_dir)

    if args.command == "list":
        print(f"Loaded skills: {list(orchestrator.skills.keys())}")
    elif args.command == "check" and args.arg:
        active = orchestrator.get_active_skills(current_file_path=args.arg)
        print(f"Active skills for {args.arg}: {[s['name'] for s in active]}")
    elif args.command == "check_prompt" and args.arg:
        active = orchestrator.get_active_skills(prompt_text=args.arg)
        print(f"Active skills for prompt '{args.arg}': {[s['name'] for s in active]}")
    else:
        parser.print_help()
