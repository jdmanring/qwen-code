# Environment Variables Configuration

## Component Identity
The `.env` file (mirrored here as `.env.md`) contains the sensitive API keys and connection strings required for the Megalonyx Stack to interact with external LLM providers, vector databases, and third-party services.

## Technical Specification
The environment configuration is a collection of key-value pairs used to populate the `env` block in `settings.json`.

### Primary Categories
- **LLM API Keys**: Keys for various providers including `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `MISTRAL_API_KEY`, and `LONGCAT_API_KEY`.
- **Vector Store**: 
  - `QDRANT_LOCAL_URL`: Connection string for the local Qdrant instance.
  - `QDRANT_CLOUD_URL` & `QDRANT_API_KEY`: Credentials for the cloud-tier memory storage.
- **Search & Tools**:
  - `TAVILY_API_KEY`: For internet search capabilities.
  - `GITHUB_TOKEN`: For repository and issue management.

### Security Note
This file contains secrets and should **never** be committed to version control. The mirrored version in `docs/` serves as a template/reference for the *types* of keys required, not as a storage for the actual values.

## Interdependencies
- **`settings.json`**: The system resolves the `$VARIABLE` placeholders in `settings.json` using the values found in this file.
- **MCP Servers**: Servers like `github` and `internet-search` ingest these keys to authenticate their requests.

## Symmetry Link
[Original Config: `config/.env`](../../config/.env)
