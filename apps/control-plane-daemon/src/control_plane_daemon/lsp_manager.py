import asyncio
from typing import Any, cast


class LSPManager:
    def __init__(self) -> None:
        # Mock data for prototyping
        self.mock_symbols: dict[str, dict[str, dict[str, Any]]] = {
            "main.py": {
                "main": {
                    "definition": "main.py:10",
                    "references": ["app.py:5", "test_main.py:2"],
                },
                "calculate": {
                    "definition": "utils.py:45",
                    "references": ["main.py:20"],
                },
            },
            "utils.py": {"calculate": {"definition": "utils.py:45", "references": ["main.py:20"]}},
        }
        self.mock_diagnostics = {
            "main.py": [
                {"line": 15, "message": "Unused import: 'os'", "severity": "warning"},
                {
                    "line": 42,
                    "message": "Undefined name: 'undefined_var'",
                    "severity": "error",
                },
            ]
        }

    async def get_definition(self, file_path: str, symbol: str) -> str | None:
        """Simulates finding the definition of a symbol."""
        # In a real LSP, this would communicate with the language server
        file_name = file_path.split("/")[-1]
        if file_name in self.mock_symbols and symbol in self.mock_symbols[file_name]:
            return cast(str, self.mock_symbols[file_name][symbol]["definition"])
        return None

    async def get_references(self, file_path: str, symbol: str) -> list[str]:
        """Simulates finding all references to a symbol."""
        file_name = file_path.split("/")[-1]
        if file_name in self.mock_symbols and symbol in self.mock_symbols[file_name]:
            return cast(list[str], self.mock_symbols[file_name][symbol]["references"])
        return []

    async def get_diagnostics(self, file_path: str) -> list[dict[str, Any]]:
        """Simulates retrieving diagnostics (errors/warnings) for a file."""
        file_name = file_path.split("/")[-1]
        return self.mock_diagnostics.get(file_name, [])

    async def hover(self, file_path: str, line: int, column: int) -> str:
        """Simulates getting hover information at a position."""
        # For the prototype, we just return a generic string based on line number
        return f"Hover info at {file_path}:{line}:{column} (Mocked)"


if __name__ == "__main__":
    import asyncio
    import sys

    async def test() -> None:
        mgr = LSPManager()
        print("Testing get_definition...", file=sys.stderr)
        print(await mgr.get_definition("main.py", "main"), file=sys.stderr)
        print("\nTesting get_references...", file=sys.stderr)
        print(await mgr.get_references("main.py", "calculate"), file=sys.stderr)
        print("\nTesting get_diagnostics...", file=sys.stderr)
        print(await mgr.get_diagnostics("main.py"), file=sys.stderr)
        print("\nTesting hover...", file=sys.stderr)
        print(await mgr.hover("main.py", 10, 5), file=sys.stderr)

    asyncio.run(test())
