# Bug Analysis Workflows Documentation

## Purpose
This file defines the patterns and workflows for tracing GitHub bugs to specific code locations using the CodeScope graph and vector infrastructure. It provides a systematic approach to root cause analysis by combining semantic search with structural graph traversal.

## Logic & Structure
The document is structured as a guide containing:
- **Quick Start**: Basic Python implementation for analyzing top bugs.
- **Single Issue Analysis**: Detailed breakdown of the `BugAnalysisResult` object and the process of parsing issues for paths, functions, and commits.
- **Batch Bug Hotspot Analysis**: Logic for aggregating bug associations across files, functions, and modules to identify "buggy" hotspots.
- **Custom Analysis Pipelines**: Methods for manual bug-to-code mapping and linking bugs to specific git commits.
- **Integration**: Strategies for combining bug analysis with structural analysis (e.g., checking if a bug is in a "bridge function" or calculating the impact of a fix).

## Usage
- **Developers**: Use this as a manual for implementing automated bug-triaging tools.
- **AI Agents**: Use these patterns to perform root-cause analysis on GitHub issues by leveraging the `codegraph` Python library.
- **CLI**: Provides a quick reference for `codegraph fetch-issue`, `analyze-bug`, and `analyze-bugs` commands.

## Original File
[config/skills/codegraph/bug-analysis.md](../../config/skills/codegraph/bug-analysis.md)
