import json
import os

import pytest

SETTINGS_PATH = os.path.expanduser("~/.qwen/settings.json")


@pytest.fixture
def settings():
    with open(SETTINGS_PATH) as f:
        return json.load(f)


def test_mcp_servers_configuration(settings):
    """Verifies that all required MCP servers are correctly configured in settings.json."""
    mcp_servers = settings.get("mcpServers", {})

    # 1. GitHub Configuration
    assert "github" in mcp_servers
    github = mcp_servers["github"]
    assert github["command"] == "npx"
    assert "-y" in github["args"]
    assert "@modelcontextprotocol/server-github" in github["args"]
    assert "GITHUB_PERSONAL_ACCESS_TOKEN" in github["env"]
    assert github["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"] == "$GITHUB_TOKEN"

    # 2. Internet Search (formerly Tavily) Configuration
    assert "internet-search" in mcp_servers
    internet_search = mcp_servers["internet-search"]
    assert internet_search["command"] == "npx"
    assert "-y" in internet_search["args"]
    assert "tavily-mcp" in internet_search["args"]
    assert "TAVILY_API_KEY" in internet_search["env"]
    assert internet_search["env"]["TAVILY_API_KEY"] == "$TAVILY_API_KEY"

    # 3. Code-index Configuration
    assert "code-index" in mcp_servers
    code_index = mcp_servers["code-index"]
    assert code_index["command"] == "uvx"
    assert "code-index-mcp" in code_index["args"]

    # 4. Qdrant Configuration
    assert "mega-db" in mcp_servers
    qdrant = mcp_servers["mega-db"]
    assert qdrant["command"].endswith("python")
    assert "-m" in qdrant["args"]
    assert "qdrant_mcp.server" in qdrant["args"]
    assert "--qdrant-url" in qdrant["args"]
    assert "http://localhost:6333" in qdrant["args"]
    assert "--embedding-provider" in qdrant["args"]
    assert "sentence-transformers" in qdrant["args"]
    assert "--embedding-model" in qdrant["args"]
    assert "all-MiniLM-L6-v2" in qdrant["args"]


def test_env_variables_for_mcp(settings):
    """Verifies that the necessary environment variables are defined in the env section."""
    env = settings.get("env", {})

    assert "GITHUB_TOKEN" in env
    assert "TAVILY_API_KEY" in env
    assert "QDRANT_URL" in env
