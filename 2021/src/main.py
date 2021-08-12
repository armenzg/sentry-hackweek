from flask import jsonify, request, Flask

from .workflow_events import process_data

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
    try:
        payload, http_code = handle_event(request.json, request.headers)
    except Exception as e:
        # XXX: Report to Sentry
        print(e)
        payload = {}
        http_code = 200
    return jsonify(payload), http_code
