#!/usr/bin/env python3

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = "1.0"


@dataclass
class MemoryRecord:
    text: str
    tier: str
    source: str = "qwen-code"
    importance: int = 5
    metadata: dict[str, Any] = field(default_factory=dict)

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        """Validates the record integrity."""
        if not self.text:
            raise ValueError("Memory record text cannot be empty.")
        if self.tier not in ["local", "cloud"]:
            raise ValueError(f"Invalid tier: {self.tier}")
        if not (1 <= self.importance <= 10):
            raise ValueError(f"Importance must be between 1 and 10. Got: {self.importance}")
        if not self.id:
            raise ValueError("Memory record ID cannot be empty.")


def serialize(record: MemoryRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "text": record.text,
        "tier": record.tier,
        "source": record.source,
        "importance": record.importance,
        "metadata": record.metadata,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "schema_version": record.schema_version,
    }


def deserialize(data: dict[str, Any]) -> MemoryRecord:
    """Reconstructs a MemoryRecord from a dictionary."""
    try:
        # Extract fields, providing defaults for missing ones to handle schema evolution
        record = MemoryRecord(
            text=data["text"],
            tier=data["tier"],
            source=data.get("source", "qwen-code"),
            importance=data.get("importance", 5),
            metadata=data.get("metadata", {}),
            id=data.get("id", str(uuid.uuid4())),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            schema_version=data.get("schema_version", SCHEMA_VERSION),
        )
        # Validate the reconstructed record
        record.validate()
        return record
    except KeyError as e:
        raise ValueError(f"Missing required field in memory record: {e}") from e
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to deserialize memory record: {e}") from e
