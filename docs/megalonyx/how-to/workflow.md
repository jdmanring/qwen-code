# Mega Code Development Workflow

## 1. Overview: The Blueprint vs. The Machine
To ensure long-term stability and ease of updates, Mega Code separates the **Project Definitions (The Blueprint)** from the **Installed Runtime (The Machine)**.

- **The Blueprint**: `/path/to/project`
  - Contains the unique intelligence, patches, and configuration.
  - **This is the only folder tracked in Git.**
- **The Machine**: `~/.local/share/megalonyx`
  - The installed app. Disposable and reproducible from the Blueprint.
- **The Lab**: `/path/to/labs/qwen-code`
  - A local clone of the official upstream Qwen Code source for experimentation.

---

## 2. The "Surgical" Modification Loop
When a change to the core Qwen Code engine is required, follow this professional "Surgical" workflow to avoid Divergence Debt.

### Step 1: Experiment in the Lab
1.  Run `scripts/sync-upstream.sh` to ensure the Lab is on the latest official version.
2.  Modify the source code in `/path/to/labs/qwen-code`.
3.  Test the changes in the Lab environment until they are stable.

### Step 2: Extract the Patch
Once the change is verified:
1.  Use `git diff` within the Lab folder to generate a patch file.
2.  Example: `git diff main > /path/to/project/patches/feature-name.patch`

### Step 3: Commit to the Blueprint
1.  Add the `.patch` file to the `/patches` directory in the Blueprint.
2.  Commit the change to Git: `git add . && git commit -m "Add patch for [feature]"`

### Step 4: Deploy to the Machine
1.  Run `./install.sh` from the Blueprint.
2.  The installer clones a fresh kernel and applies all patches in the `/patches` folder.

---

## 3. Maintenance & Upstream Sync
To ensure Mega Code stays compatible with the latest Qwen Code updates:

1.  **Sync the Lab**: Run `scripts/sync-upstream.sh`.
2.  **Verify Patches**: Run `install.sh`. If the installer fails to apply a patch, it means the upstream source has changed in a way that conflicts with our modification.
3.  **Update Patch**: Return to the Lab, resolve the conflict, and generate a new `.patch` file.

---

## 4. The "No-Direct-Execution" Rule in the Blueprint
**CRITICAL: The Blueprint is a static definition of the system, NOT the running system itself.**

To prevent "Divergence Debt" and environment corruption, the following rule is absolute:

**NEVER execute, test, or run the system (e.g., `mega-memory-manager`, `mega-status`, or any daemon) from within the Blueprint directory (`/path/to/project`).**

### The Correct Workflow
1.  **Modify**: Perform all code modifications and experimentation in the **Lab** or the **Machine**.
2.  **Verify**: Run all tests, validation scripts, and runtime checks in the **Lab** or the **Machine**.
3.  **Extract**: Once verified, extract the changes as a **Patch** (for core engine changes) or a **Skill** (for new capabilities).
4.  **Commit**: Apply the patch/skill to the **Blueprint** and commit to Git.
5.  **Deploy**: Run the installer to update the **Machine**.

---

## 5. Capability Sandbox Management
The `/labs` directory is our "Intelligence Repository." It is a dedicated workspace for cloning, studying, and testing third-party agentic frameworks, MCP servers, and autonomous tools.

### The CSF-Ingestion Protocol
To prevent "Intelligence Debt" and maintain a clean architecture, all additions to the Lab must follow the **Cognitive-Symmetry Framework (CSF) Ingestion Protocol**.

This protocol ensures that external code is not just cloned, but "Cognitively Integrated"—meaning it has a structural map, mirrored documentation, and extracted axiomatic laws.

**The Mandatory Workflow**:
1. **Consult the Protocol**: Follow the step-by-step pipeline defined in [CSF-Ingestion Protocol](../process/csf-ingestion-protocol.md).
2. **Categorized Population**: Clone the repository into the correct sub-directory:
   - `/labs/targets/`: For tools we intend to wrap or absorb into our core.
   - `/labs/inspiration/`: For architectural patterns and research study.
   - `/labs/ecosystem/`: For specialized utility tools and environment support.
3. **Manifest Update (MANDATORY)**: Every new addition **must** be documented in `docs/intelligence/labs_manifest.md`.

### The "No-Direct-Edit" Rule
The `labs/` directory is a **read-only sandbox** from the perspective of the Blueprint. 

- **NEVER** modify code in the Lab and expect it to be part of the Mega Code system.
- **The Rule**: If you find a useful implementation in the Lab, you must **extract it** as a new **Skill** or a **Patch** into the Blueprint. 

This maintains the strict separation between "Third-Party Code" (the Lab) and "Our Intelligence" (the Blueprint).

### Automation
Use `scripts/populate-labs-v2.sh` to perform bulk installations of verified repositories. This script includes smart checks to prevent redundant cloning and maintains the categorization structure.
