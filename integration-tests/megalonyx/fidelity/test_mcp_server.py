import asyncio

from mcp.server import Server


async def main():
    server = Server("test-server")
    print(f"Server object: {server}")
    print(f"Has run method: {hasattr(server, 'run')}")
    if hasattr(server, "run"):
        print(f"run type: {type(server.run)}")


if __name__ == "__main__":
    asyncio.run(main())
