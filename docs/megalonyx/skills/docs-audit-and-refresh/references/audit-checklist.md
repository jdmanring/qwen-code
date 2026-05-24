# Documentation Audit Checklist Documentation

## Purpose
This file provides a standardized checklist for performing repository-wide audits of existing documentation to identify gaps, inaccuracies, and "drift" between the code and the docs.

## Logic & Structure
The checklist is organized by:
- **High-signal surfaces**: Key areas of the codebase (CLI, Core, SDKs, IDE extensions) that are most likely to impact user-facing documentation.
- **Gap detection prompts**: Specific questions to ask when comparing code to `docs/` (e.g., "Does a feature exist in code but not in docs?").
- **Common drift patterns**: Examples of how documentation typically becomes stale (renamed settings, updated auth flows).
- **Output standard**: Guidelines for how to record audit findings (preferring precise edits over broad rewrites).

## Usage
- **Technical Writers/Developers**: Use this checklist during scheduled documentation reviews or before major releases to ensure the user manual remains accurate.
- **AI Agents**: Use these prompts to systematically scan the codebase and suggest specific documentation updates.

## Original File
[config/skills/docs-audit-and-refresh/references/audit-checklist.md](../../config/skills/docs-audit-and-refresh/references/audit-checklist.md)
