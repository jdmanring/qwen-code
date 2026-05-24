# 🛠️ Installation Troubleshooting

This document provides solutions to common issues encountered during the deployment of the Mega Code stack.

## 1. `OSError: [Errno 28] No space left on device` during PyTorch Install

### Symptom
During the `[4/9] Setting up Python virtual environment` phase, the installer fails with a "No space left on device" error, even though the main physical drive has plenty of free space.

### Root Cause
The `pip` installer uses the system's temporary directory (usually `/tmp`) to unpack large wheels (like PyTorch). On many Linux distributions, `/tmp` is mounted as a `tmpfs` (RAM disk), which is significantly smaller than the physical disk. PyTorch's unpacked size often exceeds the available space in `/tmp`.

### Solution: Redirect `TMPDIR`
Redirect the temporary directory to a location on the physical disk before running the installer.

**Recommended Command:**
```bash
mkdir -p ~/.local/share/megalonyx/tmp
TMPDIR=~/.local/share/megalonyx/tmp ./install.sh
```

### Why this works
Setting the `TMPDIR` environment variable tells `pip` and other system utilities to use the specified path for temporary files instead of the default `/tmp` RAM disk. This leverages the full capacity of the physical drive.
