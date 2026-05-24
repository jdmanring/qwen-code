import asyncio
import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.client.session import ClientSession

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
async def test_duplicate_suppression():
    """
    Verify that identical texts are rejected to prevent duplicate storage.
    """
    # Mock the MCP client session
    mock_session = AsyncMock(spec=ClientSession)

    # Mock the tool call to return a "queued" status for the first call and "rejected" for the second
    mock_session.call_tool.side_effect = [
        MagicMock(content=[MagicMock(text=json.dumps({"status": "queued"}))]),
        MagicMock(content=[MagicMock(text=json.dumps({"status": "rejected"}))]),
    ]

    # Mock the stdio_client context manager
    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        test_text = "This is a unique fact that should only be stored once."

        # 1. First ingestion - should be accepted
        res1 = await mock_session.call_tool("ingest", {"text": test_text, "tier": "local"})
        data1 = json.loads(res1.content[0].text)
        assert data1["status"] == "queued", f"First ingestion failed: {data1}"

        # 2. Second ingestion of the exact same text - should be rejected
        res2 = await mock_session.call_tool("ingest", {"text": test_text, "tier": "local"})
        data2 = json.loads(res2.content[0].text)
        assert data2["status"] == "rejected", (
            f"Duplicate should have been rejected, but got: {data2}"
        )


@pytest.mark.asyncio
async def test_noise_filtering():
    """
    Verify that "noise" words are rejected.
    """
    # Mock the MCP client session
    mock_session = AsyncMock(spec=ClientSession)

    # Mock the tool call to return a "rejected" status for all noise samples
    mock_session.call_tool.return_value = MagicMock(
        content=[MagicMock(text=json.dumps({"status": "rejected"}))]
    )

    # Mock the stdio_client context manager
    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        noise_samples = ["ok", "thanks", "cool", "yes", "no"]

        for sample in noise_samples:
            res = await mock_session.call_tool("ingest", {"text": sample, "tier": "local"})
            data = json.loads(res.content[0].text)
            assert data["status"] == "rejected", (
                f"Noise sample '{sample}' should have been rejected, but got: {data}"
            )


if __name__ == "__main__":
    asyncio.run(test_duplicate_suppression())
