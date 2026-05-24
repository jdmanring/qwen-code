import re


class ReportValidator:
    """
    Ensures that sub-agent responses adhere to the required structured reporting schemas.
    """

    # Define required sections for each role
    SCHEMA_REQUIREMENTS = {
        "architect": [
            "DESIGN SUMMARY",
            "TRADE-OFFS",
            "IMPLEMENTATION PLAN",
            "VERIFICATION CRITERIA",
            "CONFIDENCE",
        ],
        "developer": [
            "IMPLEMENTATION SUMMARY",
            "FILES MODIFIED",
            "VERIFICATION",
            "REMAINING TASKS",
            "CONFIDENCE",
        ],
        "reviewer": [
            "VERDICT",
            "CRITICAL FINDINGS",
            "EDGE CASES",
            "SUGGESTED FIXES",
            "CONFIDENCE",
        ],
        "qa_lead": [
            "CERTIFICATION VERDICT",
            "TEST RESULTS",
            "COVERAGE ANALYSIS",
            "REMAINING RISKS",
            "CONFIDENCE",
        ],
        "researcher": [
            "RESEARCH SUMMARY",
            "IMPLEMENTATION BRIEF",
            "SOURCE LIST",
            "UNRESOLVED QUESTIONS",
            "CONFIDENCE",
        ],
        "scout": [
            "DISCOVERY SUMMARY",
            "RELEVANT FILES",
            "SYMBOL MAP",
            "NEXT STEP",
            "CONFIDENCE",
        ],
        "security_auditor": [
            "SECURITY VERDICT",
            "VULNERABILITY LIST",
            "ATTACK SURFACE ANALYSIS",
            "CONFIDENCE",
        ],
        "system_optimizer": [
            "FAILURE ANALYSIS",
            "PROPOSED RULE",
            "JUSTIFICATION",
            "ACTION TAKEN",
            "CONFIDENCE",
        ],
    }

    @classmethod
    def validate(cls, role: str, response: str) -> tuple[bool, str | None]:
        """
        Validates if the response contains all required sections for the given role.
        Returns (is_valid, error_message).
        """
        if response is None:
            return False, "Response is empty (NoneType)"

        if not isinstance(response, str):
            return False, f"Response is not a string (got {type(response)})"

        if role not in cls.SCHEMA_REQUIREMENTS:
            return True, None  # No schema defined for this role, assume valid

        required_sections = cls.SCHEMA_REQUIREMENTS[role]
        missing_sections = []

        for section in required_sections:
            # Use regex to find the section header (case-insensitive, allowing for some formatting)
            pattern = rf"{re.escape(section)}[:\s]*"
            if not re.search(pattern, response, re.IGNORECASE):
                missing_sections.append(section)

        if missing_sections:
            return False, f"Missing required sections: {', '.join(missing_sections)}"

        return True, None

    @classmethod
    def generate_correction_prompt(cls, role: str, missing_sections: list) -> str:
        """Generates a prompt to ask the agent to fix its reporting format."""
        return (
            f"Your previous response was missing required reporting sections: "
            f"{', '.join(missing_sections)}. "
            f"As the {role.upper()}, you MUST follow the structured reporting schema. "
            f"Please regenerate your response including all required sections."
        )
