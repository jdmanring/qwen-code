# CodeGraph Evaluation Dataset Documentation

## Purpose
This file contains a set of evaluation prompts and expected outcomes used to verify the accuracy and effectiveness of the `codegraph` skill. It serves as a benchmark for testing the system's ability to map natural language bug reports to specific code locations.

## Logic & Structure
The file is a JSON object containing an array of evaluation cases:
- `id`: Unique identifier for the test case.
- `prompt`: The simulated user request (e.g., "analyze issue #3185 in pallets/click").
- `expected_output`: The criteria for a successful response, typically specifying which `CodeScope` methods should be called (e.g., `cs.analyze_issue`) and the expected target code areas.
- `files`: A list of relevant files (currently empty in the sample).

## Usage
- **QA/Testing**: Used by automated test suites to run prompts through the agent and compare the actual tool calls and results against the `expected_output`.
- **Regression Testing**: Ensures that updates to the `codegraph` core or the agent's prompting logic do not degrade bug-analysis capabilities.

## Original File
[config/skills/codegraph/evals/evals.json](../../config/skills/codegraph/evals/evals.json)
