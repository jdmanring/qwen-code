"""JSON lines utilities."""

from __future__ import annotations

import json


def serialize_json_line(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def parse_json_line(line: str) -> object:
    return json.loads(line)
