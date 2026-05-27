#  System Management Guidelines

This document defines the boundaries and protocols for how the agent interacts with the host system and its services.

## 1. Service Interaction Protocol

The agent must never assume the state of any service. All service-related operations must follow the `Inquire` $\rightarrow$ `Verify` $\rightarrow$ `Observe` loop.

### The Loop:
1. **Inquire**: Check the current state of the service using the user's preferred management tool (e.g., `mega-memory-manager status`).
2. **Verify**: If a change is requested (e.g., `mega-memory-manager start`), perform the action and immediately verify the result using the same tool.
3. **Observe**: Monitor the service's behavior (e.g., via logs or functional tests) to ensure it is operating as expected in the context of the task.

### Forbidden Actions:
- NEVER attempt to start or stop services using generic system commands (e.g., `systemctl`, `service`, `sudo`) unless explicitly instructed.
- NEVER assume a service is "healthy" just because its process is visible in `ps`.

## 2. Error Handling for Environment Failures

The agent must distinguish between **Code Bugs** and **Environment Discrepancies**.

### Definitions:
- **Code Bug**: An error that is reproducible by changing the code or configuration (e.g., a `TypeError`, `KeyError`, or a failed unit test).
- **Environment Discrepancy**: An error that occurs due to the state of the host system (e.g., `ConnectionRefusedError`, `PermissionError`, `FileNotFoundError` for system paths, or a service being `[OFF]`).

### The Protocol:
When an error occurs that appears to be environment-related:
1. **Identify**: Determine if the error is a standard environment error (e.g., `ConnectionRefusedError`).
2. **Halt**: If the error is an Environment Discrepancy, **STOP ALL CODE MODIFICATIONS**.
3. **Report**: Inform the user of the discrepancy and the observed error.
4. **Request Clarification**: Ask the user to verify the service state or provide the correct environment configuration.

**NEVER attempt to "patch" the codebase to bypass an environment error.**
