import socket
import threading
from database import initialize_db
from flask import Flask, request, jsonify
from process import handle_request

app = Flask(__name__)
PORT = 5000


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/v1/update", methods=["POST"])
def update():
    data = request.get_json()
    if not validate_update_json(data):
        return jsonify({"status": "error", "error": "missing client_id"}), 400
    handle_request(request.remote_addr, data)

    return jsonify({"status": "ok"}), 200


def validate_update_json(data):
    if "client_id" not in data:
        return False
    else:
        return True


if __name__ == "__main__":
    initialize_db()

    app.run(host="0.0.0.0", port=PORT, debug=True)
    print("Server started on port {}".format(PORT))
