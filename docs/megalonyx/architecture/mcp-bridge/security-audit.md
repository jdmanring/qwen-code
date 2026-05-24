# MCP Bridge Security Audit

## Overview
Since the Memory Daemon opens a Unix Domain Socket (UDS) that can be accessed by any process on the local system, a robust security model is required to prevent unauthorized access to the semantic memory.

## Identity Verification via `SO_PEERCRED`
The Sovereign Bridge does not rely on passwords or API keys for local communication. Instead, it uses **Kernel-Level Identity Verification**.

### The Mechanism
When a client connects to the UDS socket, the daemon uses the `getsockopt` system call with the `SO_PEERCRED` option:
```python
creds = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('iii'))
pid, uid, gid = struct.unpack('iii', creds)
```

### The Verification Logic
The kernel provides the `pid` (Process ID), `uid` (User ID), and `gid` (Group ID) of the connecting process. The daemon performs a strict check:
- **Rule**: `connecting_uid == daemon_uid`
- **Action**: If the UIDs do not match, the connection is immediately terminated, and a warning is logged.

This ensures that only processes running under the same user account as the daemon can interact with the memory system, effectively neutralizing attacks from other users on the same machine.

## File System Permissions
In addition to identity verification, the bridge employs the "Principle of Least Privilege" at the file system level.

### Socket Hardening
Upon creating the socket file at `~/.local/share/megalonyx/tmp/qwen_memory.sock`, the daemon immediately applies strict permissions:
- **Command**: `os.chmod(socket_path, 0o600)`
- **Effect**: This sets the permissions to `rw-------`.
- **Result**: Only the owner of the file (the user) can read from or write to the socket. Any attempt by another user to even *attempt* a connection will be blocked by the OS kernel before the `SO_PEERCRED` check is even reached.

## Security Summary Table

| Layer | Mechanism | Protection Provided |
| :--- | :--- | :--- |
| **OS Layer** | `chmod 0600` | Prevents other users from accessing the socket file. |
| **Kernel Layer** | `SO_PEERCRED` | Verifies the exact UID of the connecting process. |
| **Application Layer** | UID Comparison | Hard-rejects any connection not matching the daemon owner. |

## Threat Model Analysis
- **Local User Attack**: Blocked by `chmod 0600` and `SO_PEERCRED`.
- **Remote Network Attack**: Impossible; UDS sockets are not reachable via TCP/IP.
- **Privilege Escalation**: The daemon runs as a standard user; it does not require root privileges, limiting the blast radius of any potential exploit.
