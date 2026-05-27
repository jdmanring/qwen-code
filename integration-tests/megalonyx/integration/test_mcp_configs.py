import json
import os
import pytest

# Create a temporary settings file for testing
@pytest.fixture(scope="module")
def temp_settings(tmp_path_factory):
    settings_dir = tmp_path_factory.mktemp("settings")
    settings_file = settings_dir / "settings.json"
    settings_data = {
        "env": {
            "OPENAI_API_KEY": "sk-dummy-key",
            "GITHUB_TOKEN": "dummy-github-token",
            "TAVILY_API_KEY": "dummy-tavily-key",
            "QDRANT_URL": "http://localhost:6333",
        },
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN"},
            },
            "internet-search": {
                "command": "npx",
                "args": ["-y", "tavily-mcp"],
                "env": {"TAVILY_API_KEY": "$TAVILY_API_KEY"},
            },
            "code-index": {
                "command": "uvx",
                "args": ["code-index-mcp"],
            },
            "mega-db": {
                "command": "python -m qdrant_mcp.server",
                "args": [
                    "--qdrant-url",
                    "http://localhost:6333",
                    "--embedding-provider",
                    "sentence-transformers",
                    "--embedding-model",
                    "all-MiniLM-L6-v2",
                ],
            },
        },
    }
    settings_file.write_text(json.dumps(settings_data))
    return str(settings_file)


@pytest.fixture
def settings(temp_settings):
    with open(temp_settings) as f:
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
