# Qdrant Architecture

## Overview

Two isolated Qdrant instances are used.

---

## Local Qdrant

- Runs on localhost:6333
- Storage: local disk
- Collection: local_memory
- Vector size: 384
- Distance: cosine

Purpose:
- fast memory
- offline retrieval
- development + runtime cache

---

## Cloud Qdrant

- Remote hosted instance
- Collection: cloud_memory
- Vector size: 3072
- Distance: cosine

Purpose:
- durable memory
- high-quality retrieval
- long-term knowledge base

---

## Critical Rule

Each Qdrant instance has a fixed vector size.

Violating this causes:
- insert failures
- corrupted retrieval
- silent semantic errors

