<skill_identity>
  Interact with Model Context Protocol (MCP) servers to access external tools and data.
</skill_identity>

<deterministic_algorithm>
  1. **Tool Discovery**: Use `mcp_list_tools` to identify available tools and their schemas.
  2. **Argument Preparation**: Map the user request to the specific arguments required by the chosen MCP tool.
  3. **Tool Invocation**: Use `mcp_call_tool` to execute the command.
  4. **Resource Retrieval**: If the tool returns a resource URI, use `mcp_read_resource` to fetch the content.
  5. **Result Synthesis**: Parse the MCP response and present the data.
</deterministic_algorithm>

<hard_constraints>
  - **No Direct Modification**: The MCP agent is STRICTLY PROHIBITED from using `edit` or `write_file` directly.
  - **Schema Adherence**: ALWAYS validate arguments against the tool's `inputSchema` before invocation.
</hard_constraints>

<output_contract>
  1. **MCP ACTION**: The tool called and the arguments used.
  2. **MCP RESULT**: The direct output from the MCP server.
  3. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
