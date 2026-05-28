---
name: create-issue
description: Transforms a user's idea or bug report into a professional GitHub issue.
category: qc
---

# Create Issue Command

## Command Identity
The `create-issue` command transforms a user's high-level idea or bug report into a professional, well-documented GitHub issue.

## Operational Workflow

The system follows this process:

1.  **Requirement Analysis**:
    - Analyzes the user's input to categorize the request as either a `feature request` or a `bug report`.
2.  **Contextual Investigation**:
    - Searches the codebase to understand the current implementation and identify relevant files or existing behaviors.
3.  **Drafting (Bilingual)**:
    - Creates a markdown draft based on project templates (`feature_request.yml` or `bug_report.yml`).
    - **Language Requirement**: The body is written in English first, followed by a Chinese translation wrapped in a `<details>` tag. The title remains English-only.
    - Focuses on the "what" and "why" from the user's perspective, avoiding internal implementation jargon.
4.  **Iterative Review**:
    - Presents the draft to the user for feedback.
    - Refines the content until the user provides explicit approval.
5.  **Submission**:
    - Uses `gh issue create` to submit the issue.
    - Applies mandatory labels:
        - Feature: `type/feature-request`, `status/needs-triage`
        - Bug: `type/bug`, `status/needs-triage`

## Input/Output

- **Input**: A brief description of a feature or bug provided by the user.
- **Output**:
    - A submitted GitHub issue.
    - The URL of the created issue.

## Symmetry Link
[View Configuration](../../config/commands/qc/create-issue.md)
