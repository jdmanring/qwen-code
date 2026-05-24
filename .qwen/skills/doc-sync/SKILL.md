<skill_identity>
  A deterministic protocol for eliminating "Documentation Rot" by synchronizing technical docs with the actual implementation.
</skill_identity>

<deterministic_algorithm>
  1. **Implementation Audit**: Use `read_file` and `grep` to analyze the current state of the target feature (API signatures, parameter names, logic flow).
  2. **Doc Discovery**: Use `glob` and `grep` to find all documentation files (`.md`, `.txt`) that reference the target feature.
  3. **Delta Analysis**: Compare the implementation audit results with the current documentation to identify discrepancies.
  4. **Synchronized Update**: Use `edit` to update the documentation to perfectly reflect the current implementation.
  5. **Truth Verification**: Re-read the updated doc and the code side-by-side to ensure 100% alignment.
</deterministic_algorithm>

<hard_constraints>
  - **Implementation-First**: NEVER update documentation based on a plan; ONLY update it after the code has been verified.
  - **Zero-Assumption**: Every doc change MUST be backed by a specific line of code as evidence.
  - **Clarity over Brevity**: ALWAYS ensure that complex architectural decisions are explained clearly, not just listed.
</hard_constraints>

<output_contract>
  1. **SYNC REPORT**: A list of all documentation files and sections modified.
  2. **DELTA SUMMARY**: A "Before vs. After" summary of the changes made to the docs.
  3. **VERIFICATION**: Confirmation that all related symbols in the code were checked.
  4. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
