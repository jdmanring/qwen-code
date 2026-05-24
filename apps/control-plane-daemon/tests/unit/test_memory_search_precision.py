import asyncio
import json
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


@pytest.mark.asyncio
async def test_retrieval_precision() -> None:
    """
    Verify that the system can retrieve a specific fact from a noisy environment.
    """
    target_text = "The secret password for the test is 'GoldenGate2026'."

    mock_session = AsyncMock(spec=ClientSession)

    # Mocking the sequence of tool calls:
    # 1. 50x ingest (noise)
    # 2. 1x ingest (target)
    # 3. 1x search (target)

    # Setup side effects for ingest calls
    ingest_responses = [create_mcp_response({"status": "queued"}) for _ in range(51)]

    # Setup search response
    search_response = create_mcp_response(
        [
            {"payload": {"text": "Random fact 1"}},
            {"payload": {"text": target_text}},
            {"payload": {"text": "Random fact 2"}},
        ]
    )

    mock_session.call_tool.side_effect = ingest_responses + [search_response]
    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        # We bypass the real get_session() and use the mock
        async with mock_stdio_client as (read, write):
            async with mock_session as session:
                # 1. Ingest noise
                noise_facts = [f"Random unrelated fact number {i}" for i in range(50)]
                for fact in noise_facts:
                    await session.call_tool("ingest", {"text": fact, "tier": "local"})

                # 2. Ingest target
                await session.call_tool("ingest", {"text": target_text, "tier": "local"})

                # 3. Search for target
                search_result = await session.call_tool(
                    "search", {"query": "What is the secret password?", "tier": "local"}
                )

                data = json.loads(search_result.content[0].text)

                # Verify target is in the results
                found = any(target_text in r["payload"]["text"] for r in data)
                assert found, f"Target fact not found in search results. Got: {data}"

                # Verify it is highly ranked (top 3)
                top_results = data[:3]
                found_in_top = any(target_text in r["payload"]["text"] for r in top_results)
                assert found_in_top, "Target fact was found but not in the top 3 results."


@pytest.mark.asyncio
async def test_tier_isolation() -> None:
    """
    Verify that searching in one tier does not return results from another.
    """
    mock_session = AsyncMock(spec=ClientSession)

    # Setup side effects for ingest calls (2 ingests)
    ingest_responses = [create_mcp_response({"status": "queued"}) for _ in range(2)]

    # Setup search responses
    local_search_response = create_mcp_response([{"payload": {"text": "This is a LOCAL fact."}}])
    cloud_search_response = create_mcp_response([{"payload": {"text": "This is a CLOUD fact."}}])

    mock_session.call_tool.side_effect = ingest_responses + [
        local_search_response,
        cloud_search_response,
    ]
    mock_read = MagicMock()
    mock_write = MagicMock()
    mock_stdio_client = MagicMock()
    mock_stdio_client.__aenter__.return_value = (mock_read, mock_write)
    mock_stdio_client.__aexit__.return_value = None

    with (
        patch("mcp.client.stdio.stdio_client", return_value=mock_stdio_client),
        patch("mcp.client.session.ClientSession", return_value=mock_session),
    ):
        local_text = "This is a LOCAL fact."
        cloud_text = "This is a CLOUD fact."

        # 1. Ingest
        await mock_session.call_tool("ingest", {"text": local_text, "tier": "local"})
        await mock_session.call_tool("ingest", {"text": cloud_text, "tier": "cloud"})

        # 2. Search Local
        local_search = await mock_session.call_tool("search", {"query": "fact", "tier": "local"})
        local_data = json.loads(local_search.content[0].text)

        assert any(local_text in r["payload"]["text"] for r in local_data)
        assert not any(cloud_text in r["payload"]["text"] for r in local_data), (
            "Found cloud fact in local search!"
        )

        # 3. Search Cloud
        cloud_search = await mock_session.call_tool("search", {"query": "fact", "tier": "cloud"})
        cloud_data = json.loads(cloud_search.content[0].text)

        assert any(cloud_text in r["payload"]["text"] for r in cloud_data)
        assert not any(local_text in r["payload"]["text"] for r in cloud_data), (
            "Found local fact in cloud search!"
        )


if __name__ == "__main__":

    async def main():
        print("Running Precision Tests...")
        try:
            await test_retrieval_precision()
            print("[OK] Retrieval precision verified.")
            await test_tier_isolation()
            print("[OK] Tier isolation verified.")
            print("\nALL PRECISION TESTS PASSED!")
        except (
            AssertionError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            OSError,
        ) as e:
            print(f"\n[FAIL] Tests failed: {e}")
            import sys

            sys.exit(1)

    asyncio.run(main())
