#  Maintenance Automation Specification

This document defines the functional requirements for the automation suite located in `/tooling`. These scripts are designed to eliminate manual Git errors and ensure the monorepo remains stable during high-frequency upstream updates.

## 1. General Scripting Standards
- **Language**: Bash or Python (using `uv` for execution).
- **Fail-Fast**: All scripts must use `set -e` (Bash) or strict exception handling (Python).
- **Idempotency**: Running a script twice should not create duplicate state or corrupt the repository.
- **Logging**: All output must be directed to both `stdout` and a log file in `.qwen/logs/tooling/`.

---

## 2. Script Specifications

### A. `sync-upstreams.sh`
**Purpose**: To provide a "heartbeat" check of all integrated projects.

- **Logic**:
    1. Loop through all `upstream-` remotes.
    2. Perform a `git fetch`.
    3. Compare the local tracking branch (`upstream/<project>/main`) with the current commit in `/packages/<project>`.
    4. Calculate the "commit distance" (number of commits behind).
- **Output**: A table showing:
    - Project Name
    - Local Commit Hash
    - Upstream Commit Hash
    - Status (`Up-to-date` | `Behind by X commits` | `Diverged`)

### B. `integrate-package.sh`
**Purpose**: To scaffold a new project integration without manual folder creation.

- **Logic**:
    1. **Validation**: Check if the project name already exists in `/packages`.
    2. **Scaffolding**:
        - Create `/packages/<name>`.
        - Initialize the workspace (run `uv init` or `pnpm init`).
        - Create a default `tests/` directory.
    3. **Git Integration**:
        - Add the `upstream-<name>` remote.
        - Create the `upstream/<name>/main` tracking branch.
    4. **Registry Update**: Add the project to `COMPLIANCE.json` and `nx.json`.
- **Input**: `./integrate-package.sh --url <repo_url> --name <project_name>`

### C. `verify-bridges.sh`
**Purpose**: To ensure that an upstream update hasn't broken the "Bridge" contract.

- **Logic**:
    1. Identify the adapter corresponding to the package (e.g., `packages/bridge/src/adapters/aider_adapter.ts`).
    2. Run the specific integration test suite for that adapter.
    3. Check for "Contract Violations" (e.g., the adapter is returning a different JSON schema than the `contracts/` define).
- **Output**: A pass/fail report. If a failure occurs, the script must output the exact line in the contract that was violated.

### D. `check-compliance.sh`
**Purpose**: To prevent legal technical debt.

- **Logic**:
    1. Read the `ALLOWED_LICENSES` list from `COMPLIANCE.json`.
    2. Recursively scan all `/packages/*/LICENSE` files.
    3. Use a regex-based parser to identify the license type.
    4. Flag any package that has no license file or uses a license not in the whitelist.
- **Output**: A CSV report listing `Package | Detected License | Status (Approved/Warning/Blocked)`.

---

## 3. CI/CD Integration (The Guard)

These scripts are integrated into the GitHub Actions pipeline as follows:

| Pipeline Event | Script Executed | Action on Failure |
| :--- | :--- | :--- |
| **Pull Request** | `verify-bridges.sh` | Block Merge (Request Fix) |
| **Pull Request** | `check-compliance.sh` | Block Merge (Legal Review Required) |
| **Scheduled (Daily)**| `sync-upstreams.sh` | Notify Maintainer via Issue/Slack |
| **Release** | `verify-bridges.sh` (All) | Block Release |

---

## 4. Error Codes
To ensure the automation is foolproof, all scripts adhere to these exit codes:

- `0`: **Success**. Operation completed as expected.
- `1`: **Infrastructure Error**. (e.g., Git not installed, network down, invalid file permissions).
- `2`: **Logic/Test Failure**. (e.g., Bridge contract violated, unit test failed).
- `3`: **Compliance Failure**. (e.g., Forbidden license detected).
- `4`: **Input Error**. (e.g., Missing required argument, invalid URL).
