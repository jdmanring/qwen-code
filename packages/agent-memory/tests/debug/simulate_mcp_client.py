import json
from typing import Any

from pydantic import BaseModel


class JSONRPCError(BaseModel):
    code: int
    message: str


class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict | None = None
    id: int | str | None = None


class JSONRPCResponse(BaseModel):
    jsonrpc: str
    id: int | str
    result: Any | None = None
    error: JSONRPCError | None = None


class JSONRPCNotification(BaseModel):
    jsonrpc: str
    method: str
    params: dict | None = None


class JSONRPCMessage(BaseModel):
    request: JSONRPCRequest | None = None
    response: JSONRPCResponse | None = None
    notification: JSONRPCNotification | None = None


# Since the actual Pydantic model in the client might be a Union,
# let's try to simulate it.


def simulate_client(line: str) -> None:
    try:
        data = json.loads(line)
        # In reality, the client uses a Union of models
        # We'll try to see which one it matches
        print(f"Testing line: {line}")

        # Try Request
        try:
            _req = JSONRPCRequest(**data)
            print("Matches Request")
            return
        except (ValueError, TypeError):
            pass

        # Try Response
        try:
            _res = JSONRPCResponse(**data)
            print("Matches Response")
            return
        except (ValueError, TypeError):
            pass

        # Try Notification
        try:
            _notif = JSONRPCNotification(**data)
            print("Matches Notification")
            return
        except (ValueError, TypeError):
            pass
        print("Matches nothing!")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing: {e}")


simulate_client('{"jsonrpc": "2.0", "id": "notifications/initialized"}')
simulate_client(
    '{"jsonrpc": "2.0", "id": "notifications/initialized", "error": {"code": -32601, "message": "Unknown method: None"}}'
)
