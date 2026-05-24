#!/bin/bash
# Unified Test Runner for Megalonyx

# Set PYTHONPATH to include the skills directory
export PYTHONPATH="$PYTHONPATH:$(pwd)/.qwen/skills"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Use project's venv if it exists, otherwise fallback to system python3
if [ -f "$(pwd)/.venv/bin/python3" ]; then
    PYTHON_BIN="$(pwd)/.venv/bin/python3"
else
    PYTHON_BIN="python3"
fi

echo -e "${BOLD}🚀 Starting Full System Verification...${NC}\n"

# 1. Infrastructure Check
echo -e "${BOLD}Step 1: Infrastructure & Dependency Check${NC}"
if bash tests/validators/test.sh; then
    echo -e "${GREEN}✓ Infrastructure healthy${NC}\n"
else
    echo -e "${RED}⚠ Infrastructure check had warnings/failures (skipping to core tests)${NC}\n"
fi

# 2. MCP Configuration & Communication
echo -e "${BOLD}Step 2: MCP Tool Layer Verification${NC}"
if $PYTHON_BIN -m pytest tests/integration/test_mcp_configs.py tests/integration/test_tavily_mcp.py; then
    echo -e "${GREEN}✓ MCP tool layer verified${NC}\n"
else
    echo -e "${RED}✗ MCP tool layer verification failed${NC}"
    exit 1
fi

# 3. Orchestration Tests
echo -e "${BOLD}Step 3: Agent Orchestration Tests${NC}"
if $PYTHON_BIN -m pytest tests/integration/test_orchestration.py; then
    echo -e "${GREEN}✓ Basic orchestration logic verified${NC}\n"
else
    echo -e "${RED}✗ Basic orchestration tests failed${NC}"
    exit 1
fi

# 4. State-Aware Orchestration Tests
echo -e "${BOLD}Step 4: State-Aware Orchestration Tests${NC}"
if $PYTHON_BIN -m pytest tests/integration/test_state_orchestration.py; then
    echo -e "${GREEN}✓ State-aware logic verified${NC}\n"
else
    echo -e "${RED}✗ State-aware tests failed${NC}"
    exit 1
fi

# 5. Chaos & Resilience Tests
echo -e "${BOLD}Step 5: Chaos & Resilience Tests${NC}"
if $PYTHON_BIN -m pytest tests/e2e/test_chaos.py tests/e2e/test_resilience_and_guards.py; then
    echo -e "${GREEN}✓ Resilience layer and guards verified${NC}\n"
else
    echo -e "${RED}✗ Chaos or Guard tests failed${NC}"
    exit 1
fi

# 6. RAG Pipeline Tests
echo -e "${BOLD}Step 6: RAG Pipeline Tests${NC}"
if $PYTHON_BIN -m pytest tests/integration/test_rag.py tests/integration/test_qdrant_mcp.py; then
    echo -e "${GREEN}✓ RAG pipeline verified${NC}\n"
else
    echo -e "${RED}✗ RAG tests failed${NC}"
    exit 1
fi

# 7. Workflow Audit
echo -e "${BOLD}Step 7: Workflow Telemetry Audit${NC}"
if $PYTHON_BIN tests/validators/validate_workflow.py; then
    echo -e "${GREEN}✓ Workflow audit completed${NC}\n"
else
    echo -e "${RED}✗ Workflow audit failed${NC}"
    exit 1
fi

echo -e "\n${BOLD}${GREEN}✨ ALL SYSTEMS GO: Megalonyx is fully verified!${NC}"
