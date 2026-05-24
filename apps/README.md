This directory contains Megalonyx application services — long-running processes with entry points.
Currently: control-plane-daemon, which receives tasks, classifies intent, decomposes them into jobs, and dispatches to execution profiles.
Python packages here follow the src/ layout and are members of the uv workspace.
Do not put shared libraries here — those belong in packages/.
