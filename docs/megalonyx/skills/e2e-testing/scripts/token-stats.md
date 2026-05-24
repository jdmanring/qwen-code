# Token Statistics Utility Documentation

## Purpose
This file is a reference for `token-stats.py`, a utility script used to analyze token usage and cache efficiency from Qwen request logs.

## Logic & Structure
The script performs the following operations:
- **Log Loading**: Scans `~/.qwen/logs` for JSON files, sorting them to find the most recent entries.
- **Data Extraction**: Parses each log file to extract:
    - Timestamp and Model name.
    - `prompt_tokens` (Input).
    - `completion_tokens` (Output).
    - `cached_tokens` (from `prompt_tokens_details`).
- **Calculation**: Computes the "Cache Rate" as a percentage of input tokens that were served from cache.
- **Reporting**: Prints a formatted table showing per-request stats and a final "TOTAL" row with aggregated usage and overall cache efficiency.

## Usage
- **Performance Tuning**: Used by developers to monitor the impact of prompt caching on latency and cost.
- **Debugging**: Helps identify unexpectedly large prompts or inefficient caching patterns.
- **CLI**: Run via `python3 token-stats.py [count]` to see the last N requests.

## Original File
[config/skills/e2e-testing/scripts/token-stats.py](../../config/skills/e2e-testing/scripts/token-stats.py)
