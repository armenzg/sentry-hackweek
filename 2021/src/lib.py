import io
import gzip
import uuid
from datetime import datetime

import requests
from sentry_sdk.envelope import Envelope
from sentry_sdk.utils import format_timestamp

RELAY_DSN = "http://060c8c7a20ae472c8b32858cb41c36a7@127.0.0.1:3000/5899451"


def url_from_dsn(dsn, api):
    base_uri, project_id = dsn.rsplit("/", 1)
    # '{BASE_URI}/api/{PROJECT_ID}/{ENDPOINT}/'
    return f"{base_uri}/api/{project_id}/{api}/"


def send_envelope(envelope):
    headers = {
        "Content-Type": "application/x-sentry-envelope",
        "Content-Encoding": "gzip",
        "X-Sentry-Auth": "Sentry sentry_key=060c8c7a20ae472c8b32858cb41c36a7,"
        + f"sentry_client=gha-sentry/0.0.1,sentry_timestamp={str(datetime.utcnow())},"
        + "sentry_version=7",
        "event_id": uuid.uuid4().hex,  # Does this have to match anything?
        "sent_at": format_timestamp(datetime.utcnow()),
    }
    url = url_from_dsn(RELAY_DSN, "envelope")
    body = io.BytesIO()
    with gzip.GzipFile(fileobj=body, mode="w") as f:
        envelope.serialize_into(f)

    req = requests.post(url, data=body.getvalue(), headers=headers)
    print(url)
    print(req.text)


# Documentation about traces, transactions and spans
# https://docs.sentry.io/product/sentry-basics/tracing/distributed-tracing/#traces
def generate_transaction(workflow):
    trace_id = uuid.uuid4().hex
    parent_span_id = uuid.uuid4().hex[16:]
    trace = {
        # "op": workflow["name"], # When missing it uses "default"
        "trace_id": trace_id,
        "span_id": parent_span_id,
        "type": "trace",
        # XXX: Determine what the failure state should look like
        "status": "ok" if workflow["conclusion"] else "failed",
    }
    spans = []
    for step in workflow["steps"]:
        try:
            spans.append(
                {
                    # "description": "<OrganizationContext>",
                    "op": step["name"],
                    "parent_span_id": parent_span_id,
                    "span_id": uuid.uuid4().hex[16:],
                    "start_timestamp": step["started_at"],
                    "timestamp": step["completed_at"],
                    "trace_id": trace_id,
                }
            )
        except Exception as e:
            # XXX: Deal with this later
            print(e)
    transaction = {
        "event_id": uuid.uuid4().hex,
        "type": "transaction",
        # A better name would be desirable than "salutation"
        "transaction": workflow["name"],
        # When processing old data during development, in Sentry's UI, you will
        # see an error for transactions with "Clock drift detected in SDK";
        # It is harmeless.
        "start_timestamp": workflow["started_at"],
        "timestamp": workflow["completed_at"],
        "contexts": {
            "trace": trace,
        },
        "spans": spans,
    }
    import pprint

    pprint.pprint(transaction)
    return transaction


def process_data(data):
    envelope = Envelope()
    envelope.add_transaction(generate_transaction(data["workflow_job"]))
    send_envelope(envelope)
    return {"reason": "WIP"}, 200


if __name__ == "__main__":
    process_data(
        {
            "workflow_job": {
                "conclusion": "success",
                "started_at": "2021-08-09T18:12:37Z",
                "completed_at": "2021-08-09T18:12:41Z",
                "name": "salutation",
                "steps": [
                    {
                        "name": "Set up job",
                        "status": "completed",
                        "conclusion": "success",
                        "number": 1,
                        "started_at": "2021-08-09T18:12:37.000Z",
                        "completed_at": "2021-08-09T18:12:40.000Z",
                    },
                    {
                        "name": "Checkout",
                        "status": "completed",
                        "conclusion": "success",
                        "number": 2,
                        "started_at": "2021-08-09T18:12:40.000Z",
                        "completed_at": "2021-08-09T18:12:40.000Z",
                    },
                    {
                        "name": "Welcome",
                        "status": "completed",
                        "conclusion": "success",
                        "number": 3,
                        "started_at": "2021-08-09T18:12:40.000Z",
                        "completed_at": "2021-08-09T18:12:40.000Z",
                    },
                    {
                        "name": "Post Checkout",
                        "status": "completed",
                        "conclusion": "success",
                        "number": 6,
                        "started_at": "2021-08-09T18:12:40.000Z",
                        "completed_at": "2021-08-09T18:12:41.000Z",
                    },
                    {
                        "name": "Complete job",
                        "status": "completed",
                        "conclusion": "success",
                        "number": 7,
                        "started_at": "2021-08-09T18:12:41.000Z",
                        "completed_at": "2021-08-09T18:12:41.000Z",
                    },
                ],
            }
        }
    )
