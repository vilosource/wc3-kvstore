"""Frozen HTTP wire contract for wc3-kvstore.

This module defines the single source of truth for the HTTP contract
between the server (n2) and client (n3). The contract is frozen and
must not be modified by downstream tasks.

HTTP Semantics:
----------------
- GET /health → 200, body {"status": "ok"}
- PUT /kv/<key> with JSON {"value": <v>} → 200, body {"key": <key>, "value": <v>}
  - Request body without a "value" key → 400, body {"error": "value is required"}
- GET /kv/<key> → 200 body {"key": <key>, "value": <v>, "found": True} if key exists
  - Else 404 body {"key": <key>, "found": False}
- DELETE /kv/<key> → 204 with empty body if key existed
  - Else 404 body {"key": <key>, "found": False}
"""

HEALTH_PATH: str = "/health"
VALUE_REQUIRED: str = "value is required"

__all__ = [
    "HEALTH_PATH",
    "VALUE_REQUIRED",
    "kv_path",
    "health_body",
    "set_request",
    "set_response",
    "get_response",
    "missing_response",
    "error_body",
]


def kv_path(key: str) -> str:
    return f"/kv/{key}"


def health_body() -> dict:
    return {"status": "ok"}


def set_request(value) -> dict:
    return {"value": value}


def set_response(key, value) -> dict:
    return {"key": key, "value": value}


def get_response(key, value) -> dict:
    return {"key": key, "value": value, "found": True}


def missing_response(key) -> dict:
    return {"key": key, "found": False}


def error_body(message) -> dict:
    return {"error": message}