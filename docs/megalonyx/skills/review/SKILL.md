# Skill: Review

## 1. Skill Identity
The **Review** skill provides professional-grade code audits. It focuses on correctness, security, quality, and performance, ensuring that all contributions meet project standards and are free of critical flaws.

## 2. Trigger Logic
This skill is triggered by:
- **Pull Request Audits**: Reviewing changes in a PR.
- **File Audits**: Analyzing specific files or directories for quality.
- **Security Scans**: Looking for vulnerabilities in a specific piece of code.
- **Keywords**: `review`, `audit`, `code review`, `security check`, `performance audit`.

## 3. Operational Workflow
1. **Scope Analysis**: Determines the review target (PR, URL, or File) and fetches the necessary context using `git diff` or `qwen review` tools.
2. **Rule Loading**: Integrates project-specific guidelines (e.g., from `QWEN.md`) into the review context.
3. **Deterministic Audit**: Executes linters and type-checkers; these tool-based diagnostics are treated as "Confirmed Issues."
4. **Parallel Multi-Dimensional Review**: Dispatches specialized agents to analyze the code across multiple dimensions:
    - Correctness & Security
    - Quality & Performance
    - Test Sufficiency
    - General Undirected Audit
5. **Synthesis & Reporting**: Consolidates findings, removes redundant noise, and generates the final report.

## 4. Output Contract
The Review skill produces a structured audit report:
- **SUMMARY**: A brief overview of the review results.
- **CRITICAL FINDINGS**: A list formatted as `[File:Line] | [Source] | [Issue] | [Impact] | [Suggested Fix]`.
- **SUGGESTIONS**: Non-critical improvements formatted as `[File:Line] | [Issue] | [Suggested Fix]`.
- **BUILD/TEST STATUS**: `[Passed/Failed]`
- **CONFIDENCE**: A numerical value `(0.0 - 1.0)`.
- **VERDICT**: `[APPROVED / REJECTED]`

## 5. Symmetry Link
Original Configuration: [`config/skills/review/SKILL.md`](../../../config/skills/review/SKILL.md)
