#!/usr/bin/env bash
# test.sh -- verify the qwen-code-stack is fully operational
# Usage: bash scripts/test.sh
# Exit code: 0 = all tests passed, 1 = one or more failures

set -uo pipefail

export PATH="$HOME/.local/share/npm/bin:$PATH"

SETTINGS="$HOME/.qwen/settings.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

PASS=0; FAIL=0; SKIP=0

pass()    { echo -e "  ${GREEN}${NC} $1"; PASS=$((PASS + 1)); }
fail()    { echo -e "  ${RED}${NC} $1"; FAIL=$((FAIL + 1)); }
skip()    { echo -e "  ${YELLOW}-${NC} $1"; SKIP=$((SKIP + 1)); }
section() { echo -e "\n${BOLD}${BLUE}-- $1 --${NC}"; }

get_env_key() {
    python3 -c "
import json, sys
try:
    d = json.load(open('$SETTINGS'))
    print(d.get('env', {}).get('$1', ''))
except Exception:
    print('')
" 2>/dev/null
}

get_mcp_env() {
    python3 -c "
import json, sys
try:
    d = json.load(open('$SETTINGS'))
    print(d.get('mcpServers', {}).get('$1', {}).get('env', {}).get('$2', ''))
except Exception:
    print('')
" 2>/dev/null
}

test_mcp() {
    local name="$1"; shift
    local msg='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"stack-test","version":"1.0"}}}'
    local response
    response=$(echo "$msg" | timeout 20 "$@" 2>/dev/null | head -1)
    if [[ -n "$response" ]] && echo "$response" | python3 -c "
import json, sys
d = json.load(sys.stdin)
sys.exit(0 if 'result' in d else 1)
" 2>/dev/null; then
        pass "$name MCP server responds"
    else
        fail "$name MCP server -- no valid response (crash, timeout, or bad JSON)"
    fi
}

# -- 1. Dependencies -----------------------------------------------------------
section "1. Dependencies"

for cmd in node npm python3 uvx rg aria2c git curl; do
    if path=$(which "$cmd" 2>/dev/null); then
        pass "$cmd -- $path"
    else
        fail "$cmd -- not found in PATH"
    fi
done

if qwen_path=$(which qwen 2>/dev/null); then
    qwen_ver=$(qwen --version 2>&1 | head -1)
    pass "qwen -- $qwen_path ($qwen_ver)"
else
    fail "qwen -- not found (check npm user prefix is in PATH: ~/.local/share/npm/bin)"
fi

# -- 2. Configuration ----------------------------------------------------------
section "2. Configuration"

if [[ -f "$SETTINGS" ]]; then
    pass "~/.qwen/settings.json exists"
else
    fail "~/.qwen/settings.json not found -- copy settings.example.json and fill in API keys"
fi

if python3 -c "import json; json.load(open('$SETTINGS'))" 2>/dev/null; then
    pass "settings.json is valid JSON"
else
    fail "settings.json is invalid JSON -- run: python3 -m json.tool ~/.qwen/settings.json"
fi

for key in GEMINI_API_KEY GROQ_API_KEY OPENROUTER_API_KEY NVIDIA_API_KEY; do
    val=$(get_env_key "$key")
    if [[ -z "$val" || "$val" == *"YOUR_"* ]]; then
        fail "$key -- not set in settings.json"
    else
        pass "$key -- set"
    fi
done

PROJ_QWEN="$PROJECT_DIR/QWEN.md"
GLOBAL_QWEN="$HOME/.qwen/QWEN.md"
if [[ ! -f "$PROJ_QWEN" ]]; then
    fail "QWEN.md missing from project directory"
elif [[ ! -f "$GLOBAL_QWEN" ]]; then
    fail "~/.qwen/QWEN.md missing -- run: yes | cp -f $PROJ_QWEN $GLOBAL_QWEN"
elif diff -q "$PROJ_QWEN" "$GLOBAL_QWEN" &>/dev/null; then
    pass "QWEN.md in sync (project <=> ~/.qwen/)"
else
    fail "QWEN.md out of sync -- run: yes | cp -f $PROJ_QWEN $GLOBAL_QWEN"
fi

# -- 3. Local model (vLLM) -----------------------------------------------------
section "3. Local model (vLLM)"

