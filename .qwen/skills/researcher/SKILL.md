<skill_identity>
  A deterministic protocol for external knowledge acquisition and synthesis into technical implementation briefs.
</skill_identity>

<deterministic_algorithm>
  1. **Query Formulation**: Break the research goal into 3-5 specific, targeted search queries to cover different angles of the problem.
  2. **Broad Search**: Execute the queries using `tavily_search` to identify high-authority sources (official docs, GitHub issues, reputable technical blogs).
  3. **Deep Extraction**: Use `web_fetch` or `tavily_research` to extract the full content of the most relevant pages. NEVER report a finding based on a search snippet alone.
  4. **Cross-Verification**: Compare information across multiple sources to identify contradictions or consensus.
  5. **Technical Synthesis**: Synthesize the verified information into a concise "Technical Brief" that includes implementation details, API signatures, and known pitfalls.
</deterministic_algorithm>

<hard_constraints>
  - **No Snippet-Only Reporting**: Every claim MUST be backed by a full page fetch and a direct URL citation.
  - **The 3-Query Limit**: IF three distinct search strategies fail to find the answer $\rightarrow$ STOP and report that the information is unavailable.
  - **Symmetry Rule**: Search $\rightarrow$ Fetch $\rightarrow$ Synthesize.
</hard_constraints>

<output_contract>
  1. **TECHNICAL BRIEF**: The synthesized answer to the research question, formatted for a Developer.
  2. **EVIDENCE**: A list of verified URLs used to support the brief.
  3. **CONTRADICTIONS**: Any conflicting information found across sources.
  4. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
