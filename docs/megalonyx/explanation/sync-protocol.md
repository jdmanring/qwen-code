# Runtime-to-Source Synchronization Protocol

To maintain a high-performance, professionalized agent environment, the `qwen_code_stack` employs a specific synchronization workflow between the active runtime and the source definitions.

## 1. The Synchronization Philosophy

We treat the **Runtime (`~/.qwen`)** as our "Live Laboratory" and the **Source Repository (`/Projects/qwen_code_stack`)** as our "Authoritative Blueprint."

- **Runtime $\rightarrow$ Source**: When a prompt, skill, or configuration is refined and stabilized during active use in the runtime, it must be back-ported to the source repository.
- **Source $\rightarrow$ Runtime**: New features or systemic updates developed in the source are deployed to the runtime via the installation or update process.

This prevents "configuration drift" and ensures that the professional standards developed during real-world use are captured and reproducible.

---

## 2. The Synchronization Workflow

### Phase A: Live Iteration (Runtime)
1. **Hypothesis**: Identify a prompt friction point (e.g., "empty nest" errors, instruction conflict).
2. **Experiment**: Modify the active agent configurations in `~/.qwen/QWEN.md` or `~/.qwen/skills/`.
3. **Validation**: Test the change across multiple complex tasks.
4. **Stabilization**: Once the behavior is consistent and superior, mark the configuration as "Gold Standard."

### Phase B: Back-porting (Source)
1. **Mirror Configuration**: Copy the stabilized `~/.qwen` files into the appropriate project-level overrides or examples (e.g., `QWEN.md` in the root or `config/settings.EXAMPLE.json`).
2. **Update Documentation**: Reflect the change in the `/docs` folder (e.g., update `prompt-strategy.md` or `configuration.md`).
3. **Update Installation**: If the change should be the default for all users, update `install.sh` or the bundled config files.

### Phase C: Propagation (New/Other Installs)
1. **Re-install/Update**: Run the updated `install.sh`.
2. **Verify**: Ensure the new installation exhibits the professionalized behavior.

---

## 3. Key Synchronization Points

| Artifact | Runtime Path | Source Path | Sync Direction |
| :--- | :--- | :--- | :---: |
| **System Prompt** | `~/.qwen/QWEN.md` | `/qwen_code_stack/QWEN.md` | $\leftrightarrow$ |
| **Global Settings** | `~/.qwen/settings.json` | `/qwen_code_stack/config/settings.EXAMPLE.json` | $\rightarrow$ |
| **Global Skills** | `~/.qwen/skills/` | `/qwen_code_stack/docs/how-to/creating-skills.md` (as examples) | $\rightarrow$ |
| **Env Variables** | `~/.qwen/.env` | `/qwen_code_stack/config/.env.EXAMPLE` | $\rightarrow$ |

---

## 4. Compliance Checklist for AI Agents

When performing maintenance on this stack, the agent must:
- [ ] **Check for Drift**: Compare `~/.qwen/QWEN.md` with the project root `QWEN.md`.
- [ ] **Document the Change**: If a runtime change is made, create a corresponding update in `docs/explanation/`.
- [ ] **Update the Blueprint**: Ensure the source repository reflects the current "best-known" configuration.
