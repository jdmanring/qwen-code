# Embedding System

## Overview

The system uses a dual embedding architecture:

---

## Local Embeddings

- Model: sentence-transformers/all-MiniLM-L6-v2
- Dimensions: 384
- Runs locally
- No API dependency

Use cases:
- fast retrieval
- frequent writes
- ephemeral memory

---

## Cloud Embeddings

- Model: gemini-embedding-2
- Provider: Google Gemini API
- Dimensions: 3072
- Rate limited

Use cases:
- long-term memory
- high-quality semantic search
- cross-session reasoning

---

## Rule: NEVER MIX VECTOR SPACES

| System | Model | Dim |
|--------|------|-----|
| Local | MiniLM | 384 |
| Cloud | Gemini | 3072 |

Mixing breaks retrieval.

---

## Routing Rules

All embeddings MUST go through:

embedding-router.py

- embed_local() => Qdrant local
- embed_google() => Qdrant cloud

