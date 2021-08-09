from flask import jsonify, request, Flask

from lib import process_data

app = Flask(__name__)


def handle_event(data, headers):
    if headers.get("X-GitHub-Event") != "workflow_job":
        # We return 200 to make webhook not turn red
        return {"reason": "Event not supported."}, 200

    if data["action"] != "completed":
        return ({"reason": "We cannot do anything with this workflow state."}, 200)

    return process_data(data)


@app.route("/", methods=["POST"])
def main():
    payload, http_code = handle_event(request.json, request.headers)
    return jsonify(payload), http_code
