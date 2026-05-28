import sys
from pathlib import Path

# Add project root to sys.path to allow importing from packages/

# Add memory package to sys.path
sys.path.insert(0, str(PROJECT_ROOT / "packages/memory"))

try:
    from memory_daemon import MemoryDaemon
    from memory_transport import run_socket_server

    print("Starting MemoryDaemon...")
    core = MemoryDaemon()
    print("Calling core.start()...")
    core.start()
    print("Calling run_socket_server()...")
    # Use the standard socket path
    socket_path = Path.home() / ".local/share/megalonyx/tmp/megalonyx_memory.sock"
    run_socket_server(core, str(socket_path))
except (ImportError, OSError, RuntimeError, ValueError, TypeError, AttributeError) as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
