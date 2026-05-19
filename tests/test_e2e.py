"""End-to-end tests for the composed kvstore package.

This module tests the full integration of the kvstore package by:
1. Starting a real HTTP server using kvstore.create_app()
2. Driving kvstore.KVClient against it
3. Verifying all contract behaviors
"""

import threading
from wsgiref.simple_server import make_server, WSGIRequestHandler

import pytest
import requests

from kvstore import create_app, KVClient, contract


class QuietHandler(WSGIRequestHandler):
    """WSGI request handler that suppresses logging."""

    def log_message(self, *args, **kwargs):
        pass


@pytest.fixture
def server_url():
    """Start a test server and return its base URL.

    The server runs in a background thread and is automatically
    shut down when the test completes.
    """
    app = create_app()
    server = make_server("127.0.0.1", 0, app, handler_class=QuietHandler)
    port = server.server_address[1]
    base_url = f"http://127.0.0.1:{port}"

    # Start server in background thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    yield base_url

    # Shutdown server
    server.shutdown()


@pytest.fixture
def client(server_url):
    """Create a KVClient instance for the test server."""
    return KVClient(server_url)


def test_health(client):
    """Test health endpoint returns expected response."""
    assert client.health() is True


def test_set_and_get(client):
    """Test setting and getting a key-value pair."""
    client.set("test_key", "test_value")
    assert client.get("test_key") == "test_value"


def test_get_absent_key(client):
    """Test getting a non-existent key returns None."""
    assert client.get("nonexistent_key") is None


def test_delete_existing_key(client):
    """Test deleting an existing key."""
    client.set("to_delete", "value")
    assert client.delete("to_delete") is True
    assert client.get("to_delete") is None


def test_delete_absent_key(client):
    """Test deleting a non-existent key returns False."""
    assert client.delete("nonexistent_key") is False


def test_put_without_value_returns_400_error(server_url):
    """Test PUT request without 'value' field returns contract error."""
    url = server_url + contract.kv_path("x")
    response = requests.put(url, json={"nope": 1})

    assert response.status_code == 400
    assert response.json() == contract.error_body(contract.VALUE_REQUIRED)


def test_full_round_trip(client):
    """Test complete round trip of operations."""
    # Set a value
    result = client.set("round_trip", "v1")
    assert result == {"key": "round_trip", "value": "v1"}

    # Get it back
    assert client.get("round_trip") == "v1"

    # Delete it
    assert client.delete("round_trip") is True

    # Verify it's gone
    assert client.get("round_trip") is None
    assert client.delete("round_trip") is False