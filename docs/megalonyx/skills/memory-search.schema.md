# Memory Search Response Schema Documentation

## Purpose
This file defines the JSON Schema for the `MemorySearchResponse` object, ensuring consistent data exchange between the memory search service and the agent.

## Logic & Structure
The schema defines a structured response object:
- **`results` (Required)**: An array of match objects.
    - `text` (Required): The actual content retrieved from memory.
    - `score` (Required): A numerical value between 0 and 1 representing the semantic similarity or relevance.
    - `metadata`: An optional object containing additional context about the retrieved item.
- **`query_latency` (Optional)**: A number representing the time taken to perform the search.

## Usage
- **API Implementation**: Used by the backend to validate the response sent back to the agent.
- **Agent Parsing**: Used by the agent to predictably access search results and their associated scores.
- **Testing**: Used to generate mock responses for unit tests.

## Original File
[config/skills/memory-search.schema.json](../../config/skills/memory-search.schema.json)
