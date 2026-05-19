"""Flask server for the kvstore key-value API."""

from flask import Flask, jsonify, request

from kvstore import contract


def create_app() -> Flask:
    """Create and configure a Flask app with an in-memory store."""
    app = Flask(__name__)

    # In-memory store (dict) scoped to this app instance
    store: dict = {}

    @app.route(contract.HEALTH_PATH, methods=["GET"])
    def health():
        return jsonify(contract.health_body()), 200

    @app.route("/kv/<key>", methods=["PUT"])
    def put_key(key):
        data = request.get_json()
        if data is None or "value" not in data:
            return jsonify(contract.error_body(contract.VALUE_REQUIRED)), 400
        value = data["value"]
        store[key] = value
        return jsonify(contract.set_response(key, value)), 200

    @app.route("/kv/<key>", methods=["GET"])
    def get_key(key):
        if key not in store:
            return jsonify(contract.missing_response(key)), 404
        return jsonify(contract.get_response(key, store[key])), 200

    @app.route("/kv/<key>", methods=["DELETE"])
    def delete_key(key):
        if key not in store:
            return jsonify(contract.missing_response(key)), 404
        del store[key]
        return "", 204

    return app


app = create_app()