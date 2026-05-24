# Skill: Security Auditor

## 1. Skill Identity
The **Security Auditor** is a deterministic protocol designed for systematic security auditing, vulnerability identification, and risk assessment. It transforms the often-subjective process of security review into a rigorous, repeatable sequence of analysis to ensure that software entry points are secure and that common vulnerability patterns are identified and mitigated.

## 2. Trigger Logic
This skill is activated when the system detects requests for:
- Security audits or vulnerability scans.
- Threat modeling of a specific feature or endpoint.
- Review of code for OWASP/CWE compliance.
- Identification of potential attack vectors in a given codebase.
- Verification of sanitization and validation logic for user-provided input.

## 3. Operational Workflow
The Security Auditor operates through a five-stage deterministic pipeline:
1. **Attack Surface Mapping**: Utilizes `grep` and `glob` to identify all external entry points, including API endpoints, user input fields, file upload handlers, and environment variable reads.
2. **Pattern Scanning**: Scans the identified surface for known dangerous patterns (e.g., `eval()`, `exec()`, `innerHTML`, raw SQL concatenation) and maps these findings to specific CWE/OWASP categories.
3. **Data Flow Analysis**: Traces the lifecycle of untrusted input from the entry point to the "sink" (the point of execution or storage) to determine if necessary sanitization or validation is missing.
4. **Logic Audit**: Performs a deep review of authentication and authorization mechanisms to identify potential bypasses, race conditions, or privilege escalation flaws.
5. **Remediation Planning**: For every confirmed vulnerability, the auditor defines a precise, secure remediation step to resolve the issue.

## 4. Output Contract
The output of a Security Audit must adhere to the following schema:
- **SECURITY VERDICT**: A clear status of `[SECURE / VULNERABLE / UNCERTAIN]`.
- **VULNERABILITY LIST**: A detailed breakdown for each finding:
    - **Vulnerability**: [Name] | **Severity**: [Critical/High/Medium/Low] | **CWE**: [ID] | **Line**: [X]
    - **Impact**: Description of the consequences if the vulnerability is exploited.
    - **Remediation**: Specific instructions on how to fix the vulnerability.
- **ATTACK SURFACE ANALYSIS**: A high-level summary of the most exposed areas of the system.
- **CONFIDENCE**: A score from `0.0` to `1.0` indicating the certainty of the findings.

## 5. Symmetry Link
**Original Configuration**: [`../../../config/skills/security_auditor/SKILL.md`](../../../config/skills/security_auditor/SKILL.md)
