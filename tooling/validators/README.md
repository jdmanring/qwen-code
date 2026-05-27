Validators that test the live stack against real services.
Unlike smoke tests, these require running infrastructure (Qdrant, Ollama, or the memory daemon).
Run manually before releases, not in standard CI.

Validators:
- validate_config.py -- checks that required runtime config files exist in the expected locations
- validate_stack.py -- full-stack validation: PyTorch, vLLM, embeddings, Qdrant insert/search, end-to-end RAG
- validate_telemetry.py -- verifies telemetry log format and event structure
- validate_vector_indexing.py -- indexes the project into Qdrant using tree-sitter symbol extraction + Ollama embeddings
- validate_workflow.py -- verifies the agentic workflow log records match expected structure
- test_installer.py -- pytest test that runs install-megalonyx-stack.sh in a fake HOME and verifies the result