if curl -sf http://localhost:8000/health &>/dev/null; then
    pass "vLLM running on port 8000"
    model=$(curl -sf http://localhost:8000/v1/models \
        | python3 -c "import json,sys; print(json.load(sys.stdin)['data'][0]['id'])" 2>/dev/null)
    if [[ -n "$model" ]]; then
        pass "Model loaded: $model"
    else
        fail "vLLM running but /v1/models returned no models"
    fi
else
    skip "vLLM not running -- start with 'qwenstart' or 'qwencode --local' then re-run"
fi

# -- 4. External APIs ----------------------------------------------------------
section "4. External APIs"

check_api() {
    local name="$1" key="$2" url="$3"
    if [[ -z "$key" || "$key" == *"YOUR_"* ]]; then
        skip "$name -- key not set"
        return
    fi
    local http_code
    http_code=$(curl -sf -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $key" "$url" 2>/dev/null)
    if [[ "$http_code" == "200" ]]; then
        pass "$name -- HTTP 200"
    else
        fail "$name -- HTTP ${http_code:-000} (check API key and quota)"
    fi
}

GROQ_KEY=$(get_env_key "GROQ_API_KEY")
OR_KEY=$(get_env_key "OPENROUTER_API_KEY")
NV_KEY=$(get_env_key "NVIDIA_API_KEY")
GEM_KEY=$(get_env_key "GEMINI_API_KEY")

check_api "Groq (Llama 4 Scout)"       "$GROQ_KEY" "https://api.groq.com/openai/v1/models"
check_api "OpenRouter"                  "$OR_KEY"   "https://openrouter.ai/api/v1/models"
check_api "NVIDIA NIM (Llama 3.1 70B)" "$NV_KEY"   "https://integrate.api.nvidia.com/v1/models"

if [[ -z "$GEM_KEY" || "$GEM_KEY" == *"YOUR_"* ]]; then
    skip "Gemini -- key not set"
else
    http_code=$(curl -sf -o /dev/null -w "%{http_code}" \
        "https://generativelanguage.googleapis.com/v1beta/models?key=$GEM_KEY" 2>/dev/null)
    if [[ "$http_code" == "200" ]]; then
        pass "Gemini 2.0 Flash -- HTTP 200"
    else
        fail "Gemini 2.0 Flash -- HTTP ${http_code:-000} (check API key)"
    fi
fi

# -- 5. MCP servers ------------------------------------------------------------
section "5. MCP servers"

GH_TOKEN=$(get_mcp_env "github" "GITHUB_PERSONAL_ACCESS_TOKEN")
if [[ -n "$GH_TOKEN" && "$GH_TOKEN" != *"YOUR_"* ]]; then
    GITHUB_PERSONAL_ACCESS_TOKEN="$GH_TOKEN" \
        test_mcp "github" npx -y @modelcontextprotocol/server-github
else
    skip "github MCP -- GITHUB_PERSONAL_ACCESS_TOKEN not set in settings.json"
fi

TAVILY_KEY=$(get_mcp_env "tavily-search" "TAVILY_API_KEY")
if [[ -n "$TAVILY_KEY" && "$TAVILY_KEY" != *"YOUR_"* ]]; then
    TAVILY_API_KEY="$TAVILY_KEY" \
        test_mcp "tavily-search" npx -y tavily-mcp
else
    skip "tavily-search MCP -- TAVILY_API_KEY not set in settings.json"
fi

test_mcp "code-index" uvx code-index-mcp

QDRANT_URL=$(get_mcp_env "mega-db" "QDRANT_URL")
if [[ -n "$QDRANT_URL" ]]; then
    test_mcp "mega-db" python3 -m qdrant_mcp.server --qdrant-url "$QDRANT_URL" --embedding-provider sentence-transformers --embedding-model all-MiniLM-L6-v2
else
    skip "mega-db MCP -- QDRANT_URL not set in settings.json"
fi


# -- Summary -------------------------------------------------------------------
echo -e "\n${BOLD}Results:${NC}  ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}  ${YELLOW}${SKIP} skipped${NC}"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo -e "${RED}${BOLD}Stack has failures -- resolve before running 'qwencode'${NC}"
    exit 1
else
    echo -e "${GREEN}${BOLD}Stack is healthy${NC}"
    exit 0
fi
