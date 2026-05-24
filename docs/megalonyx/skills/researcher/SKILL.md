# Skill: Researcher

## 1. Skill Identity
The **Researcher** is a deterministic protocol for external knowledge acquisition. It transforms raw web data into synthesized technical implementation briefs, ensuring that developers have verified, high-authority information before starting implementation.

## 2. Trigger Logic
This skill is triggered when the system needs:
- **External Knowledge**: Information not present in the local codebase or internal docs.
- **API Documentation**: Researching third-party library usage or API signatures.
- **Problem Solving**: Finding solutions to obscure bugs or exploring industry best practices.
- **Keywords**: `research`, `find documentation`, `technical brief`, `look up API`.

## 3. Operational Workflow
1. **Query Formulation**: Deconstructs the research goal into 3-5 targeted search queries to ensure multi-angle coverage.
2. **Broad Search**: Uses `tavily_search` to identify high-authority sources (official documentation, GitHub issues, reputable technical blogs).
3. **Deep Extraction**: Uses `web_fetch` or `tavily_research` to extract full page content. It strictly avoids relying on search snippets.
4. **Cross-Verification**: Compares data across multiple sources to identify consensus and highlight contradictions.
5. **Technical Synthesis**: Compiles the verified data into a "Technical Brief" including implementation details and known pitfalls.

## 4. Output Contract
The Researcher produces a standardized technical brief:
- **TECHNICAL BRIEF**: The synthesized answer, formatted specifically for a Developer's consumption.
- **EVIDENCE**: A list of verified URLs used to support the claims.
- **CONTRADICTIONS**: Any conflicting information found between different sources.
- **CONFIDENCE**: A numerical value `(0.0 - 1.0)` based on source authority and consensus.

## 5. Symmetry Link
Original Configuration: [`config/skills/researcher/SKILL.md`](../../../config/skills/researcher/SKILL.md)
