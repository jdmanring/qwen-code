#!/bin/bash
set -e
echo "Merging upstream changes into upstream-main..."
git checkout upstream-main
git pull upstream main
echo "Upstream changes merged into upstream-main."
