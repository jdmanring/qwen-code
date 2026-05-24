# PR Impact Analysis Documentation

## Purpose
This document outlines the workflow for analyzing the structural risk and impact of open Pull Requests (PRs) using the `codegraph-ai` tool. It aims to prioritize PR reviews based on technical risk rather than just chronological order.

## Logic & Structure
The workflow is described as a multi-step pipeline:
1. **Environment Setup**: Virtual environment and dependency installation.
2. **PR Fetching**: Using `GitHubClient` to retrieve open PRs and their corresponding branches.
3. **Indexing**: Creating a `.codegraph` index of the target repository.
4. **Review Pipeline**: The `pr_review.py` entry point which computes risk scores and detects conflicts.
5. **Risk Scoring**: Detailed breakdown of "File-level signals" (config changes, interface changes) and "Function-level signals" (blast radius, test coverage).
6. **Cross-PR Analysis**: Using `CrossPRAnalyzer` to detect conflicts via file overlap, function overlap, and dependency chain overlap.

## Usage
- **Maintainers**: Run the `codegraph pr-review prepare` and `label` commands to automatically categorize PRs into "Auto-merge", "Independent Review", or "Conflicting Groups".
- **CI/CD**: Integrate this pipeline into GitHub Actions to automatically label PRs with risk levels (CRITICAL, HIGH, etc.).

## Original File
[config/skills/codegraph/pr-analysis.md](../../config/skills/codegraph/pr-analysis.md)
