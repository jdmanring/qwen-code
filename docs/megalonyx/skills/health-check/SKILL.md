<skill_identity>
  A diagnostic protocol to verify the operational status of the Qwen Code stack's core components, specifically the memory server socket and the master settings configuration.
</skill_identity>

<deterministic_algorithm>
  1. **Socket Verification**: Check for the existence and accessibility of the memory server socket at `~/.local/share/megalonyx/tmp/qwen_memory.sock`.
  2. **Configuration Validation**: Verify that `~/.qwen/settings.json` exists and contains valid JSON syntax.
  3. **Status Aggregation**: Compile the results from both the socket and configuration checks.
  4. **Report Generation**: Output a structured health report indicating the status of each component.
</deterministic_algorithm>

<hard_constraints>
  - **Absolute Paths**: Use absolute paths for all system checks.
  - **Graceful Failure**: Handle missing files or inaccessible sockets without crashing; report them as FAIL.
  - **Read-Only**: The skill must only read and probe; it must not modify any system state.
</hard_constraints>

<output_contract>
  1. **COMPONENT**: The name of the checked component (e.g., "Memory Socket", "Settings JSON").
  2. **STATUS**: [PASS] or [FAIL].
  3. **DETAILS**: A brief description of the finding or the specific error encountered.
</output_contract>
