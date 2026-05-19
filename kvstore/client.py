"""HTTP client for the kvstore key-value store API."""

import requests
from kvstore import contract


class KVClient:
    """Client for the kvstore HTTP API."""

    def __init__(self, base_url: str):
        """Initialize the client with a base URL.

        Args:
            base_url: Base URL of the kvstore server (trailing '/' is stripped).
        """
        self.base_url = base_url.rstrip("/")

    def health(self) -> bool:
        """Check if the server is healthy.

        Returns:
            True if the server responds with 200 and the expected health body,
            False if the server is unreachable or returns an unexpected response.
        """
        try:
            url = self.base_url + contract.HEALTH_PATH
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json() == contract.health_body()
            return False
        except requests.RequestException:
            return False

    def set(self, key, value) -> dict:
        """Set a key-value pair.

        Args:
            key: The key to set.
            value: The value to associate with the key.

        Returns:
            The parsed JSON response body on success.
        """
        url = self.base_url + contract.kv_path(key)
        response = requests.put(
            url,
            json=contract.set_request(value),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    def get(self, key):
        """Get the value for a key.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        url = self.base_url + contract.kv_path(key)
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data["value"]
        elif response.status_code == 404:
            return None
        response.raise_for_status()

    def delete(self, key) -> bool:
        """Delete a key.

        Args:
            key: The key to delete.

        Returns:
            True if the key was deleted, False if the key did not exist.
        """
        url = self.base_url + contract.kv_path(key)
        response = requests.delete(url, timeout=5)

        if response.status_code == 204:
            return True
        elif response.status_code == 404:
            return False
        response.raise_for_status()