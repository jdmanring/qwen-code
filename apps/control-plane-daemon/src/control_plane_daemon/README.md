The control_plane_daemon Python package. All modules here are importable as control_plane_daemon.<module>.

Key modules:
- control_plane.py -- top-level orchestrator; instantiates and wires all components
- intent_classifier.py -- classifies prompt into one of six intent types via LLM
- task_decomposer.py -- breaks compound intents into atomic jobs
- execution_profile_selector.py -- scores and ranks agent profiles for a given intent + prompt
- policy_engine.py -- evaluates intent + risk profile against configured rules
- job_state_manager.py -- tracks job lifecycle (created -> running -> complete)
- tool_executor.py -- bridges classified intent to subprocess skill execution
- mcp_manager.py -- client-side manager for multiple MCP server sessions
- model_router.py -- CLI entry point: reads prompt, calls ControlPlane, streams output

Do not import from this package using relative paths outside the package -- always use the full module name.
