import os
import subprocess
from typing import Any

from .execution_context import ExecutionContext
from .models import Policy, ToolResponse
from .tool_handler import ToolHandler

_ERR = ToolResponse(success=False, content=None)


def _err(msg: str) -> ToolResponse:
    return ToolResponse(success=False, content=None, error=msg)


class FileHandler(ToolHandler):
    """Handles file system operations: reading and writing files."""

    def __init__(self, stack_root: str) -> None:
        self.stack_root = stack_root

    def _resolve_path(self, path: str | None) -> str | None:
        if not path:
            return None
        if os.path.isabs(path):
            return path
        return os.path.join(self.stack_root, path)

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            if tool_name == "read_file":
                file_path = self._resolve_path(args.get("file_path"))
                if not file_path or not os.path.exists(file_path):
                    return _err(f"File not found: {file_path}")

                if context:
                    cached_content = context.file_cache.get(file_path)
                    if cached_content:
                        return ToolResponse(success=True, content=cached_content)

                if "allowed_paths" in policy.model_dump():
                    allowed = policy.allowed_paths
                    if "*" not in allowed and not any(
                        file_path.endswith(p.replace("**", "")) for p in allowed
                    ):
                        return _err(f"Policy Violation: Access to {file_path} is not permitted.")

                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                if context:
                    context.file_cache.set(file_path, content)

                return ToolResponse(success=True, content=content)

            if tool_name == "write_file":
                file_path = self._resolve_path(args.get("file_path"))
                content_val = args.get("content")
                if not file_path or not isinstance(content_val, str):
                    return _err("Missing file_path or content (must be string) for write_file")

                if "allowed_paths" in policy.model_dump():
                    allowed = policy.allowed_paths
                    if "*" not in allowed and not any(
                        file_path.endswith(p.replace("**", "")) for p in allowed
                    ):
                        return _err(
                            f"Policy Violation: Write access to {file_path} is not permitted."
                        )

                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content_val)

                return ToolResponse(success=True, content=f"Successfully wrote to {file_path}")

            return _err(f"Tool {tool_name} not implemented in FileHandler")
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))


class SearchHandler(ToolHandler):
    """Handles search operations: grep and semantic search."""

    def __init__(self, stack_root: str) -> None:
        self.stack_root = stack_root

    def _resolve_path(self, path: str | None) -> str | None:
        if not path:
            return None
        if os.path.isabs(path):
            return path
        return os.path.join(self.stack_root, path)

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            if tool_name == "grep_search":
                pattern = args.get("pattern")
                path = self._resolve_path(args.get("path", "."))
                if not pattern or not path:
                    return _err("Missing pattern or path for grep_search")

                result = subprocess.run(
                    ["rg", pattern, path], capture_output=True, text=True, encoding="utf-8"
                )
                return ToolResponse(
                    success=True,
                    content=(
                        result.stdout
                        if result.returncode == 0
                        else f"No matches found or error: {result.stderr}"
                    ),
                )

            if tool_name == "semantic_search":
                query = args.get("query", "")
                limit = args.get("limit", 5)
                result = search_tool.semantic_search(query, limit)
                return ToolResponse(success=True, content=result)

            return _err(f"Tool {tool_name} not implemented in SearchHandler")
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))


class MemoryHandler(ToolHandler):
    """Handles memory operations via the Memory Daemon."""

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            if tool_name in ["memory_ingest", "memory_search", "memory_reflect"]:
                from .mcp_manager import MCPManager

                socket_path = os.path.join(
                    os.path.expanduser("~"),
                    ".local/share/megalonyx/sockets/megalonyx_memory.sock",
                )

                mgr = MCPManager()
                mgr.register_server("memory", socket_path=socket_path)

                method_map = {
                    "memory_ingest": "ingest",
                    "memory_search": "search",
                    "memory_reflect": "reflect",
                }

                method = method_map[tool_name]
                result = await mgr.call_tool(server_name="memory", tool_name=method, arguments=args)
                return ToolResponse(success=True, content=result)

            if tool_name == "archive_knowledge":
                key = args.get("key")
                if not key:
                    return _err("Missing 'key' argument for archive_knowledge")
                if not state_manager:
                    return _err("StateManager instance not available for archive_knowledge")

                success = state_manager.archive_item(key)
                if success:
                    return ToolResponse(
                        success=True,
                        content=f"Context for '{key}' archived successfully.",
                    )
                else:
                    return _err(f"Key '{key}' not found in rag_context.")

            return _err(f"Tool {tool_name} not implemented in MemoryHandler")
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))


class MCPHandler(ToolHandler):
    """Handles Model Context Protocol (MCP) tool calls."""

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            from .mcp_manager import MCPManager

            mgr = MCPManager()
            server_name = args.get("server_name")
            if not server_name:
                return _err("Missing 'server_name' argument")

            command = args.get("command", ["npx", "-y", "@modelcontextprotocol/server-everything"])
            mgr.register_server(server_name, command=command)

            if tool_name == "mcp_list_tools":
                result: Any = await mgr.list_tools(server_name)
            elif tool_name == "mcp_call_tool":
                result = await mgr.call_tool(
                    server_name, args["tool_name"], args.get("arguments", {})
                )
            elif tool_name == "mcp_read_resource":
                result = await mgr.read_resource(server_name, args["uri"])
            else:
                return _err(f"Tool {tool_name} not implemented in MCPHandler")

            return ToolResponse(success=True, content=result)
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))


class LSPHandler(ToolHandler):
    """Handles Language Server Protocol (LSP) operations."""

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            from .lsp_manager import LSPManager

            mgr = LSPManager()
            file_path = args.get("file_path")
            if not file_path:
                return _err("Missing 'file_path' argument")

            if tool_name == "lsp_get_definitions":
                symbol = args.get("symbol")
                if not symbol:
                    return _err("Missing 'symbol' argument")
                result: Any = await mgr.get_definition(file_path, symbol)
            elif tool_name == "lsp_get_references":
                symbol = args.get("symbol")
                if not symbol:
                    return _err("Missing 'symbol' argument")
                result = await mgr.get_references(file_path, symbol)
            elif tool_name == "lsp_get_diagnostics":
                result = await mgr.get_diagnostics(file_path)
            elif tool_name == "lsp_hover":
                line = args.get("line")
                column = args.get("column")
                if line is None or column is None:
                    return _err("Missing 'line' or 'column' argument")
                result = await mgr.hover(file_path, line, column)
            else:
                return _err(f"Tool {tool_name} not implemented in LSPHandler")

            return ToolResponse(success=True, content=result)
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))


class AgentHandler(ToolHandler):
    """Handles agent generation and management."""

    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        try:
            if tool_name == "create_agent":
                from .agent_generator import AgentGenerator
                from .tool_executor import load_settings

                description = args.get("description")
                if not description:
                    return _err("Missing 'description' argument for create_agent")

                _agent_settings = load_settings()
                gen_service = AgentGenerator(_agent_settings)

                agent_data = await gen_service.generate(description)
                return ToolResponse(
                    success=True, content={"status": "success", "agent_data": agent_data}
                )

            return _err(f"Tool {tool_name} not implemented in AgentHandler")
        except (OSError, RuntimeError, ValueError) as e:
            return _err(str(e))
