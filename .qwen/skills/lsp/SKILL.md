<skill_identity>
  Use Language Server Protocol (LSP) to perform deep semantic analysis, code navigation, and error detection.
</skill_identity>

<deterministic_algorithm>
  1. **LSP Command Selection**: Based on the request, select the appropriate LSP command (`get_definitions`, `get_references`, `get_diagnostics`, or `hover`).
  2. **Target Identification**: Resolve the requested symbol or path to an absolute file path and line number.
  3. **LSP Execution**: Execute the selected LSP command to retrieve semantic information.
  4. **Information Synthesis**: Parse the LSP response and present the findings clearly.
</deterministic_algorithm>

<hard_constraints>
  - **Read-Only**: The LSP agent is STRICTLY PROHIBITED from modifying code.
  - **Precision**: ALWAYS provide absolute file paths and line numbers for any identified symbols.
</hard_constraints>

<output_contract>
  1. **LSP RESULTS**: The direct output from the LSP command.
  2. **SEMANTIC ANALYSIS**: A brief explanation of what the findings mean for the codebase.
  3. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
