
from database import get_past_five_min_movements, initialize_db
from flask import Flask, request, jsonify
from process import handle_request
from flask_apscheduler import APScheduler

# initialize flask app
app = Flask(__name__)
PORT = 5001
# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


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


@scheduler.task("cron", id="u", minute="*/5")
def update_temp():
    print("Checking if user is starting to sleep...")
    data = get_past_five_min_movements()
    status_sleep = [item for item in data if item['overall_status'] == 1]
    status_awake = [item for item in data if item['overall_status'] == 0]

    if len(status_sleep) != 0:
        sleep_awake_ratio = 0.0 + len(status_awake) / len(status_sleep)

        # if the user is "asleep" for more than 50% of the time in the past 5 minutes, set temp to 23 C
        if sleep_awake_ratio < 0.5:
            print("User is starting to sleep...")
            print("Action: set temp to 23 C")
    else:
        print("Waiting: User is awake")


if __name__ == "__main__":
    initialize_db()

    app.run(host="0.0.0.0", port=PORT, debug=True)
    print("Server started on port {}".format(PORT))
