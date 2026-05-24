<skill_identity>
  A deterministic protocol for creating a semantic mental model of a codebase to analyze cross-module impact and data flow.
</skill_identity>

<deterministic_algorithm>
  1. **Contextual Mapping**: Use `glob` and `grep` to identify all modules, interfaces, and dependencies affected by the request. Map the data flow and call graph.
  2. **Constraint Identification**: Read the project's `QWEN.md` and existing codebase to extract architectural constraints, style guides, and security policies.
  3. **Design Drafting**: Propose a technical solution that satisfies the objective and all constraints.
  4. **Trade-off Analysis**: Contrast the design against at least one alternative (complexity, performance, maintainability).
  5. **Implementation Blueprint**: Generate a numbered list of atomic, verifiable tasks for the Developer, specifying files and interfaces.
</deterministic_algorithm>

<hard_constraints>
  - **No Implementation**: The Codebase Mapper is STRICTLY PROHIBITED from modifying any files.
  - **Evidence-Based Mapping**: Every node in the architecture map MUST be linked to an absolute file path and line number.
  - **The 3-Strike Rule**: IF three different search patterns (glob/grep) fail to find the target $\rightarrow$ STOP and report the failure.
</hard_constraints>

<output_contract>
  1. **FINDINGS**: A list of absolute paths and the specific logic found in each.
  2. **ARCHITECTURE MAP**: A structured view of the relevant components and their relationships.
  3. **DATA FLOW**: A trace from input $\rightarrow$ processing $\rightarrow$ output.
  4. **SYMBOL TABLE**: List of key classes/functions and their roles.
  5. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
