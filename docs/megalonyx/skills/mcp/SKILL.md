# Skill: mcp

## Skill Identity
The `mcp` skill facilitates interaction with Model Context Protocol (MCP) servers. It allows the agent to extend its capabilities by accessing external tools, APIs, and data sources provided by MCP-compliant servers.

## Trigger Logic
This skill is triggered by:
- Requests to use external tools provided by an MCP server.
- The need to access data from a resource URI managed by an MCP server.
- Mentions of "MCP tools" or "MCP server" capabilities.

## Operational Workflow
1. **Tool Discovery**: Use `mcp_list_tools` to identify available tools and their required input schemas.
2. **Argument Preparation**: Map the user's request to the specific JSON schema required by the chosen tool.
3. **Tool Invocation**: Execute the tool via `mcp_call_tool`.
4. **Resource Retrieval**: If the tool returns a resource URI, use `mcp_read_resource` to fetch the actual content.
5. **Result Synthesis**: Parse the MCP server's response and integrate the data into the final answer.

## Output Contract
The output must include:
1. **MCP ACTION**: The name of the tool called and the arguments used.
2. **MCP RESULT**: The direct output returned by the MCP server.
3. **CONFIDENCE**: A numerical value (0.0 - 1.0).

## Symmetry Link
Original configuration: [`config/skills/mcp/SKILL.md`](../../../config/skills/mcp/SKILL.md)
