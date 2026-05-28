# Makefile for qwen-code

.PHONY: help install build build-sandbox build-all test lint format preflight clean start debug release run-npx create-alias

help:
	@echo "Makefile for qwen-code"
	@echo ""
	@echo "Usage:"
	@echo "  make install          - Install pnpm dependencies"
	@echo "  make build            - Build the main project"
	@echo "  make build-all        - Build the main project and sandbox"
	@echo "  make test             - Run the test suite"
	@echo "  make lint             - Lint the code"
	@echo "  make format           - Format the code"
	@echo "  make preflight        - Run the preflight verification"
	@echo "  make clean            - Remove generated files"
	@echo "  make start            - Start the Qwen Code CLI"
	@echo "  make debug            - Start the Qwen Code CLI in debug mode"
	@echo ""
	@echo "  make run-npx          - Run the CLI using npx (for testing the published package)"
	@echo "  make create-alias     - Create a 'qwen' alias for your shell"

install:
	pnpm install

build:
	pnpm run build


build-all:
	pnpm run build:all

test:
	pnpm run test

lint:
	pnpm run lint

format:
	pnpm run format

preflight:
	pnpm run preflight

clean:
	pnpm run clean

start:
	pnpm run start

debug:
	pnpm run debug


run-npx:
	npx https://github.com/QwenLM/qwen-code

create-alias:
	scripts/create_alias.sh
