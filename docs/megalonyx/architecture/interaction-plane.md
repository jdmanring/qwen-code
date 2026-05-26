# 🖥️ Interaction Plane: From CLI to Orchestration Dashboard

## 1. Conceptual Shift: Chat vs. Orchestration

The project is transitioning from a **Chat-based interaction** (linear conversation) to an **Orchestration-based interaction** (system management). 

### The Limitations of CLI Chat
While the Qwen Code CLI is effective for atomic tasks, it is insufficient for managing an independent monorepo due to:
- **State Opacity**: The user cannot visually monitor the status of background services, agentic loops, or package health.
- **Review Friction**: Reviewing large-scale code changes (diffs) in a terminal is inefficient and increases the risk of overlooking errors.
- **Manual Overhead**: High-level orchestration (e.g., "Run all integration tests for the Memory package") requires manual command entry rather than a single dashboard action.

### The Orchestration Model
An Orchestration Interface transforms the interaction into a **Control Center**. Instead of simply chatting, the user manages the system via:
- **System Monitoring**: Real-time visibility into active agents, resource usage, and service health.
- **Visual Verification**: Side-by-side diff reviews and interactive approval workflows.
- **Pipeline Management**: A visual representation of the `Intent` $\rightarrow$ `Plan` $\rightarrow$ `Execute` $\rightarrow$ `Verify` loop.

---

## 2. Integration Philosophy: The "Face" vs. "Runtime Stack"

A critical architectural decision is that interfaces like **T3** and **OpenCode** are not treated as independent tools, but as the **Interaction Plane (The Face)** of the Runtime Stack.

### Why Integrated Interfaces?
Using an independent tool creates a "Blind Interface" that is unaware of the project's internal logic. By integrating the interface into the monorepo, the dashboard gains direct access to:
- **The UDS Bridge**: The UI can trigger actions through the standardized Bridge contracts.
- **The Memory System**: The UI can visualize the semantic map and architectural graph.
- **Symmetry Standards**: The UI can enforce documentation and token efficiency rules in real-time.

---

## 3. The Interface Evolution Path

The transition from CLI to a full Orchestration Dashboard follows a three-stage progression to ensure stability.

### Stage 1: Advanced TUI (Terminal User Interface)
The first step is implementing a TUI (inspired by OpenCode). This provides a split-screen terminal experience.
- **Capabilities**: Integrated file tree, real-time log streaming, and a dedicated task-tracking pane alongside the chat.
- **Goal**: Increase visibility without leaving the terminal environment.

### Stage 2: Web-Based Control Center
The second step is the implementation of a web GUI (inspired by T3).
- **Capabilities**: Rich visual diffs, interactive dependency graphs, and a comprehensive system health dashboard.
- **Goal**: Provide a high-fidelity management environment for complex orchestration.

### Stage 3: Native IDE Integration
The final stage is the development of a native extension for IDEs (e.g., VS Code, JetBrains).
- **Capabilities**: Direct manipulation of the codebase, inline agentic suggestions, and seamless integration with the developer's existing workflow.
- **Goal**: Eliminate the boundary between the orchestrator and the editor.

---

## 4. Implementation Prerequisites

To prevent the interface from becoming a "hollow shell," it must be implemented only after the following foundations are stable:
1. **The Core Orchestrator**: The "Brain" must be capable of managing state independently of the UI.
2. **The Bridge Layer**: The interface must communicate with packages via the `IExecutionProvider` and `IRoutingProvider` contracts.
3. **The Monorepo Structure**: Dependency isolation (`uv`/`pnpm`) must be in place to ensure the UI components do not conflict with core logic.
