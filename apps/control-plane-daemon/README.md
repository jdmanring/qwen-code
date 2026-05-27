The control-plane-daemon is the Megalonyx orchestration service.
It receives a user prompt, classifies the intent (one of six types), decomposes compound tasks into atomic jobs, selects an execution profile, and dispatches to the appropriate tool or agent.
Entry point: src/control_plane_daemon/control_plane.py (ControlPlane class).
Python package: control_plane_daemon -- importable via the uv workspace after uv sync --all-packages.
