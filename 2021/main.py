import sentry_sdk
from flask import jsonify, request, Flask

# sentry_sdk.init(
#     "https://060c8c7a20ae472c8b32858cb41c36a7@o19635.ingest.sentry.io/5899451",
#     traces_sample_rate=1.0,
# )

app = Flask(__name__)


def process_data(data):
    steps = data["workflow_job"]["steps"]
    for s in steps:
        with sentry_sdk.start_transaction(op="task", name=s["name"]):
            # with sentry_sdk.start_span(op="http", description="GET /") as span:
            #     response = my_custom_http_library.request("GET", "/")
            #     span.set_tag("http.status_code", response.status_code)
            #     span.set_data("http.foobarsessionid", get_foobar_sessionid())
            pass
    return {"reason": "WIP"}, 200


def handle_event(data, headers):
    return {}, 200
    if headers.get("X-GitHub-Event") != "workflow_job":
        # We return 200 to make webhook not turn red
        return {"reason": "Event not supported."}, 200

    if data["action"] != "completed":
        return ({"reason": "We cannot do anything with this workflow state."}, 200)

    return process_data(data)


@app.route("/", methods=["POST"])
def main():
    print(request.data)
    payload, http_code = handle_event(request.data, request.headers)
    return jsonify(payload), http_code
