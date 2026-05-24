"""
MCP bridge reliability suite.

Validates the memory MCP bridge under environmental edge cases:
- CWD independence
- Stdout pollution (only JSON-RPC on stdout)
- Shell compatibility
- Clean-room environment isolation
- Handshake latency

Run against any deployment to catch configuration regressions.
"""

import asyncio
import json
import os
import subprocess
import sys
import time

# mega-memory starts the MCP server; no separate bridge script needed
COMMAND = "mega-memory"
ARGS: list[str] = []

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
        stdout, stderr, code = await run_mcp_command(COMMAND, ARGS, input_data=input_bytes, cwd=d)

        if b"result" in stdout and b"protocolVersion" in stdout:
            print("PASS")
        else:
            print(f"FAIL (Code: {code})")
            print(f"    Stderr: {stderr.decode(errors='replace')}")
            return False
    return True


async def test_stdout_pollution():
    print("\n[2/5] Testing Stdout Pollution Audit...")
    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")
    stdout, stderr, code = await run_mcp_command(COMMAND, ARGS, input_data=input_bytes)

    if not stdout:
        print("FAIL: No output received.")
        return False

    lines = stdout.decode(errors="replace").strip().split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if not line.startswith("{"):
            print(f"FAIL: Pollution detected at line {i + 1}: {repr(line)}")
            return False

    print("PASS: Stdout is clean JSON-RPC.")
    return True


async def test_shell_robustness():
    print("\n[3/5] Testing Shell Robustness...")
    shells = ["/bin/sh", "/bin/bash"]

    for shell in shells:
        print(f"  Testing Shell: {shell}...", end=" ", flush=True)
        cmd_str = f"{COMMAND} {' '.join(ARGS)}"
        input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")

        stdout, stderr, code = await run_mcp_command(shell, ["-c", cmd_str], input_data=input_bytes)

        if b"result" in stdout:
            print("PASS")
        else:
            print(f"FAIL (Code: {code})")
            print(f"    Stderr: {stderr.decode(errors='replace')}")
            return False
    return True


async def test_clean_room():
    print("\n[4/5] Testing Clean Room Environment...")
    clean_env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "HOME": os.path.expanduser("~"),
        "USER": os.getlogin() if hasattr(os, "getlogin") else "user",
    }

    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")
    stdout, stderr, code = await run_mcp_command(
        COMMAND, ARGS, input_data=input_bytes, env=clean_env
    )

    if b"result" in stdout:
        print("PASS")
        return True
    else:
        print(f"FAIL (Code: {code})")
        print(f"    Stderr: {stderr.decode(errors='replace')}")
        return False


async def test_handshake_latency():
    print("\n[5/5] Testing Handshake Latency...")
    input_bytes = (json.dumps(INIT_REQUEST) + "\n").encode("utf-8")

    start_time = time.perf_counter()
    process = await asyncio.create_subprocess_exec(
        COMMAND,
        *ARGS,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    process.stdin.write(input_bytes)
    await process.stdin.drain()

    await process.stdout.read(1)
    end_time = time.perf_counter()

    latency = (end_time - start_time) * 1000
    print(f"  Time to First Byte: {latency:.2f}ms")

    process.kill()
    await process.wait()

    if latency < 500:
        print("PASS: Latency is within limits.")
        return True
    else:
        print("FAIL: Latency too high (> 500ms).")
        return False


async def main():
    print("=" * 50)
    print("MCP BRIDGE RELIABILITY SUITE")
    print("=" * 50)

    subprocess.run(["mega-memory", "start"], check=True)

    results = []
    results.append(("CWD Independence", await test_cwd_independence()))
    results.append(("Stdout Pollution", await test_stdout_pollution()))
    results.append(("Shell Robustness", await test_shell_robustness()))
    results.append(("Clean Room Env", await test_clean_room()))
    results.append(("Handshake Latency", await test_handshake_latency()))

    print("\n" + "=" * 50)
    print("RELIABILITY REPORT")
    print("=" * 50)
    all_passed = True
    for name, res in results:
        status = "PASS" if res else "FAIL"
        if not res:
            all_passed = False
        print(f"{name:25}: {status}")
    print("=" * 50)

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
