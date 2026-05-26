"""
MCP High-Fidelity Integration Suite

This test suite validates the reliability of the MCP (Model Context Protocol) bridge
under extreme environmental conditions. It is designed to catch regressions in:
- Path resolution (CWD independence)
- Output cleanliness (Stdout pollution)
- Shell compatibility
- Environment isolation (Clean-room execution)
- Protocol timing (Handshake latency)

Run this suite as part of any deployment or major configuration change.
"""

import asyncio
import json
import os
import subprocess
import sys
import time

# ======================================
# CONFIGURATION
# ======================================
# These must match exactly what is in settings.json
COMMAND = "mega-run-py"
ARGS = ["packages/core/src/stdio_socket_relay.py"]
# We need the absolute path to the wrapper for tests that use 'env -i' or different CWDs
WRAPPER_PATH = "mega-memory"
# The bridge script absolute path (for verification)
BRIDGE_ABS_PATH = (
    "stdio_socket_relay"
)
# Expected MCP initialize request
INIT_REQUEST = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "fidelity-test-suite", "version": "1.0.0"},
    },
}


async def run_mcp_command(cmd, args, input_data=None, env=None, cwd=None, timeout=5.0):
    """
    Executes an MCP command and captures raw stdout/stderr.
    """
    process = await asyncio.create_subprocess_exec(
        cmd,
        *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
        cwd=cwd,
    )

    stdout, stderr = b"", b""
    if input_data:
        process.stdin.write(input_data)
        await process.stdin.drain()

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except TimeoutError:
        process.kill()
        stdout, stderr = await process.communicate()
        return stdout, stderr, "TIMEOUT"

    return stdout, stderr, process.returncode


async def test_cwd_independence():
    print("\n[1/5] Testing CWD Independence...")
    test_dirs = ["/tmp", os.path.expanduser("~"), "/"]

    for d in test_dirs:
        print(f"  Testing CWD: {d}...", end=" ", flush=True)
        input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")
        stdout, stderr, code = await run_mcp_command(
            WRAPPER_PATH, ARGS, input_data=input_bytes, cwd=d
        )

        if b"result" in stdout and b"protocolVersion" in stdout:
            print("✅ PASS")
        else:
            print(f"❌ FAIL (Code: {code})")
            print(f"    Stderr: {stderr.decode(errors='replace')}")
            return False
    return True


async def test_stdout_pollution():
    print("\n[2/5] Testing Stdout Pollution Audit...")
    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")
    stdout, stderr, code = await run_mcp_command(
        WRAPPER_PATH, ARGS, input_data=input_bytes
    )

    if not stdout:
        print("❌ FAIL: No output received.")
        return False

    # Split stdout into lines
    lines = stdout.decode(errors="replace").strip().split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if not line.startswith("{"):
            print(f"❌ FAIL: Pollution detected at line {i + 1}: {repr(line)}")
            return False

    print("✅ PASS: Stdout is clean JSON-RPC.")
    return True


async def test_shell_robustness():
    print("\n[3/5] Testing Shell Robustness...")
    shells = ["/bin/sh", "/bin/bash"]

    for shell in shells:
        print(f"  Testing Shell: {shell}...", end=" ", flush=True)
        # We simulate the UI spawning via shell: shell -c "command args"
        cmd_str = f"{WRAPPER_PATH} {' '.join(ARGS)}"
        input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")

        stdout, stderr, code = await run_mcp_command(
            shell, ["-c", cmd_str], input_data=input_bytes
        )

        if b"result" in stdout:
            print("✅ PASS")
        else:
            print(f"❌ FAIL (Code: {code})")
            print(f"    Stderr: {stderr.decode(errors='replace')}")
            return False
    return True


async def test_clean_room():
    print("\n[4/5] Testing Clean Room Environment...")
    # UI usually has a very stripped environment.
    # We provide only the bare minimum PATH.
    clean_env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "HOME": os.path.expanduser("~"),
        "USER": os.getlogin() if hasattr(os, "getlogin") else "user",
    }

    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")
    stdout, stderr, code = await run_mcp_command(
        WRAPPER_PATH, ARGS, input_data=input_bytes, env=clean_env
    )

    if b"result" in stdout:
        print("✅ PASS")
    else:
        print(f"❌ FAIL (Code: {code})")
        print(f"    Stderr: {stderr.decode(errors='replace')}")
        return False


async def test_handshake_latency():
    print("\n[5/5] Testing Handshake Latency...")
    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")

    start_time = time.perf_counter()
    # We use a custom reader to measure time to first byte
    process = await asyncio.create_subprocess_exec(
        WRAPPER_PATH,
        *ARGS,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    process.stdin.write(input_bytes)
    await process.stdin.drain()

    # Wait for first chunk
    await process.stdout.read(1)
    end_time = time.perf_counter()

    latency = (end_time - start_time) * 1000
    print(f"  Time to First Byte: {latency:.2f}ms")

    process.kill()
    await process.wait()

    if latency < 500:
        print("✅ PASS: Latency is within limits.")
        return True
    else:
        print("❌ FAIL: Latency too high (> 500ms).")
        return False


async def main():
    print("=" * 50)
    print("MCP HIGH-FIDELITY INTEGRATION SUITE")
    print("=" * 50)

    # Ensure daemon is running
    subprocess.run(["mega-memory-manager", "start"], check=True)

    results = []
    results.append(("CWD Independence", await test_cwd_independence()))
    results.append(("Stdout Pollution", await test_stdout_pollution()))
    results.append(("Shell Robustness", await test_shell_robustness()))
    results.append(("Clean Room Env", await test_clean_room()))
    results.append(("Handshake Latency", await test_handshake_latency()))

    print("\n" + "=" * 50)
    print("FINAL FIDELITY REPORT")
    print("=" * 50)
    all_passed = True
    for name, res in results:
        status = "✅ PASS" if res else "❌ FAIL"
        if not res:
            all_passed = False
        print(f"{name:25}: {status}")
    print("=" * 50)

    if all_passed:
        print(
            "\nCONCLUSION: The bridge is robust. The issue is likely in the UI's specific spawn environment or a cached config."
        )
    else:
        print("\nCONCLUSION: Critical integration flaws found. Fixes required.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
