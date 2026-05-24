# Dreaming

The Dreaming subsystem is a background cognitive process that generates autonomous ideas, prompts, or code sketches independently of direct user input. It operates via the following sequence:

1. **Context Collection**: Aggregates recent user messages, tool results, and internal memory snapshots.
2. **Reasoning Pass**: A lightweight "dream" model produces a concise plan or code fragment.
3. **Context Injection**: The generated fragment is fed back to the main agent as a system-prompt augmentation.

### Operational Value

- **Zero-Shot Generation**: Enables autonomous suggestions (e.g., function completion, test case proposal).
- **Token Optimization**: Reduces primary agent overhead by utilizing a lightweight reasoning model for initial sketching.

### Functional Integration

- **Developer Agent**: Invokes the Dreaming API for rapid prototyping prior to final implementation.
- **Architect Agent**: Utilizes Dreaming to explore divergent design alternatives.
- **Manual Trigger**: Accessible via the `/dream` slash command.

*Reference:* `../design/dreaming/README.md` in the upstream source.
