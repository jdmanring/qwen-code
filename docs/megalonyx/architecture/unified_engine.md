 
# Unified Engineering Engine Architecture

## Overview
The Unified Engine transforms the agent from a series of disconnected scripts into a stateful, deterministic engineering system. Instead of "fire-and-forget" script execution, the engine implements a high-fidelity `Act -> Observe -> Verify -> Correct` loop.

## Core Components

The Unified Engine is composed of several interlocking modules that manage the lifecycle of an engineering task. For detailed technical specifications, interfaces, and algorithms, refer to the architecture documentation:

- **Control Plane**: The central orchestrator. See [Agent System Architecture](docs/architecture/agent-system.md).
- **Job State Manager**: Persistent state layer for task tracking. See [Job State Manager Architecture](docs/architecture/job_state_manager.md).
- **Verification Engine**: The quality gatekeeper. See [Verification Engine Architecture](docs/architecture/verification_engine.md).
- **Command Routing**: Maps slash-commands to workflows. See [Agent System Architecture](docs/architecture/agent-system.md) (Orchestration Flow).

## The Execution Loop: Act $\rightarrow$ Observe $\rightarrow$ Verify $\rightarrow$ Correct

The system operates on a deterministic self-healing loop to ensure high-fidelity outcomes.

For a detailed breakdown of the **Orchestration Flow** and the **Recovery Loop (RETRY/PIVOT/ABORT)**, see [Agent System Architecture: The Control Plane](docs/architecture/agent-system.md).

## Integration with Megalonyx
- **Entry Point**: `skill_bridge.py` acts as the lean CLI wrapper that instantiates the `ControlPlane`.
- **Configuration**: All model routing and API keys are resolved via `settings.json` and `~/.qwen/.env`.
- **Memory**: The `RAGTool` provides the semantic context required for the `Act` phase.
