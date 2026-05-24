import asyncio
import json
import logging
from collections.abc import AsyncIterator
from typing import Any

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_sim")


# We need to mimic the UDS streams because mcp.client.session expects them
class SimUDSReadStream:
    def __init__(self, reader: asyncio.StreamReader) -> None:
        self._reader = reader

    async def __aenter__(self) -> "SimUDSReadStream":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def __aiter__(self) -> AsyncIterator[Any]:
        return self

    async def __anext__(self) -> Any:
        line = await self._reader.readline()
        if not line:
            raise StopAsyncIteration

        try:
            data = json.loads(line.decode("utf-8"))
            # Simplified wrapping for simulation
            from mcp.shared.message import SessionMessage
            from mcp.types import JSONRPCMessage

            rpc_message = JSONRPCMessage(**data) if isinstance(data, dict) else data
            return SessionMessage(message=rpc_message)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Sim read error: {e}")
            raise


class SimUDSWriteStream:
    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer

    async def __aenter__(self) -> "SimUDSWriteStream":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._writer.close()
        await self._writer.wait_closed()

    async def send(self, message: Any) -> None:
        try:
            # Use model_dump_json if it's a Pydantic model, otherwise json.dumps
            if hasattr(message.message, "model_dump_json"):
                serialized = message.message.model_dump_json()
            else:
                serialized = json.dumps(message.message)

            payload = (serialized + "\n").encode("utf-8")
            self._writer.write(payload)
            await self._writer.drain()
        except (RuntimeError, TypeError, ValueError) as e:
            logger.error(f"Sim write error: {e}")
            raise


async def run_simulation() -> None:
    socket_path = os.path.expanduser("~/.local/share/megalonyx/tmp/megalonyx_memory.sock")
    logger.info(f"Connecting to {socket_path}...")

    try:
        reader, writer = await asyncio.open_unix_connection(socket_path)

        async with SimUDSReadStream(reader) as read, SimUDSWriteStream(writer) as write:
            from mcp.client.session import ClientSession

            async with ClientSession(read, write) as session:
                logger.info("Attempting to initialize session...")
                await session.initialize()
                logger.info("SUCCESS: Session initialized!")

                logger.info("Attempting to list tools...")
                tools = await session.list_tools()
                logger.info(f"SUCCESS: Found {len(tools.tools)} tools.")
                for t in tools.tools:
                    logger.info(f" - {t.name}")

    except (TimeoutError, ConnectionRefusedError, RuntimeError) as e:
        logger.exception(f"FAILURE: Simulation failed: {e}")


if __name__ == "__main__":
    asyncio.run(run_simulation())
