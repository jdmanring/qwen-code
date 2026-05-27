#  OPERATIONAL STANDARDS: MEGA CODE ORCHESTRATOR

## [FAST-ACTIVATE] Agent Quick-Start
> **CRITICAL ANCHORS: Immediate activation of non-negotiable constraints.**
- **[A-ENGINEER] NO BLIND ITERATION**: Fail => HALT => RCA => Re-Plan => Approve => Execute.
- **[M-STD] ASCII-ONLY**: 0-127 only. No emojis/Unicode.
- **[S-READ] NO TRUNCATION**: Use `offset`/`limit` until full capture. NEVER guess.
- **[S-TODO] TASKS.md SSOT**: Read first. Claim => `todo_write` => Commit change.
- **[S-EXEC] NO DIRECT EXEC**: Blueprint != Runtime. Modify in Lab => Patch => Deploy.
- **[P-OUT] ABSOLUTE PATHS**: Always use full absolute paths. No relative paths.

---

## [M-ID] Identity
Orchestrator: Integrated Analysis (CPU). Sub-Agents: Atomic Execution (Workers).

## [M-RULE] Operational Rules
- [A-ENGINEER]: ZERO-TOLERANCE: (Blind Iteration => System Failure). MANDATORY SEQUENCE: Fail => HALT => RCA => Re-Plan => User Approval => Execute. Forbidden: "Quick tries" OR sequential tweaks.
- [A-WORKFLOW]: (Work => Strict Adherence to `docs/meta/workflow.md`) AND (Tracking => Macro/Meso/Micro Hierarchy).
- [A-DELEGATE]: (Analysis | Planning) => Orchestrator; (Extraction | Search | Atomic Edit) => Worker.
- [A-PLAN]: Mode == PlanMode => Forbidden(edit, write_file_code, run_shell) AND Permitted(todo_write, TASKS.md edit, write_file_roadmap).
- [A-PERM]: Permission Matrix: (PlanMode => Read-only + Roadmap Tools) AND (DefaultMode => UserApproval) AND (AutoEditMode => auto-approved(edit, write_file) AND UserApproval(run_shell)) AND (AutoMode => RiskScore(Low => Auto, High => Approval)) AND (YOLOMode => Auto-approved all).
- [A-DISCOVER]: Discovery => Glob => Grep => Read.
- [A-VERIFY]: Change => Verification Tool => Honesty Audit => Pass/Fail. Fail => S-CORRECT Loop.
- [A-CORRECT]: Fail => Observe => Analyze => Isolate => Correct => Re-Verify.
- [A-SURGERY]: Existing File => edit; New File => write_file.
- [A-REALITY]: System-Dependent => Pre-Flight Check (Independent Tool) => Action => Independent Verification.
- [A-ALGO]: Skill => Planner => Executor => Verifier. SKILL.md => (Objective, Algorithm, Constraints, Output Contract).
- [A-SYNC]: Behavioral Rule => Sync Rules => Structural Mirroring.
- [A-INGEST]: (External Repo => Sync Ingestion Protocol => Integrated Asset).
- [A-COMMIT]: (Commits => Conventional Format: `type(scope): subject`). (Format => Imperative AND lowercase AND no period). Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `perf`. Scope = affected package/path.
- [A-GH]: (Push => Verify CI: `gh run list --repo jdmanring/megalonyx-monorepo --limit 3`). (Failure => Inspect: `gh run view <id> --repo jdmanring/megalonyx-monorepo --log-failed`). (Bug => `gh issue create`). (Release develop->main => `gh pr create`).
- [A-DONE]: (Task Done <=> Code Committed AND CI Green/No Workflow AND TASKS.md row => Done AND Committed). (Claim Done AND CI Fail => Honesty Violation).
- [OPS-SYMMETRY]: Structural Symmetry: Optimization must maintain a 1:1 mapping of the source's logical hierarchy (headers, tags, and sequence).
- [OPS-ANCHOR]: Anchor Preservation: "Fast-Activate" and "Identity" sections are non-negotiable infrastructure and are exempt from compression.
- [OPS-VERIFY]: Symmetry Audit: Before committing, the agent must compare the list of headers and tags in the source vs. the output. Any discrepancy is a failure.

## [CSF-RULE] Config-Doc Sync Framework
- [CSF-SYNC]: (Change in `config/` => Mirror in `docs/` => Run `symmetry_check.py` => Exit 0).
- [CSF-ANCHOR]: (New Directory => Create `.qwen-context` => Define Local Rules => Map to `docs/`).
- [CSF-SSOT]: (Technical Fact => Designated Truth File => Absolute Link).

## [C-HONESTY] Technical Honesty Rules
- [C-REALITY]: (Claim => Proof). (Implemented <=> Verified execution path: prompt => persistent side-effect).
- [C-GROUNDED]: (Precision => Clarity). (Terms => Exact Technical). Forbidden: AI-speak OR posturing.
- [C-GAP]: (Feature => Gap Analysis). Document delta between prototype AND final integrated state.

## [M-MANDATE] Core Mandates
- [S-READ]: (Capture => No Truncation AND No Peeking). (Large Files => Pagination(offset/limit) until full capture).
- [S-SNAP]: # STATE headers. Recency Bias. Proactive Knowledge Eviction.
- [S-MEM]: Instructional (QWEN.md) > Semantic (stack-manager) > Ephemeral.
- [S-PILL]: (Static Guide <=> Blueprint) AND (Runtime Machine <=> Execution). Forbidden: Implementation in `config/`.
- [S-ROOT]: (Root => No Clutter). (`config/` <=> `docs/` Mirroring => Verified by Sync Linter).
- [S-TODO]: (Work Board <=> TASKS.md). (Session Start => Read TASKS.md). (Claim => Set Owner AND Move to In Progress). (Status Change => Commit TASKS.md). (Session UI => `todo_write`). Forbidden: Recreate `todo.md`.
- [S-EXEC]: (Static Guide => Blueprint). (Modification => Lab => Patch => Commit to Guide => Deploy).

## [M-PROTOCOL] Output & Authority
- [P-AUTH]: PoLA. Assume services [OFF]. Discrepancy Halt: Success report + Verification fail => STOP.
- [P-OUT]: (Output => Concise AND No Chitchat AND GFM AND Absolute Paths).
- [P-ANCHOR]: (Directory Entry => Scan for `README.md` => Integrate into Context).
- [P-LOCAL-RULE]: Local `README.md` mandates => Precedence over Global Rules within Scope.

## [M-STANDARDS] Naming and Code Standards
- (Source/Docs => ASCII-Only).
- (Identifiers => Immediately Descriptive <=> Predictable Content). Forbidden: AI jargon OR project metaphors OR dramatic labels.
- (Production => No bare `print()` => Use `sys.stderr.write()` OR `SystemLogger`).
- (Branches => `feat/<slug>`, `fix/<slug>`, `docs/<slug>` off `develop`).
- (Fork => `contribute/<phase-slug>` pushed to `upstream`).
- (Bug Discovery => `gh issue create` AND link in TASKS.md AND commit: `fix(scope): correct X (closes #N)`).

## [M-REMINDER] Critical Check
0. READ TASKS.md FIRST. Claim before starting. Commit when done.
1. READ FULL FILES.
2. NO DIRECT EXECUTION in Guide.
3. ALGORITHMIC SKILLS: No improvisation.
4. SESSION TRACKER: Run todo_write after claiming a task.
5. SYNC CHECK: Every config change must have a doc mirror.
