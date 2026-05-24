#!/bin/bash
set -euo pipefail

# Verification Gate — standalone runner for the three quality gates.
# Mirrors the gate logic in upstream_ingest_pipeline.py for use outside the full pipeline.
#
# Usage:
#   ./tooling/sync-upstreams/verification-gate.sh
#
# Run from the repo root. Must be on the integration branch.

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_error()   { echo -e "${RED}[FAIL]${NC} $1" >&2; }

# Resolves ruff using the same priority as upstream_ingest_pipeline.py:
#   1. uv run ruff  (project-pinned version — preferred)
#   2. $RUFF_BIN    (explicit CI override)
#   3. PATH ruff    (last resort)
run_ruff() {
    if command -v uv &>/dev/null; then
        uv run ruff "$@"
    elif [ -n "${RUFF_BIN:-}" ]; then
        "$RUFF_BIN" "$@"
    elif command -v ruff &>/dev/null; then
        ruff "$@"
    else
        log_error "ruff not found. Install uv (https://docs.astral.sh/uv/) or set RUFF_BIN=/path/to/ruff"
        exit 1
    fi
}

gate_lint() {
    log_info "Gate 1/3: Ruff lint..."
    if ! run_ruff check .; then
        log_error "Lint gate failed. Run: ruff check --fix ."
        return 1
    fi
    log_success "Lint gate passed."
}

gate_symmetry() {
    log_info "Gate 2/3: Symmetry check (config ↔ docs)..."
    if ! python3 tooling/symmetry_check.py; then
        log_error "Symmetry gate failed. config/ and docs/ are out of sync."
        return 1
    fi
    log_success "Symmetry gate passed."
}

gate_boot() {
    log_info "Gate 3/3: Boot test (uv lock --check)..."
    if ! uv lock --check; then
        log_error "Boot gate failed — lockfile out of sync. Run: uv lock"
        return 1
    fi
    log_success "Boot gate passed."
}

main() {
    gate_lint
    gate_symmetry
    gate_boot
    echo ""
    log_success "All gates passed."
}

main "$@"
