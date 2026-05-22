# 🏗️ The Hybrid Stack: Cognitive & Interface Layers

This document describes the architectural split between the cognitive engine and the user interface in the Sovereign stack.

## 🧩 The Architectural Split

The Sovereign stack is implemented as a hybrid system to separate deep cognitive reasoning from high-performance UI rendering.

### 1. The Cognitive Engine (Python Core)
**Role**: The "Brain."
- **Implementation**: Written in Python.
- **Responsibilities**:
    - Model routing and provider management.
    - Persona injection and prompt construction.
    - Tool dispatch and `PolicyEngine` enforcement.
    - State management and memory bridging.
- **Nature**: Headless. It provides a set of services (via the `ControlPlane`) but has no native UI.

### 2. The Interface Layer (Node.js TUI)
**Role**: The "Senses and Voice."
- **Implementation**: Written in Node.js / TypeScript.
- **Responsibilities**:
    - Rendering the Terminal User Interface (TUI) using Ink.
    - Managing the high-level ReAct loop.
    - Handling user input and streaming model responses.
    - Managing session persistence and local configuration.
- **Nature**: The primary entry point for the user.

---

## 🔄 Communication Flow

The Interface Layer communicates with the Cognitive Engine as a backend service.

**User Input** $\to$ **Node.js TUI** $\to$ **Python ControlPlane** $\to$ **LLM** $\to$ **Python ControlPlane** $\to$ **Node.js TUI** $\to$ **User Output**

### Key Integration Points
- **The Loop**: The Node.js layer manages the "Turn Loop," deciding when to call the Python core and how to render the resulting tool calls or text.
- **TUI Components**: Complex elements like the `PermissionsDialog` or `MemoryDialog` are rendered in Node.js, but the data they display and the actions they trigger are managed by the Python core.
- **Streaming**: The system uses SSE (Server-Sent Events) or standard streams to pipe model responses from the Python core to the Node.js TUI in real-time.

---

## ⚙️ Configuration Hierarchy

The system uses a layered configuration approach to ensure flexibility:

1. **Blueprint Layer (`config/`)**: Static definitions of personas, skills, and commands. These are the "Default Laws."
2. **User Layer (`~/.qwen/settings.json`)**: User-specific overrides for models, providers, and approval modes.
3. **Environment Layer (`~/.qwen/.env`)**: Secret keys and API tokens.
4. **Session Layer (`~/.qwen/state.json`)**: Ephemeral state, including the current todo list and active phase.
