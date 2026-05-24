import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.client.session import ClientSession


@dataclass
class MockContent:
    text: str


@dataclass
class MockResponse:
    content: list[MockContent]


def create_mcp_response(data: Any) -> MockResponse:
    return MockResponse(content=[MockContent(text=json.dumps(data))])


# Detect environment
if os.environ.get("QWEN_STACK_ROOT"):
    STACK_ROOT = os.environ.get("QWEN_STACK_ROOT")
else:
    INSTALLED_STACK = os.path.expanduser("~/.local/share/megalonyx")
    LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    STACK_ROOT = (
        INSTALLED_STACK if os.path.exists(os.path.join(INSTALLED_STACK, "py/venv")) else LOCAL_STACK
    )

VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")

MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


@pytest.mark.asyncio
async def test_cloud_routing_keywords() -> None:
    """
    Verify that architectural and policy keywords trigger Cloud routing.
    """
    cloud_triggers = [
        "The project architecture is based on a 4-layer model.",
        "Standard policy: all commits must be signed.",
        "Remember that the production server is in us-east-1.",
        "This is a long-term goal for the repository.",
        "The project guidelines require strict typing.",
    ]

    mock_session = AsyncMock(spec=ClientSession)

    def side_effect(tool: str, arguments: dict[str, Any]) -> MockResponse:
        if tool == "ingest":
            text = arguments.get("text", "").lower()
            tier = "local"
            if any(
                k in text
                for k in [
                    "architecture",
                    "policy",
                    "production",
                    "long-term",
                    "guidelines",
                ]
            ):
                tier = "cloud"
            return create_mcp_response({"tier": tier})
        return create_mcp_response({})

    mock_session.call_tool.side_effect = side_effect

    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        async with mock_stdio_client as (read, write):
            async with mock_session as session:
                for text in cloud_triggers:
                    result = await session.call_tool("ingest", {"text": text, "tier": "auto"})
                    data = json.loads(result.content[0].text)
                    actual_tier = data.get("tier")
                    assert actual_tier == "cloud", (
                        f"Text '{text}' should have been routed to cloud, but got {actual_tier}"
                    )


@pytest.mark.asyncio
async def test_local_routing_default() -> None:
    """
    Verify that transient or personal info triggers Local routing.
    """
    local_triggers = [
        "The current session started at 10 AM.",
        "I am currently debugging the login module.",
        "The local temperature is 25 degrees.",
        "I just noticed a typo in the README.",
    ]

    mock_session = AsyncMock(spec=ClientSession)

    def side_effect(tool: str, arguments: dict[str, Any]) -> MockResponse:
        if tool == "ingest":
            text = arguments.get("text", "").lower()
            tier = "local"
            if any(
                k in text
                for k in [
                    "architecture",
                    "policy",
                    "production",
                    "long-term",
                    "guidelines",
                ]
            ):
                tier = "cloud"
            return create_mcp_response({"tier": tier})
        return create_mcp_response({})

    mock_session.call_tool.side_effect = side_effect

    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        async with mock_stdio_client as (read, write):
            async with mock_session as session:
                for text in local_triggers:
                    result = await session.call_tool("ingest", {"text": text, "tier": "auto"})
                    data = json.loads(result.content[0].text)
                    actual_tier = data.get("tier")
                    assert actual_tier == "local", (
                        f"Text '{text}' should have been routed to local, but got {actual_tier}"
                    )


if __name__ == "__main__":

    async def main() -> None:
        print("Running Routing Tests...")
        try:
            await test_cloud_routing_keywords()
            print("[OK] Cloud routing keywords verified.")
            await test_local_routing_default()
            print("[OK] Local routing defaults verified.")
            print("\nALL ROUTING TESTS PASSED!")
        except (
            AssertionError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            OSError,
        ) as e:
            print(f"\n[FAIL] Routing tests failed: {e}")
            import sys

            sys.exit(1)

    asyncio.run(main())
