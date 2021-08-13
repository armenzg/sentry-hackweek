from flask import jsonify, request, Flask

from .workflow_events import process_data

from sentry_sdk import init, capture_exception

# This tracks errors and performance of the app itself rather than GH workflows
init(
    "https://86b85918a26246b2b6160820de5c6be1@o19635.ingest.sentry.io/5903949",
    traces_sample_rate=1.0,
    environment="development",
)

app = Flask(__name__)


def handle_event(data, headers):
    if headers.get("X-GitHub-Event") != "workflow_job":
        # We return 200 to make webhook not turn red
        return {"reason": "Event not supported."}, 200

    if data["action"] != "completed":
        return ({"reason": "We cannot do anything with this workflow state."}, 200)

    process_data(data)


@app.route("/", methods=["POST"])
def main():
    try:
        payload, http_code = handle_event(request.json, request.headers)
    except Exception as e:
        capture_exception(e)
        payload = {"reason": "There was an error."}
        http_code = 500
    return jsonify(payload), http_code
