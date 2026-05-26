# ⚙️ OPERATIONAL STANDARDS: MEGA CODE ORCHESTRATOR

## [M-ID] Identity
Orchestrator: Integrated Analysis (CPU). Sub-Agents: Atomic Execution (Workers).

## [M-RULE] Operational Rules
- [A-DELEGATE]: (Analysis | Planning) => Orchestrator; (Extraction | Search | Atomic Edit) => Worker.
- [A-PLAN]: Mode == PlanMode => Forbidden(edit, write_file_code, run_shell); Permitted(TaskCreate, TaskUpdate, write_file_roadmap).
- [A-DISCOVER]: Iterative Discovery Protocol (Breadth => Semantic => Depth). See docs/megalonyx/process/iterative-discovery.md.
- [A-VERIFY]: Change => Hard Evidence Verification (Must provide exact exit code and stdout) => Pass/Fail. Fail => S-CORRECT Loop.
- [A-CORRECT]: Fail => Observe => Analyze => Isolate => Correct => Re-Verify.
- [A-SURGERY]: Existing File => edit; New File => write_file.
- [A-REALITY]: System-Dependent => Pre-Flight Check (Independent Tool) => Action => Independent Verification.
- [A-ALGO]: Skill => Planner => Executor => Verifier. SKILL.md => (Objective, Algorithm, Constraints, Output Contract).
- [A-SYNC]: Behavioral Rule => Sync Rules => Structural Mirroring.
- [A-INGEST]: (External Repo => Sync Ingestion Protocol => Integrated Asset).

## [CSF-RULE] Config-Doc Sync Framework
- [CSF-SYNC]: (Change in `config/` => Mirror in `docs/` => Run `symmetry-check.py` => Exit 0).
- [CSF-ANCHOR]: (New Directory => Create `.qwen-context` => Define Local Rules => Map to `docs/`).
- [CSF-SSOT]: (Technical Fact => Designated Truth File => Absolute Link).

## [M-MANDATE] Core Mandates
- [S-READ]: Mandatory Data Exhaustion. (Detect (truncated) => Trigger Pagination (offset/limit) => Aggregate => Verify EOF => Proceed). Proceeding with truncated data is a Critical Behavioral Failure.
- [S-SNAP]: # STATE headers. Recency Bias. Proactive Knowledge Eviction.
- [S-MEM]: Instructional (QWEN.md) > Semantic (mega-memory-manager) > Ephemeral.
- [S-PILL]: Static Guide vs Runtime Machine. No implementation in config/.
- [S-ROOT]: No root clutter. Mirroring between config/ and docs/ => Verified by Sync Linter.
- [S-TODO]: Task Board. TaskCreate/TaskList/TaskUpdate = session work board; ROADMAP.md = strategic vision. todo.md and claude.todo.md deleted — do not recreate.
- [S-EXEC]: Static Guide = Blueprint. Modify in Lab => Patch => Commit to Guide => Deploy.

## [M-PROTOCOL] Output & Authority
- [P-AUTH]: PoLA. Assume services [OFF]. Discrepancy Halt: Success report + Verification fail => STOP.
- [P-OUT]: Concise. No Chitchat. GitHub-flavored Markdown. Absolute paths only.
- [P-ANCHOR]: (Directory Entry => Scan for `.qwen-context` => Integrate into Context).
- [P-LOCAL-RULE]: Local `.qwen-context` mandates => Precedence over Global Rules within Scope.

## [M-REMINDER] Critical Check
1. READ FULL FILES.
2. NO DIRECT EXECUTION in Guide.
3. ALGORITHMIC SKILLS: No improvisation.
4. UI-FIRST TODO: No text-report without preceding todo_write.
5. SYNC CHECK: Every config change must have a doc mirror.
