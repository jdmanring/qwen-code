from abc import ABC, abstractmethod
from typing import Any

from .execution_context import ExecutionContext
from .models import Policy, ToolResponse


class ToolHandler(ABC):
    """
    Abstract base class for all tool handlers.
    Each tool handler is responsible for the execution logic of one or more related tools.
    """

    @abstractmethod
    async def execute(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: ExecutionContext,
        policy: Policy,
        search_tool: Any,
        state_manager: Any,
    ) -> ToolResponse:
        """
        Execute the requested tool.

        Args:
            tool_name: The name of the tool to execute.
            args: The arguments provided to the tool.
            context: The current execution context (cache, etc.).
            policy: The active policy enforcing boundaries.
            search_tool: The vector search tool instance.
            state_manager: The JobStateManager instance.

        Returns:
            A ToolResponse object indicating success/failure and the result content.
        """
        pass
