import asyncio
import os
import subprocess

from control_plane_daemon.mcp_manager import MCPManager


async def test_pdeathsig():
    print("\nTesting PDEATHSIG (Parent Death Signal)...")
    # We launch the bridge directly with the venv python to avoid shell wrapper issues
    python_bin = "sys.executable"
    bridge_script = (
        "stdio_socket_relay"
    )

    # Spawn a process that will be the parent
    # We use a small python script to spawn the bridge and then die
    parent_code = f"""
import subprocess
import sys
import time
subprocess.Popen(['{python_bin}', '{bridge_script}'])
time.sleep(5)
    """

    _proc = subprocess.Popen(
        [python_bin, "-c", parent_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for bridge to start
    await asyncio.sleep(2)

    # Find the bridge PID
    try:
        bridge_pid_str = (
            subprocess.check_output(["pgrep", "-f", "stdio_socket_relay.py"], text=True)
            .decode()
            .strip()
            .split("\n")[0]
        )

        print(f"Bridge PID: {bridge_pid_str}")

        # The parent is the process we spawned. It will die after 5 seconds.
        # We just wait for it to die.
        print("Waiting for parent to die...")
        await asyncio.sleep(6)

        # Check if bridge is still alive
        try:
            os.kill(int(bridge_pid_str), 0)
            print("❌ FAILURE: Bridge is still alive after parent death!")
            return False
        except ProcessLookupError:
            print("✅ SUCCESS: Bridge terminated after parent death.")
            return True
    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"Error during PDEATHSIG test: {e}")
        return False


async def test_daemon_crash():
    print("\nTesting Daemon Crash...")
    mgr = MCPManager()
    socket_path = os.path.expanduser("~/.local/share/megalonyx/sockets/megalonyx_memory.sock")

    try:
        session = await mgr._get_session("memory", socket_path=socket_path)
        print("Connected to daemon.")
    except (TimeoutError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"❌ FAILURE: Could not connect to daemon: {e}")
        return False

    print("Killing Memory Daemon...")
    subprocess.run(["pkill", "-9", "-f", "memory_daemon.py"])

    try:
        await session.call_tool("search", {"query": "test"})
        print("❌ FAILURE: Tool call succeeded after daemon crash!")
        return False
    except (TimeoutError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"✅ SUCCESS: Caught expected error after crash: {e}")
        return True
    finally:
        await mgr.close_all()


async def test_rapid_cycle():
    print("\nTesting Rapid Cycle (50x)...")
    socket_path = os.path.expanduser("~/.local/share/megalonyx/sockets/megalonyx_memory.sock")

    # Ensure daemon is actually running
    subprocess.run(["mega-memory-manager", "start"])
    await asyncio.sleep(2)

    for i in range(50):
        try:
            mgr = MCPManager()
            # We use a short timeout for the session get
            await asyncio.wait_for(
                mgr._get_session("memory", socket_path=socket_path), timeout=2.0
            )
            await mgr.close_all()
            if i % 10 == 0:
                print(f"Cycle {i}/50... OK")
        except (TimeoutError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
            print(f"❌ FAILURE at cycle {i}: {e}")
            return False

    print("✅ SUCCESS: 50 cycles completed without leaks.")
    return True


async def main():
    results = []
    results.append(("PDEATHSIG", await test_pdeathsig()))
    results.append(("Daemon Crash", await test_daemon_crash()))
    results.append(("Rapid Cycle", await test_rapid_cycle()))

    print("\n" + "=" * 30)
    print("CHAOS TEST RESULTS")
    print("=" * 30)
    for name, res in results:
        status = "✅ PASS" if res else "❌ FAIL"
        print(f"{name:20}: {status}")
    print("=" * 30)


if __name__ == "__main__":
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
    asyncio.run(main())
