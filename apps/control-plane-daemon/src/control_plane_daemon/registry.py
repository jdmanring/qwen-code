from .tool_handler import ToolHandler


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered in the registry."""

    pass


class ToolRegistry:
    """
    A central registry for mapping tool names to their respective handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, tool_names: list[str], handler: ToolHandler) -> None:
        """
        Registers one or more tool names to a specific handler.
        """
        for name in tool_names:
            self._handlers[name] = handler

    def get_handler(self, tool_name: str) -> ToolHandler:
        """
        Retrieves the handler for a given tool name.

        Raises:
            ToolNotFoundError: If the tool is not registered.
        """
        if tool_name not in self._handlers:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered in the registry.")
        return self._handlers[tool_name]

    def list_registered_tools(self) -> list[str]:
        """Returns a list of all currently registered tools."""
        return list(self._handlers.keys())
