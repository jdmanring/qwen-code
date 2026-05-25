# Skill: Docs-Audit-And-Refresh

## Skill Identity
**Docs-Audit-And-Refresh** is a comprehensive audit skill used to review the `docs/` directory against the current codebase. Its primary purpose is to find missing, incorrect, or stale documentation and refresh the affected pages to ensure total accuracy.

## Trigger Logic
This skill is triggered when the user asks to:
- Review documentation coverage.
- Find outdated or stale documentation.
- Compare the existing docs with the current repository state.
- Fix "documentation drift" across features, settings, tools, or integrations.

## Operational Workflow
1. **Build a Current-State Inventory**: Inspect repository areas defining user-facing or developer-facing behavior (code, tests, schemas, package surfaces).
2. **Compare Implementation against `docs/`**: Identify three classes of issues: missing documentation, incorrect documentation (contradicts code), or stale documentation (outdated names/paths).
3. **Prioritize by Reader Impact**: Address high-cost issues first (e.g., broken onboarding, wrong settings, missing core feature docs).
4. **Refresh the Docs**: Update the smallest correct set of pages under `docs/`. This includes editing existing pages, adding new pages for durable gaps, and updating `_meta.ts` for discoverability.
5. **Validate the Refresh**: Search for old terminology, check neighboring pages for conflicts, and verify examples against the code.

## Output Contract
The deliverable for this skill is:
- **Docs Refresh**: A set of edits under `docs/` that make the repository more accurate and complete.
- **Summary**: A report of the audited surfaces and the specific pages updated.

## Mirror Link
Original configuration: [`config/skills/docs-audit-and-refresh/SKILL.md`](../../config/skills/docs-audit-and-refresh/SKILL.md)
