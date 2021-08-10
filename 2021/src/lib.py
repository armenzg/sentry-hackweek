import time

import sentry_sdk

# This will capture issues for this app *and* the manually reported GHA data
sentry_sdk.init(
    "https://060c8c7a20ae472c8b32858cb41c36a7@o19635.ingest.sentry.io/5899451",
    # "http://060c8c7a20ae472c8b32858cb41c36a7@127.0.0.1:3000/5899451",
    traces_sample_rate=1.0,
    environment="development",
)

data = {
    "name": "salutation",
    "steps": [
      {
        "name": "Set up job",
        "status": "completed",
        "conclusion": "success",
        "number": 1,
        "started_at": "2021-08-09T18:12:37.000Z",
        "completed_at": "2021-08-09T18:12:40.000Z"
      },
      {
        "name": "Checkout",
        "status": "completed",
        "conclusion": "success",
        "number": 2,
        "started_at": "2021-08-09T18:12:40.000Z",
        "completed_at": "2021-08-09T18:12:40.000Z"
      },
    ],
}

def send_envelope():
    # sentry_sdk.capture_message("foo")
    # with sentry_sdk.configure_scope() as scope:
    #     # XXX: Is this even important?
    #     scope.transaction = "TempTransaction"
    for 
    with sentry_sdk.start_transaction(op="task", name="foo"):
        # process_item may create more spans internally (see next examples)
        time.sleep(3)


# XXX: When running tests, how can I prevent post requests from happening?
def process_data(data):
    steps = data["workflow_job"]["steps"]
    for s in steps:
        pass
    return {"reason": "WIP"}, 200


if __name__ == "__main__":
    send_envelope()
