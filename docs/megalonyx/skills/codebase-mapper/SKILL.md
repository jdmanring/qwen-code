# Skill: Codebase Mapper

## 1. Skill Identity
The **Codebase Mapper** is a deterministic protocol for creating a semantic mental model of a codebase. It solves the problem of "architectural blindness" by enabling precise analysis of cross-module impacts, data flows, and symbol relationships.

## 2. Trigger Logic
This skill is triggered when the agent needs to:
- Map the impact of a proposed change across the entire system.
- Trace the flow of data from an input source to an output sink.
- Understand the relationship between disparate modules or classes.
- Create a symbol table for a specific subsystem.

## 3. Operational Workflow
The Mapper follows a structured discovery process:
1. **Contextual Mapping**: Uses `glob` and `grep` to identify all affected modules, interfaces, and dependencies, mapping the call graph.
2. **Constraint Identification**: Reads `QWEN.md` and the codebase to extract architectural constraints and style guides.
3. **Design Drafting**: Proposes a technical solution that satisfies the objective and all constraints.
4. **Trade-off Analysis**: Contrasts the design against an alternative (evaluating complexity, performance, and maintainability).
5. **Implementation Blueprint**: Generates a numbered list of atomic tasks specifying exact files and interfaces.

## 4. Output Contract
The Mapper must deliver the following artifacts:
- **FINDINGS**: A list of absolute paths and the specific logic discovered in each.
- **ARCHITECTURE MAP**: A structured view of relevant components and their relationships.
- **DATA FLOW**: A trace from input $\rightarrow$ processing $\rightarrow$ output.
- **SYMBOL TABLE**: A list of key classes/functions and their respective roles.
- **CONFIDENCE**: A score from 0.0 to 1.0.

## 5. Symmetry Link
Original Configuration: [`config/skills/codebase-mapper/SKILL.md`](../../../config/skills/codebase-mapper/SKILL.md)
