# 🔄 Project Workflow & Tracking Standards

This document defines the mandatory tracking and planning hierarchy for the Megalonyx project. To ensure transparency, permanence, and engineering rigor, all work must be tracked across three tiers.

## 1. The Tracking Hierarchy

### Tier 1: Macro (Strategic) — `ROADMAP.md`
- **Purpose:** High-level vision, strategic milestones, and overall system stability status.
- **Usage:** Updated when a major feature is completed or when a system-wide stability or architectural shift occurs.
- **Constraint:** No task-level items. Only strategic targets.

### Tier 2: Meso (Official Record) — `TASKS.md`
- **Purpose:** The official project work board. All bugs, architectural decisions, and feature tasks must be recorded here.
- **Usage:** 
    - Every new bug or feature starts as an entry in `TASKS.md`.
    - Major architectural decisions and their rationales are linked or summarized here.
    - Status updates (Pending $\to$ In Progress $\to$ Completed) are committed to this file.
- **Constraint:** This is the "Source of Truth" for what is being worked on.

### Tier 3: Micro (Execution) — `todo_write` (Agent Session)
- **Purpose:** Turn-by-turn execution steps for the current active session.
- **Usage:** Used by the Orchestrator to break down a `TASKS.md` item into atomic, verifiable steps.
- **Constraint:** Ephemeral. Once the `TASKS.md` item is marked completed, the micro-todos are considered resolved.

---

## 2. Engineering Lifecycle (The Recovery Protocol)

When a bug is discovered or a system failure occurs, the following protocol is mandatory:

1. **Identification:** Record the bug in `TASKS.md`.
2. **Documentation:** Create a bug report in `docs/bugs/` detailing the root cause and impact.
3. **Analysis:** Perform a formal RCA (Root Cause Analysis) and evaluate options.
4. **Planning:** Present a comprehensive fix plan for user approval.
5. **Execution:** Implement the fix using atomic steps tracked via `todo_write`.
6. **Verification:** Certify the fix via tests and regression suites.
7. **Closure:** Mark the task as completed in `TASKS.md` and update `ROADMAP.md` if the stability status has changed.
