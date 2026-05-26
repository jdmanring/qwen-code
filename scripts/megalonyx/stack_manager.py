#!/usr/bin/env python3
import logging
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ======================================
# CONFIGURATION
# ======================================
STACK_ROOT = Path.home() / ".local/share/megalonyx"
LOG_FILE = Path.home() / ".qwen/logs/mega-memory-manager.log"
TMP_DIR = STACK_ROOT / "tmp"
SOCKETS_DIR = STACK_ROOT / "sockets"


# Qdrant Config
QDRANT_BIN = STACK_ROOT / "packages/infra/qdrant/bin/qdrant"
QDRANT_CONFIG = STACK_ROOT / "config/qdrant_config.yaml"
QDRANT_PID_FILE = TMP_DIR / "qdrant.pid"
QDRANT_HEALTH_URL = "http://localhost:6333/health"


# Memory Config
MEMORY_BIN = STACK_ROOT / "py/venv/bin/python3"
MEMORY_SCRIPT = STACK_ROOT / "packages/agent-memory/src/agent_memory/memory_daemon.py"
MEMORY_PID_FILE = TMP_DIR / "memory.pid"
MEMORY_SOCKET = SOCKETS_DIR / "megalonyx_memory.sock"


# ======================================
# LOGGING
# ======================================
os.makedirs(LOG_FILE.parent, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log(msg: str, level: str = "INFO") -> None:
    print(f"[{level}] {msg}")
    if level == "INFO":
        logging.info(msg)
    elif level == "ERROR":
        logging.error(msg)
    elif level == "WARNING":
        logging.warning(msg)


# ======================================
# HEALTH CHECKS
# ======================================
def check_qdrant_health() -> bool:
    try:
        # Use /collections as a reliable health indicator if /health is 404
        with urllib.request.urlopen("http://localhost:6333/collections", timeout=2) as response:
            return response.getcode() == 200
    except (TimeoutError, urllib.error.URLError):
        return False


def check_network_connectivity(host: str, port: int, path: str = "/healthz") -> bool:
    try:
        url = f"http://{host}:{port}{path}"
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.getcode() == 200
    except (TimeoutError, urllib.error.URLError):
        return False


def check_memory_health() -> bool:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(str(MEMORY_SOCKET))

            # Hard Evidence: Perform JSON-RPC Handshake
            handshake = (
                b'{"jsonrpc": "2.0", "id": 1, "method": "initialize", '
                b'"params": {"protocolVersion": "2024-11-05", '
                b'"capabilities": {}, "clientInfo": {"name": "health-check", "version": "1.0.0"}}'
                b"}\n"
            )
            s.sendall(handshake)

            response = s.recv(1024)
            if b"result" in response and b"jsonrpc" in response:
                return True
            return False
    except (TimeoutError, OSError):
        return False


def get_process_state(pid_file: Path, health_fn: Any) -> str:
    # First, check the actual health of the service.
    # If the service is responsive, it is OK, regardless of the PID file.
    if health_fn():
        return "OK"

    if not pid_file.exists():
        return "OFF"

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())

        # Check if process is actually running
        os.kill(pid, 0)

        # Process is running, but health check failed
        return "ZOMBIE"
    except (ProcessLookupError, ValueError, OSError):
        return "OFF"


# ======================================
# PROCESS CONTROL
# ======================================
def kill_process(pid_file: Path, pattern: str, timeout: int = 5) -> None:
    # 1. Kill by pattern first to prevent double-daemons
    try:
        subprocess.run(["pkill", "-9", "-f", pattern], check=False)
    except OSError:
        pass

    if not pid_file.exists():
        return

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())

        log(f"Stopping process {pid}...")
        os.kill(pid, signal.SIGTERM)

        # Wait for termination
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except ProcessLookupError:
                log(f"Process {pid} terminated gracefully.")
                pid_file.unlink(missing_ok=True)
                return

        log(f"Process {pid} timed out. Sending SIGKILL...", "WARNING")
        os.kill(pid, signal.SIGKILL)
        pid_file.unlink(missing_ok=True)
    except (ProcessLookupError, ValueError, OSError):
        pid_file.unlink(missing_ok=True)


def scorched_earth() -> None:
    log("Executing Scorched Earth cleanup...")
    kill_process(QDRANT_PID_FILE, "qdrant")
    kill_process(MEMORY_PID_FILE, "memory_daemon")

    # Remove stale sockets
    if MEMORY_SOCKET.exists():
        log(f"Removing stale socket {MEMORY_SOCKET}")
        MEMORY_SOCKET.unlink()


