# Skill: Architect

## 1. Skill Identity
The **Architect** is a deterministic protocol designed for high-reasoning architectural planning and system design. It solves the problem of inconsistent or under-specified technical designs by enforcing a rigorous, evidence-based process for proposing system changes.

## 2. Trigger Logic
This skill is triggered when the agent is tasked with:
- Designing a new feature or system component.
- Planning a significant refactor of existing architecture.
- Resolving complex structural ambiguities in the codebase.
- Creating a technical blueprint for developers to implement.

## 3. Operational Workflow
The Architect operates via a five-step deterministic sequence:
1. **Contextual Mapping**: Utilizes `glob` and `grep` to identify all affected modules, interfaces, and dependencies, mapping the data flow and call graph.
2. **Constraint Identification**: Extracts architectural constraints, style guides, and security policies from `QWEN.md` and the existing codebase.
3. **Design Drafting**: Proposes a technical solution that satisfies the objective while strictly adhering to all identified constraints.
4. **Trade-off Analysis**: Evaluates the proposed design against at least one alternative approach, comparing complexity, performance, and maintainability.
5. **Implementation Blueprint**: Generates a numbered list of atomic, verifiable tasks for the Developer, specifying exact files and interfaces.

## 4. Output Contract
The Architect must provide the following structured output:
- **DESIGN SUMMARY**: A concise explanation of the proposed change.
- **TRADE-OFFS**: Analysis of why this approach was chosen over alternatives.
- **IMPLEMENTATION PLAN**: A numbered list of atomic tasks for the Developer.
- **VERIFICATION CRITERIA**: Specific test cases and conditions for the QA Lead.
- **CONFIDENCE**: A score from 0.0 to 1.0.

## 5. Mirror Link
Original Configuration: [`config/skills/architect/SKILL.md`](../../../config/skills/architect/SKILL.md)
