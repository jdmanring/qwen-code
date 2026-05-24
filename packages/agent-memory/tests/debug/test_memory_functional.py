import asyncio
import json
import os

from control_plane_daemon.mcp_manager import MCPManager


async def run_data_loop_test():
    print("Starting Functional Data Loop Test...")

    socket_path = os.path.join(
        os.path.expanduser("~"), ".local/share/megalonyx/tmp/qwen_memory.sock"
    )
    server_name = "memory-daemon"

    mgr = MCPManager()
    try:
        test_text = "The secret code is 9988776655. This is a functional verification string."
        print("\n[1/3] Ingesting test text...")
        ingest_res = await mgr.call_tool(
            server_name,
            tool_name="ingest",
            arguments={"text": test_text},
            socket_path=socket_path,
        )
        print(f"Ingest Response: {ingest_res}")

        await asyncio.sleep(5)

        query = "What is the secret code?"
        print(f"\n[2/3] Searching for: '{query}'...")
        search_res = await mgr.call_tool(
            server_name,
            tool_name="search",
            arguments={"query": query},
            socket_path=socket_path,
        )
        print(f"Search Response: {search_res}")

        content = search_res["content"][0]["text"]
        results = json.loads(content)

        print("\n[3/3] Verifying results...")

        found_local = any("9988776655" in str(res) for res in results.get("local", []))
        found_cloud = any("9988776655" in str(res) for res in results.get("cloud", []))
        found = found_local or found_cloud

        if found:
            print("\nSUCCESS: Data Loop Verified. Ingested data was successfully recalled.")
            return True
        else:
            print("\nFAILURE: Ingested data was NOT found in search results.")
            return False

    except (
        json.JSONDecodeError,
        OSError,
        RuntimeError,
        ValueError,
        KeyError,
        IndexError,
    ) as e:
        print(f"\nERROR during test: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        await mgr.close_all()


if __name__ == "__main__":
    import sys

    success = asyncio.run(run_data_loop_test())
    sys.exit(0 if success else 1)
