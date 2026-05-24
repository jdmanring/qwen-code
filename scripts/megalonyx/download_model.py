#!/usr/bin/env python3
"""Download Qwen2.5-Coder-14B-Instruct-AWQ with per-file progress."""

from huggingface_hub import list_repo_files, snapshot_download

MODEL = "Qwen/Qwen2.5-Coder-14B-Instruct-AWQ"

print(f"Model: {MODEL}")
print("Checking files in repo...")

files = list(list_repo_files(MODEL))
print(f"Total files to download: {len(files)}")
for f in files:
    print(f"  {f}")

print("\nStarting download (already-cached files will be skipped)...")
print("Cache: ~/.cache/huggingface/hub/\n")

path = snapshot_download(
    repo_id=MODEL,
    local_files_only=False,
    force_download=False,
)

print(f"\nDone. Model stored at:\n{path}")
