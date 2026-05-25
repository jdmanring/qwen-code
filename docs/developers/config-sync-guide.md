# Config Mirroring Guide: Qwen Code

This guide defines the **Config Mirroring Standard** of the Qwen Code project. To prevent undocumented configuration and system behaviors, the project enforces a 1:1 correspondence between configuration files and their documentation mirrors.

---

## 1. The Mirroring Requirement

**Requirement:** Every file located within the `.qwen/config/` directory must have a corresponding documentation file in the `docs/` directory.

The goal is to ensure that the purpose, schema, and impact of any configuration setting are explicitly documented, allowing for immediate understanding without requiring code analysis.

---

## 2. The Mirroring Rule

Mirroring is enforced through a deterministic path-mapping algorithm. To find or create a mirror, follow these steps:

1. **Identify the Relative Path**: Get the path of the config file relative to `.qwen/config/`.
2. **Map to Docs Root**: Apply that relative path to the `docs/` directory.
3. **Append the Extension**: Add `.md` to the end of the filename.

### Examples

| Configuration Path | $\to$ | Documentation Mirror Path |
| :--- | :---: | :--- |
| `.qwen/config/settings.json` | $\to$ | `docs/settings.json.md` |
| `.qwen/config/meta/versions.lock` | $\to$ | `docs/meta/versions.lock.md` |
| `.qwen/config/providers/gemini.json` | $\to$ | `docs/providers/gemini.json.md` |

---

## 3. The Verification Workflow

Config mirroring is a gated requirement in the CI pipeline.

### Step 1: Modify Configuration
When adding a new configuration file or modifying an existing one in `.qwen/config/`, you must update the mirror.

### Step 2: Update the Mirror
Create or update the corresponding `.md` file in `docs/`. The mirror should contain:
- **Purpose**: Why this config exists.
- **Schema**: A description of every key and its expected value/type.
- **Impact**: What happens when these values are changed.

### Step 3: Run the Symmetry Check
Before committing, verify your changes using the symmetry tool:

```bash
python3 tooling/symmetry_check.py
```

- **Success**: "Symmetry Check Passed: All configurations are mirrored in documentation."
- **Failure**: The script will list every config file that is missing its mirror. All violations must be resolved before the commit is accepted.

---

## 4. The Symmetry Map

While `symmetry_check.py` handles the strict config-to-doc mirroring, the project also maintains a broader `docs/meta/symmetry-map.json`.

This map defines high-level relationships between major code directories and their corresponding documentation sections. It is used by auditing tools to ensure that entire modules are documented.

**Example Entry:**
```json
{
  "code_path": "apps/qwen-orchestrator",
  "doc_path": "docs/apps/qwen-orchestrator"
}
```
When adding a new top-level package or app, update the `symmetry-map.json` to link the new code path to its documentation root.

---

## 5. Common Pitfalls

- **Missing `.md` Suffix**: Creating `docs/meta/versions.lock` instead of `docs/meta/versions.lock.md`.
- **Wrong Relative Path**: The directory structure inside `docs/` must exactly match the structure inside `.qwen/config/`.
- **Outdated Mirrors**: The content of the mirror must stay in sync with the schema of the config.

---

## 6. Verification Checklist

- [ ] Does every file in `.qwen/config/` have a mirror in `docs/`?
- [ ] Do the mirrors follow the `path/to/file.ext.md` naming convention?
- [ ] Does `python3 tooling/symmetry_check.py` return an exit code of 0?
- [ ] If a new module was added, has `docs/meta/symmetry-map.json` been updated?
