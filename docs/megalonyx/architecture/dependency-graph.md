# 📉 Dependency Graph: Independent Flow

This document provides a high-level visualization of the data and control flow within the Megacode monorepo.

## 🔄 High-Level Flow

The system follows a strictly hierarchical flow to maintain modularity and prevent circular dependencies.

```text
[ User / API ]
       |
       v
[ apps/qwen-orchestrator ] <-----------------------+
       |                                           |
       v                                           |
[ packages/sdk-* ] (TypeScript/Python/Java)        |
       |                                           |
       v                                           |
[ packages/core ] (The Brain)                      |
       |                                           |
       +--> [ Permission Classifier ]              |
       |                                           |
       +--> [ Tool Dispatcher ] -------------------+ (Feedback Loop)
       |                                           |
       +--> [ Memory Bridge ]                      |
       |                                           |
       v                                           |
[ packages/infra ] (The Body)                      |
       |                                           |
       +--> [ Qdrant Adapter ] --------------------+
       |
       +--> [ Filesystem Wrapper ]
       |
       v
[ System / OS / Network ]
```

## 🛠️ Detailed Interaction Logic

1. **Request Phase**:
   `User` -> `App` -> `Core (Tool Dispatcher)`

2. **Validation Phase**:
   `Core (Tool Dispatcher)` -> `Core (Permission Classifier)` -> `Core (Tool Dispatcher)`

3. **Contextualization Phase**:
   `Core (Tool Dispatcher)` -> `Core (Memory Bridge)` -> `Core (Tool Dispatcher)`

4. **Execution Phase**:
   `Core (Tool Dispatcher)` -> `Infra (Adapter)` -> `System/OS`

5. **Persistence Phase**:
   `System/OS` -> `Infra (Adapter)` -> `Core (Memory Bridge)` -> `Infra (Qdrant)`

---

## 🚫 Forbidden Paths
To prevent architectural decay, the following paths are strictly forbidden:
- `packages/core` -> `apps/` (Core must not know about the App)
- `packages/infra` -> `apps/` (Infra must not know about the App)
- `packages/infra` -> `packages/core` (Infra should not dictate Core logic)
