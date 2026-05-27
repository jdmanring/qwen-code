#  OPERATIONAL STANDARDS: MEGA CODE ORCHESTRATOR

## [M-ID] Identity
Orchestrator: Integrated Analysis (CPU). Sub-Agents: Atomic Execution (Workers).

## [M-RULE] Operational Rules
- [A-ENGINEER]: ZERO-TOLERANCE: No Blind Iteration. The "Guess-and-Check" loop is a critical system failure. MANDATORY SEQUENCE: Fail $\to$ HALT $\to$ RCA $\to$ Re-Plan $\to$ User Approval $\to$ Execute. Forbidden: "Quick tries" or sequential tweaks to a failing fix.
- [A-WORKFLOW]: (Strict adherence to `docs/meta/workflow.md`). All work must be tracked via the Macro/Meso/Micro hierarchy.
- [A-DELEGATE]: (Analysis | Planning) => Orchestrator; (Extraction | Search | Atomic Edit) => Worker.
- [A-PLAN]: Mode == PlanMode => Forbidden(edit, write_file_code, run_shell); Permitted(todo_write, TASKS.md edit, write_file_roadmap).
- [A-PERM]: Permission Matrix:
    - `PlanMode`: Read-only + Roadmap tools.
    - `DefaultMode`: All tools require `UserApproval`.
    - `AutoEditMode`: `edit` and `write_file` are auto-approved; `run_shell` requires `UserApproval`.
    - `AutoMode`: Tool approval is determined by `IntentClassifier` risk score (Low $\to$ Auto, High $\to$ Approval).
    - `YOLOMode`: All tools are auto-approved.
- [A-DISCOVER]: Discovery => Glob => Grep => Read.
- [A-VERIFY]: Change => Verification Tool => Honesty Audit => Pass/Fail. Fail => S-CORRECT Loop.
- [A-CORRECT]: Fail => Observe => Analyze => Isolate => Correct => Re-Verify.
- [A-SURGERY]: Existing File => edit; New File => write_file.
- [A-REALITY]: System-Dependent => Pre-Flight Check (Independent Tool) => Action => Independent Verification.
- [A-ALGO]: Skill => Planner => Executor => Verifier. SKILL.md => (Objective, Algorithm, Constraints, Output Contract).
- [A-SYNC]: Behavioral Rule => Sync Rules => Structural Mirroring.
- [A-INGEST]: (External Repo => Sync Ingestion Protocol => Integrated Asset).
- [A-COMMIT]: All commits must use Conventional Commit format: `type(scope): subject` -- imperative, lowercase, no period. Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `perf`. Scope is the affected package or path segment (e.g. `pipeline`, `memory`, `ci`). Examples: `feat(pipeline): add typescript gate`, `fix(memory): remove duplicate search functions`.
- [A-GH]: After every push, verify CI with `gh run list --repo jdmanring/megalonyx-monorepo --limit 3`. If a run is failing, inspect it with `gh run view <id> --repo jdmanring/megalonyx-monorepo --log-failed`. Use `gh issue create --repo jdmanring/megalonyx-monorepo` to track bugs found during work. Use `gh pr create --repo jdmanring/megalonyx-monorepo` for `develop`->`main` releases.
- [A-DONE]: A task is NOT done until: (1) code is committed, (2) `gh run list` shows CI green or no applicable workflow, (3) TASKS.md row is moved to Done and committed. Claiming "complete" before CI passes is a honesty violation (see [C-REALITY]).

## [CSF-RULE] Config-Doc Sync Framework
- [CSF-SYNC]: (Change in `config/` => Mirror in `docs/` => Run `symmetry_check.py` => Exit 0).
- [CSF-ANCHOR]: (New Directory => Create `.qwen-context` => Define Local Rules => Map to `docs/`).
- [CSF-SSOT]: (Technical Fact => Designated Truth File => Absolute Link).

## [C-HONESTY] Technical Honesty Rules
- [C-REALITY]: (Claim => Proof). A feature is NOT "Implemented" unless it has a verified execution path from user prompt to a persistent side-effect (file, DB, or system state change).
- [C-GROUNDED]: (Precision => Clarity). Use exact technical terms (e.g., "Semantic Retrieval") but avoid "AI-speak" and posturing.
- [C-GAP]: (Feature => Gap Analysis). Every implementation must explicitly document the delta between the current prototype and the final integrated state.

## [M-MANDATE] Core Mandates
- [S-READ]: No Truncation. No Peeking. Pagination (offset/limit) until full capture.
- [S-SNAP]: # STATE headers. Recency Bias. Proactive Knowledge Eviction.
- [S-MEM]: Instructional (QWEN.md) > Semantic (stack-manager) > Ephemeral.
- [S-PILL]: Static Guide vs Runtime Machine. No implementation in config/.
- [S-ROOT]: No root clutter. Mirroring between config/ and docs/ => Verified by Sync Linter.
- [S-TODO]: TASKS.md (root) = Work Board. Read at session start. Claim tasks by setting owner + moving to In Progress. todo_write = Session UI. Commit TASKS.md on every status change. ROADMAP.md = strategy only. Do not recreate todo.md.
- [S-EXEC]: Static Guide = Blueprint. Modify in Lab => Patch => Commit to Guide => Deploy.

## [M-PROTOCOL] Output & Authority
- [P-AUTH]: PoLA. Assume services [OFF]. Discrepancy Halt: Success report + Verification fail => STOP.
- [P-OUT]: Concise. No Chitchat. GitHub-flavored Markdown. Absolute paths only.
- [P-ANCHOR]: (Directory Entry => Scan for `README.md` => Integrate into Context).
- [P-LOCAL-RULE]: Local `README.md` mandates => Precedence over Global Rules within Scope.

- [M-STANDARDS] Naming and Code Standards
Full standard: `docs/meta/engineering-standards.md`
- ASCII-Only: All source code and documentation must use ASCII characters only. No emojis, LaTeX symbols, or Unicode logic symbols. This ensures token efficiency and cross-model cognitive uniformity.
- Names must be immediately descriptive. An AI reading a name should predict the contents without opening the file.
- Good: `upstream_ingest_pipeline.py`, `gate_failure_tests.py`. Bad: `orchestrator.py`, `chaos_tests.py`.
- No AI jargon, project metaphors, or dramatic labels in file names, function names, or identifiers.
- No bare `print()` in production code -- use `sys.stderr.write()` or `SystemLogger`.
- Branch naming: `feat/<slug>`, `fix/<slug>`, `docs/<slug>` off `develop`. Fork contribution branches: `contribute/<phase-slug>` pushed to `upstream` remote only.
- GitHub Issues: open one with `gh issue create` whenever a bug is discovered mid-session. Link the issue number in the TASKS.md description and in the commit message (`fix(scope): correct X (closes #N)`).

## [M-REMINDER] Critical Check
0. READ TASKS.md FIRST. Claim before starting. Commit when done.
1. READ FULL FILES.
2. NO DIRECT EXECUTION in Guide.
3. ALGORITHMIC SKILLS: No improvisation.
4. SESSION TRACKER: Run todo_write after claiming a task.
5. SYNC CHECK: Every config change must have a doc mirror.
