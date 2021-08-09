from flask import jsonify, request, Flask

app = Flask(__name__)


class WorkflowState:
    # data as per GH webhook's payload
    def __init__(self, data) -> None:
        # queued, started, completed
        self.state = data["action"]
        wf_job = data["workflow_job"]
        # Does this id persist for the same wf after each commit?
        self.id = wf_job["id"]  # e.g. 3283437728
        # This, I assume is when a workflow is re-run
        # Metadata about the run: https://api.github.com/repos/armenzg/sentry-hackweek/actions/runs/1113865931
        self.run_id = wf_job["id"]  # e.g. 1113865931
        self.startime_start = wf_job["started_at"]  # e.g. "2021-08-09T18:12:37Z"
        self.startime_start = wf_job["name"]  # e.g. yml file -> "name": "salutation"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.headers.get("X-GitHub-Event") != "workflow_job":
        # We return 200 to make webhook not turn red
        return jsonify({"reason": "Event not supported"}), 200
    data = WorkflowState(request.data)
    print(request.data)
    print(request.headers)
    # return "<p>Hello, World!</p>"
    return jsonify({}), 200