def start_process(
    name: str,
    bin_path: Path,
    args: list[str],
    pid_file: Path,
    health_fn: Any,
    timeout: int = 60,
    cwd: Path = STACK_ROOT,
    env: dict[str, str] | None = None,
) -> bool:
    log(f"Starting {name}...")

    # Ensure it's not already OK
    if get_process_state(pid_file, health_fn) == "OK":
        log(f"{name} is already running and healthy.")
        return True

    try:
        # Redirect output to logs for debugging
        log_path = LOG_FILE.parent / f"{name.lower()}_daemon.log"

        # Merge current env with provided env
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        with open(log_path, "a") as log_file:
            proc = subprocess.Popen(
                [str(bin_path)] + args,
                stdout=log_file,
                stderr=log_file,
                cwd=str(cwd),
                env=full_env,
                start_new_session=True,
            )

        with open(pid_file, "w") as f:
            f.write(str(proc.pid))

        # Wait for health check
        start_time = time.time()
        while time.time() - start_time < timeout:
            if health_fn():
                log(f"{name} is now [OK].")
                return True
            time.sleep(1)

        log(
            f"{name} failed to become healthy within {timeout}s. Check {log_path}",
            "ERROR",
        )
        return False
    except (OSError, ValueError) as e:
        log(f"Failed to start {name}: {e}", "ERROR")
        return False


# ======================================
# COMMANDS
# ======================================
def cmd_start(strict: bool = False) -> None:
    scorched_earth()

    # Define services with their specific requirements
    # (Name, Bin, Args, PID, HealthFn, Env)
    services_config = [
        (
            "Qdrant",
            QDRANT_BIN,
            ["--config-path", str(QDRANT_CONFIG)],
            QDRANT_PID_FILE,
            check_qdrant_health,
            None,
        ),
        (
            "Memory",
            MEMORY_BIN,
            ["-m", "agent_memory.memory_daemon"],
            MEMORY_PID_FILE,
            check_memory_health,
            {"PYTHONPATH": str(STACK_ROOT / "packages/agent-memory/src")},
        ),
    ]

    results = []
    for name, bin_path, args, pid_file, health_fn, env in services_config:
        success = start_process(
            name=name,
            bin_path=bin_path,
            args=args,
            pid_file=pid_file,
            health_fn=health_fn,
            env=env,
        )
        results.append((name, success))
        if not success and strict:
            log(f"Strict mode: Critical failure starting {name}. Exiting.", "ERROR")
            sys.exit(1)

    # Summary
    print("\n--- Start Summary ---")
    all_ok = True
    for name, success in results:
        status = "[OK]" if success else "[FAILED]"
        print(f"{name}: {status}")
        if not success:
            all_ok = False
    print("---------------------\n")

    if all_ok:
        log("Stack started successfully.")
    else:
        log("Stack started with some failures.", "WARNING")
        sys.exit(1)


def cmd_stop() -> None:
    log("Stopping stack services...")
    scorched_earth()
    log("Stack stopped.")


def cmd_status() -> None:
    q_state = get_process_state(QDRANT_PID_FILE, check_qdrant_health)
    m_state = get_process_state(MEMORY_PID_FILE, check_memory_health)

    print(f"Qdrant: [{q_state}]")
    print(f"Memory: [{m_state}]")

    if q_state == "OK" and m_state == "OK":
        sys.exit(0)
    elif q_state == "OFF" and m_state == "OFF":
        sys.exit(0)
    else:
        sys.exit(1)


def cmd_restart(strict: bool = False) -> None:
    cmd_stop()
    cmd_start(strict=strict)


def cmd_connectivity_check() -> None:
    log("Performing connectivity check...")

    services = [
        {"name": "Qdrant", "port": 6333, "path": "/healthz", "type": "network"},
        {"name": "Memory", "port": None, "path": None, "type": "unix"},
    ]

    print("\n--- Connectivity Report ---")
    for s in services:
        if s["type"] == "network":
            for host in ["localhost", "127.0.0.1"]:
                res = check_network_connectivity(host, s["port"], s["path"])
                print(f"{s['name']} ({host}): {'[OK]' if res else '[FAILED]'}")
        elif s["type"] == "unix":
            res = check_memory_health()
            print(f"{s['name']} (UNIX socket): {'[OK]' if res else '[FAILED]'}")
            for host in ["localhost", "127.0.0.1"]:
                print(f"{s['name']} ({host}): [FAILED] (UNIX socket only)")
    print("---------------------------\n")


# ======================================
# MAIN
# ======================================
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(
            "Usage: mega-memory-manager {start|stop|restart|status|connectivity-check} [--strict]"
        )
        sys.exit(1)

    cmd = args[0].lower()
    strict = "--strict" in args

    if cmd == "start":
        cmd_start(strict=strict)
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "restart":
        cmd_restart(strict=strict)
    elif cmd == "status":
        cmd_status()
    elif cmd == "connectivity-check":
        cmd_connectivity_check()
    else:
        print(f"Unknown command: {cmd}")
        print(
            "Usage: mega-memory-manager {start|stop|restart|status|connectivity-check} [--strict]"
        )
        sys.exit(1)
