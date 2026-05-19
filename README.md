# wc3-kvstore

A simple key-value store HTTP API.

## HTTP Contract

This project defines a frozen wire contract for a key-value store API.

### Endpoints

| Method | Path | Request | Success Response | Error Response |
|--------|------|---------|------------------|----------------|
| GET | `/health` | - | 200 `{"status": "ok"}` | - |
| PUT | `/kv/<key>` | `{"value": <v>}` | 200 `{"key": <key>, "value": <v>}` | 400 `{"error": "value is required"}` |
| GET | `/kv/<key>` | - | 200 `{"key": <key>, "value": <v>, "found": true}` | 404 `{"key": <key>, "found": false}` |
| DELETE | `/kv/<key>` | - | 204 (empty body) | 404 `{"key": <key>, "found": false}` |

### Usage

```python
import kvstore

# Access contract symbols
kvstore.contract.HEALTH_PATH  # "/health"
kvstore.contract.kv_path("mykey")  # "/kv/mykey"

# After server/client modules exist
from kvstore import KVClient, create_app
```