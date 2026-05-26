#!/usr/bin/env python3
import asyncio
import ctypes
import logging
import os
import signal
import sys
import threading

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp.bridge")

PR_SET_PDEATHSIG = 1
SIGTERM = signal.SIGTERM


def set_pdeathsig() -> None:
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.prctl(PR_SET_PDEATHSIG, SIGTERM)
        logger.info("Parent death signal (SIGTERM) configured.")
    except OSError as e:
        logger.error(f"Failed to set PDEATHSIG: {e}")


class StdioReader:
    """
    A reader for sys.stdin that uses a separate thread to avoid
    PermissionError with asyncio.loop.add_reader on certain platforms/environments.
    """

    def __init__(self) -> None:
        self.queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def _read_loop(self) -> None:
        try:
            while not self._stop_event.is_set():
                # Read from stdin buffer
                data = sys.stdin.buffer.read(4096)
                if data:
                    self.loop.call_soon_threadsafe(self.queue.put_nowait, data)
                elif not data:
                    # EOF reached
                    self.loop.call_soon_threadsafe(self.queue.put_nowait, None)
                    break
        except Exception as e:
            logger.error(f"Stdin read thread error: {e}")
            self.loop.call_soon_threadsafe(self.queue.put_nowait, None)

    async def read(self) -> bytes | None:
        return await self.queue.get()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            # We can't easily interrupt a blocking read on stdin,
            # but daemon=True will handle it on exit.
            pass


async def pipe_stdio_to_uds(reader: StdioReader, uds_writer: asyncio.StreamWriter) -> None:
    """
    Pipes bytes from the non-blocking reader to the UDS socket.
    """
    try:
        while True:
            chunk = await reader.read()
            if chunk is None:
                logger.info("Stdin EOF reached.")
                break

            uds_writer.write(chunk)
            await uds_writer.drain()
    except asyncio.CancelledError:
        pass
    except (OSError, ConnectionError) as e:
        logger.error(f"Error piping stdin -> UDS: {e}")
        raise


async def pipe_uds_to_stdio(uds_reader: asyncio.StreamReader, stdout_buffer: object) -> None:
    """
    Pipes bytes from the UDS socket to stdout.
    """
    try:
        while True:
            # UDS reader is already async and non-blocking
            chunk = await uds_reader.read(4096)
            if not chunk:
                logger.info("UDS EOF reached.")
                break

            stdout_buffer.write(chunk)  # type: ignore[union-attr]
            stdout_buffer.flush()  # type: ignore[union-attr]
    except asyncio.CancelledError:
        pass
    except (OSError, ConnectionError) as e:
        logger.error(f"Error piping UDS -> stdout: {e}")
        raise


async def main() -> None:
    set_pdeathsig()

    socket_path = os.path.join(
        os.path.expanduser("~"), ".local/share/megalonyx/tmp/qwen_memory.sock"
    )

    logger.info("Initializing Memory Bridge (Event-Driven Mode)...")

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_unix_connection(socket_path), timeout=2.0
        )
        logger.info("Successfully connected to Memory Daemon.")
    except (OSError, TimeoutError) as e:
        logger.error(f"Connection failed: {e}")
        sys.exit(1)

    # Initialize the non-blocking stdin reader
    stdin_reader = StdioReader()
    stdin_reader.start()

    try:
        # Use gather to run both loops.
        await asyncio.gather(
            pipe_stdio_to_uds(stdin_reader, writer),
            pipe_uds_to_stdio(reader, sys.stdout.buffer),
        )
    except (OSError, RuntimeError) as e:
        # Last Resort: Top-level bridge loop error handler
        logger.exception(f"Bridge loop error: {e}")
        sys.exit(1)
    finally:
        stdin_reader.stop()
        writer.close()
        try:
            await writer.wait_closed()
        except (OSError, RuntimeError):
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
