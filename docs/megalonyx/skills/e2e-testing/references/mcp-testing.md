# MCP Server E2E Testing Documentation

## Purpose
This file provides instructions for setting up and executing end-to-end (E2E) tests for Model Context Protocol (MCP) tool servers within the Qwen Code environment.

## Logic & Structure
The guide covers:
- **Configuration**: Explicitly states that MCP servers must be configured in `.qwen/settings.json` under `mcpServers`.
- **Setup**: Step-by-step instructions for creating a temporary git repository and configuration file for testing.
- **Server Implementation**: Guidance on using `scripts/mcp-test-server.js` as a template for creating zero-dependency JSON-RPC servers.
- **Verification**: How to sanity-check a server using raw JSON-RPC pipes and how to verify server connectivity via the CLI's JSON output.
- **Troubleshooting**: A list of common reasons why MCP servers might fail to load.

## Usage
- **QA Engineers**: Use this to validate that new MCP servers are correctly integrated and functional.
- **Developers**: Use the provided setup patterns to test new tool definitions before deploying them to a production server.

## Original File
[config/skills/e2e-testing/references/mcp-testing.md](../../config/skills/e2e-testing/references/mcp-testing.md)
