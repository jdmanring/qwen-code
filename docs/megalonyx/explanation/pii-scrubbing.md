# PII Scrubbing & Telemetry Masking

This document defines the technical specification for the local-first masking middleware used to protect sensitive data before it is transmitted to cloud-based LLMs or vector stores.

## 1. Objective
To enable the use of high-power cloud models (e.g., Gemini, GPT-4) while ensuring that Personally Identifiable Information (PII), secrets, and proprietary keys never leave the local environment.

## 2. The Masking Middleware Architecture

The scrubbing process is implemented as a middleware layer between the **Orchestrator** and the **Routing Plane**.

### 2.1 The Scrubbing Pipeline
Every outgoing request passes through the following sequence:
1. **Pattern Recognition**: Use of high-performance regex and NER (Named Entity Recognition) to identify potential PII (emails, IPs, API keys, paths).
2. **Tokenization**: Sensitive values are replaced with unique, non-reversible tokens (e.g., `USER_EMAIL_1`, `SECRET_KEY_A`).
3. **Mapping**: A local, encrypted map of `Token $\to$ Original Value` is stored in the transient session state.
4. **Transmission**: The scrubbed text is sent to the cloud provider.
5. **Re-Hydration**: Upon receiving the response, the middleware replaces the tokens with the original values before presenting the result to the user.

### 2.2 Masking Strategies
- **Hard Masking**: Replacing data with generic labels (e.g., `[REDACTED]`). Used for high-sensitivity fields.
- **Soft Masking**: Replacing data with consistent tokens. Used for maintaining the semantic structure of the prompt.

## 3. Implementation Status
- **[Current]**: Basic regex-based stripping of common API key patterns.
- **[Target]**: Full NER-based masking middleware integrated into the `Routing Plane`, supporting custom scrubbing rules per project.
