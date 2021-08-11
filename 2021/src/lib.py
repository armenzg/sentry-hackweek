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
    if not req.ok:
        print(req.text)


def get_extra_metadata(workflow_run):
    req = requests.get(workflow_run)
    if not req.ok:
        raise Exception(req.text)
    run_data = req.json()
    # XXX: We could enrich each transaction by having access to the yml file and/or the logs
    return requests.get(run_data["workflow_url"]).json()


# Documentation about traces, transactions and spans
# https://docs.sentry.io/product/sentry-basics/tracing/distributed-tracing/#traces
def generate_transaction(workflow):
    try:
        # This helps to have human friendly transaction names
        meta = get_extra_metadata(workflow["run_url"])
        transaction_name = f'{meta["name"]}/{workflow["name"]}'
    except Exception as e:
        print(e)
        print(f"Failed to process -> {workflow['run_url']}")
        transaction_name = {workflow["name"]}

    # This can happen when the workflow is skipped and there are no steps
    if not workflow["steps"]:
        print(f"We are ignoring {transaction_name} -> {workflow['html_url']}")
        return

    trace_id = uuid.uuid4().hex
    parent_span_id = uuid.uuid4().hex[16:]

    transaction = {
        "event_id": uuid.uuid4().hex,
        "type": "transaction",
        "transaction": transaction_name,
        # When processing old data during development, in Sentry's UI, you will
        # see an error for transactions with "Clock drift detected in SDK";
        # It is harmeless.
        "start_timestamp": workflow["started_at"],
        "timestamp": workflow["completed_at"],
        "contexts": {
            "trace": {
                "op": workflow["name"],
                "trace_id": trace_id,
                "span_id": parent_span_id,
                "type": "trace",
                # XXX: Determine what the failure state should look like
                "status": "ok" if workflow["conclusion"] else "failed",
                "data": workflow["html_url"],
                # html_url points to the UI showing the job run
                # url points has the data to generate this transaction
                # workflow_run has extra metadata about the workflow file
                "tags": {
                    "html_url": workflow["html_url"],
                    "url": workflow["url"],
                    "workflow_run": workflow["run_url"],
                },
            },
        },
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

    transaction["spans"] = spans
    return transaction


def process_data(data):
    transaction = generate_transaction(data["workflow_job"])
    if transaction:
        envelope = Envelope()
        envelope.add_transaction(transaction)
        send_envelope(envelope)
    # XXX: Return something sensiblwe
    return {"reason": "WIP"}, 200


# XXX: This is a big hack; remove when the time comes
if __name__ == "__main__":
    import json

    data = {}
    with open("tests/fixtures/wf_completed.json") as f:
        data = json.load(f)
    process_data(data)
