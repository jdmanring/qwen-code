#  Contextual Anchors: The `.qwen-context` Standard

## 1. Purpose and Scope

The `.qwen-context` file is a **Local Operational Law** used to establish directory-specific constraints, mandates, and reasoning patterns. It allows the `qwen_code_stack` to implement **Granular Cognitive Control**, overriding or augmenting global axioms with highly specific, local intelligence.

**Scope**: A `.qwen-context` file applies to its own directory and all subdirectories within that tree.

---

## 2. Format Specification

To maximize the **Signal-to-Noise Ratio (SNR)** and minimize token fragmentation, the `.qwen-context` standard uses **YAML** with **Standardized ASCII Logic**.

### 2.1 Schema Definition

| Key | Type | Description |
| :--- | :--- | :--- |
| `[M-LAWS]` | List | A collection of localized axioms and mandates. |
| `[M-METADATA]` | Map | Non-executable context (e.g., critical files, symmetry paths). |

### 2.2 Axiom Structure

Each item within `[M-LAWS]` must follow this structure:

- **Attention Landmark**: An emoji used to prime the model's reasoning domain (, , ).
- **Axiom Tag**: A bracketed identifier (e.g., `[A-ARCH]`, `[S-OPERATIONAL]`, `[A-LOGIC]`).
- `desc`: A brief human-readable description of the constraint.
- `axiom`: The deterministic, imperative mandate that the agent must follow.

---

## 3. Usage Examples

### 3.1 Architectural Constraints ()
Used to enforce structural patterns, module boundaries, or design principles.

```yaml
[M-LAWS]:
  -  [A-ARCH]:
      desc: "Module Boundary Enforcement"
      axiom: "All components in this directory must be stateless and side-effect free."
```

### 3.2 Operational Mandates ()
Used to enforce workflows, testing requirements, or deployment steps.

```yaml
[M-LAWS]:
  -  [S-OPERATIONAL]:
      desc: "Verification Requirement"
      axiom: "Always run 'stack-verify' and 'pytest' before marking a task as completed in this directory."
```

### 3.3 Logic/Reasoning Constraints ()
Used to enforce specific implementation patterns or mathematical/logical approaches.

```yaml
[M-LAWS]:
  -  [A-LOGIC]:
      desc: "Transformation Pattern"
      axiom: "All data transformations must use the 'Functional Pipeline' pattern (map/filter/reduce)."
```

### 3.4 Metadata (Non-executable)

```yaml
[M-METADATA]:
  critical_files:
    - file1.py
    - file2.py
  symmetry_path: "docs/path/"
```

---

## 4. Mandatory Agent Protocol

**[S-MANDATE]: (Directory Entry => Scan for `.qwen-context` => Integrate into Context)**

Upon entering any directory, an agent **MUST**:
1.  Check for the existence of a `.qwen-context` file.
2.  If present, parse the file and integrate the `[M-LAWS]` into its active reasoning context.
3.  Treat these local laws as **Project Standard Mandates** that take precedence over general guidelines within the scope of that directory.

---

##  Implementation Checklist for Contributors

- [ ] **ASCII Only**: Did you use `=>` instead of $\to$?
- [ ] **Anchor the Domain**: Did you use the correct category emoji (, , )?
- [ ] **Axiomatize**: Did you replace narrative suggestions with a formal `[S-MANDATE]` or `[A-AXIOM]`?
- [ ] **Symmetrize**: Is there a 1:1 mirror between the new config and the new doc?
