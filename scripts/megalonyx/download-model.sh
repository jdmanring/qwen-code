#!/usr/bin/env bash
set -e

BASE="https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-AWQ/resolve/main"
DEST="$HOME/.cache/huggingface/hub/models--Qwen--Qwen2.5-Coder-14B-Instruct-AWQ/blobs"

mkdir -p "$DEST"

echo "Downloading shard 1 of 3..."
aria2c -c -x 10 -s 10 -d "$DEST" "$BASE/model-00001-of-00003.safetensors"

echo "Downloading shard 2 of 3..."
aria2c -c -x 10 -s 10 -d "$DEST" "$BASE/model-00002-of-00003.safetensors"

echo "Downloading shard 3 of 3..."
aria2c -c -x 10 -s 10 -d "$DEST" "$BASE/model-00003-of-00003.safetensors"

echo "All shards downloaded."
