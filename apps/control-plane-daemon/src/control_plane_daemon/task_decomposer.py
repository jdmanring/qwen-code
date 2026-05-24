import json
import os
import time
from typing import Any

import litellm
import yaml


class TaskDecomposer:
    def __init__(self, settings_path: str | None = None) -> None:
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        with open(settings_path) as f:
            self.settings = json.load(f)

    def _get_available_skills(self) -> str:
        """Extracts available skills from YAML persona files in config/prompts/agents/."""
        try:
            agents_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "prompts",
                "agents",
            )
            skill_list = []
            for filename in os.listdir(agents_dir):
                if filename.endswith(".yaml"):
                    name = filename.replace(".yaml", "")
                    with open(os.path.join(agents_dir, filename)) as f:
                        data = yaml.safe_load(f)
                        persona = data.get("persona", "No description available.")
                        summary = persona.split(".")[0] if "." in persona else persona
                        skill_list.append(f"- {name}: {summary}")
            return "\\n".join(skill_list)
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            # Fallback list if directory read fails
            return "- general-purpose, explore, structural-designer, logic-implementer, test-engineer, performance-tuner, codebase-mapper, sota-synthesizer, logic-verifier, security-hardener, root-cause-diagnostician, doc-synchronizer"

    def decompose(self, job_contract: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Breaks a high-level Job Contract into a sequence of atomic Jobs.
        Now uses dynamic LLM-driven decomposition with a fallback to static templates.
        """
        intent = job_contract["intent"]
        original_prompt = job_contract.get("original_prompt", "No original prompt provided.")

        # --- Dynamic LLM Decomposition ---
        try:
            # 1. Handle API keys and environment variables
            env_vars = self.settings.get("env", {})
            for key, value in env_vars.items():
                os.environ[key] = os.path.expandvars(str(value))

            # 2. Determine model
            model_name = self.settings.get("model", {}).get("name", "gpt-4")

            # 3. Construct System Prompt
            skills_info = self._get_available_skills()
            system_prompt = (
                "You are a Strategic Task Decomposer. Your goal is to break a high-level user intent "
                "into a sequence of atomic, verifiable jobs that a multi-agent system can execute.\\n\\n"
                f"Available Skills:\\n{skills_info}\\n\\n"
                "UNIX PHILOSOPHY: Each job must be assigned to the most granular specialist possible. "
                "Do not use 'general-purpose' if a specialized agent (e.g., 'logic-implementer') can do the job. "
                "Do not use 'logic-implementer' if 'test-engineer' is more appropriate for verification.\\n\\n"
                "Surgical Pipeline (feat-dev): For feature requests or significant changes, you MUST follow this sequence:\\n"
                "1. Investigate (explore/researcher) -> 2. Design (architect) -> 3. Test Plan (test-engineer) -> "
                "4. Dry-Run (test-engineer: prove baseline fails) -> 5. Implement (developer) -> "
                "6. Verify (test-engineer: prove fix works) -> 7. Review (reviewer).\\n\\n"
                "Logical Flow:\\nEnsure the sequence follows a logical progression: Discovery -> Analysis -> Mutation -> Verification.\\n\\n"
                "Output Format:\\nYou MUST return a JSON list of jobs. Each job must have:\\n"
                "- description: A clear, actionable task.\\n"
                "- skill: One of the available skills listed above.\\n"
                "- type: The category of work (e.g., 'discovery', 'analysis', 'mutation', 'verification', 'synthesis').\\n"
                "- verification_criteria: A binary condition to determine if the job succeeded.\\n\\n"
                "Example Output:\\n"
                '[\\n  {\\"description\\": \\"Map the current authentication flow\\", \\"skill\\": \\"explore\\", \\"type\\": \\"discovery\\", \\"verification_criteria\\": \\"A complete call graph of the auth flow is produced\\"},\\n'
                '  {\\"description\\": \\"Identify the race condition in the token refresh logic\\", \\"skill\\": \\"root-cause-diagnostician\\", \\"type\\": \\"analysis\\", \\"verification_criteria\\": \\"The exact line causing the race is isolated\\"}\\n]'
            )

            user_prompt = f"User Intent: {intent}\\nOriginal Prompt: {original_prompt}\\n\\nGenerate the sequence of atomic jobs in JSON format."

            response = litellm.completion(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
                if "gpt-4" in model_name or "claude" in model_name
                else None,
            )

            content = response.choices[0].message.content
            # Handle cases where the model wraps JSON in markdown blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # The model might return {"jobs": [...]} or just [...]
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "jobs" in parsed:
                sequence = parsed["jobs"]
            elif isinstance(parsed, list):
                sequence = parsed
            else:
                raise ValueError("LLM returned JSON but not in the expected list/jobs format")

            # Validate that we got a list of jobs with required keys
            if not isinstance(sequence, list) or not all(
                all(k in j for k in ("description", "skill", "type", "verification_criteria"))
                for j in sequence
            ):
                raise ValueError("LLM returned incomplete job definitions")

        except (json.JSONDecodeError, ValueError, RuntimeError):
            # --- Fallback Mechanism ---
            # print(f"Dynamic decomposition failed: {e}. Falling back to static templates.")

            # Decomposition Templates based on Intent
            templates = {
                "Exploratory Analysis": [
                    {
                        "desc": "Map relevant symbols and file paths",
                        "skill": "explore",
                        "type": "discovery",
                    },
                    {
                        "desc": "Analyze data flow and logic patterns",
                        "skill": "researcher",
                        "type": "analysis",
                    },
                    {
                        "desc": "Synthesize findings into a mental model",
                        "skill": "architect",
                        "type": "synthesis",
                    },
                ],
                "Surgical Correction": [
                    {
                        "desc": "Isolate the exact line of failure",
                        "skill": "troubleshooter",
                        "type": "isolation",
                    },
                    {
                        "desc": "Apply the minimal corrective edit",
                        "skill": "developer",
                        "type": "mutation",
                    },
                    {
                        "desc": "Verify fix with targeted tests",
                        "skill": "qa_lead",
                        "type": "verification",
                    },
                ],
                "Feature Synthesis": [
                    {
                        "desc": "Investigate current implementation and requirements",
                        "skill": "researcher",
                        "type": "discovery",
                    },
                    {
                        "desc": "Design the architectural approach and interface",
                        "skill": "architect",
                        "type": "analysis",
                    },
                    {
                        "desc": "Create a test suite to define success criteria",
                        "skill": "test-engineer",
                        "type": "planning",
                    },
                    {
                        "desc": "Prove the current baseline fails the new tests (Dry-Run)",
                        "skill": "test-engineer",
                        "type": "verification",
                    },
                    {
                        "desc": "Implement the feature logic",
                        "skill": "developer",
                        "type": "mutation",
                    },
                    {
                        "desc": "Verify the implementation via the test suite",
                        "skill": "test-engineer",
                        "type": "verification",
                    },
                    {
                        "desc": "Perform final code review and quality audit",
                        "skill": "reviewer",
                        "type": "verification",
                    },
                ],
                "Structural Evolution": [
                    {
                        "desc": "Map current structural dependencies",
                        "skill": "architect",
                        "type": "discovery",
                    },
                    {
                        "desc": "Execute systemic refactoring",
                        "skill": "developer",
                        "type": "mutation",
                    },
                    {
                        "desc": "Perform regression audit",
                        "skill": "reviewer",
                        "type": "verification",
                    },
                ],
                "Adversarial Review": [
                    {
                        "desc": "Scan for known vulnerability patterns",
                        "skill": "security_auditor",
                        "type": "discovery",
                    },
                    {
                        "desc": "Attempt exploit vector verification",
                        "skill": "security_auditor",
                        "type": "analysis",
                    },
                    {
                        "desc": "Document flaws and remediation",
                        "skill": "reviewer",
                        "type": "synthesis",
                    },
                ],
                "Knowledge Sync": [
                    {
                        "desc": "Identify discrepancies between code and docs",
                        "skill": "doc_expert",
                        "type": "analysis",
                    },
                    {
                        "desc": "Update documentation to reflect reality",
                        "skill": "doc_expert",
                        "type": "mutation",
                    },
                    {
                        "desc": "Verify doc accuracy",
                        "skill": "reviewer",
                        "type": "verification",
                    },
                ],
            }

            sequence = templates.get(
                intent,
                [
                    {
                        "desc": "Analyze request",
                        "skill": "general-purpose",
                        "type": "analysis",
                    },
                    {
                        "desc": "Execute task",
                        "skill": "general-purpose",
                        "type": "mutation",
                    },
                    {
                        "desc": "Verify result",
                        "skill": "general-purpose",
                        "type": "verification",
                    },
                ],
            )

        # Enrich the sequence with the specific job contract details for JobStateManager compatibility
        enriched_jobs = []
        for i, job in enumerate(sequence):
            # Handle both LLM format (description) and template format (desc)
            desc = job.get("description") or job.get("desc")
            skill = job.get("skill")
            job_type = job.get("type")
            v_criteria = job.get("verification_criteria") or (
                "Standard verification for " + str(job_type)
            )

            job_id = f"{intent.lower().replace(' ', '_')}_{i + 1}"
            enriched_jobs.append(
                {
                    "job_id": job_id,
                    "description": desc,
                    "assigned_skill": skill,
                    "job_type": job_type,
                    "status": "pending",
                    "dependencies": [
                        f"{intent.lower().replace(' ', '_')}_{j + 1}" for j in range(i)
                    ],
                    "verification_criteria": v_criteria,
                }
            )

        return enriched_jobs

    def create_correction_job(
        self, original_job: dict[str, Any], failure_logs: str
    ) -> dict[str, Any]:
        """
        Dynamically creates a correction job to address a specific failure.
        """
        correction_id = f"corr_{original_job['job_id']}_{int(time.time())}"
        return {
            "job_id": correction_id,
            "description": f"Correction for {original_job['job_id']}: {failure_logs[:200]}...",
            "assigned_skill": "developer",  # Default to developer for corrections
            "job_type": "mutation",
            "status": "pending",
            "dependencies": [],  # Correction jobs are usually immediate
            "verification_criteria": f"Fix the failure reported in logs: {failure_logs}",
        }


if __name__ == "__main__":
    decomposer = TaskDecomposer()
    # Test a Surgical Correction contract
    contract = {
        "intent": "Surgical Correction",
        "risk_profile": "Low-Med",
        "original_prompt": "Fix the race condition in the auth module",
    }
    print(
        f"Decomposed Jobs for {contract['intent']}:\n{json.dumps(decomposer.decompose(contract), indent=2)}"
    )
