import time

import requests

RELAY_DSN = "http://060c8c7a20ae472c8b32858cb41c36a7@127.0.0.1:3000/5899451"


def url_from_dsn(dsn, api):
    base_uri, project_id = dsn.rsplit("/", 1)
    # '{BASE_URI}/api/{PROJECT_ID}/{ENDPOINT}/'
    return f"{base_uri}/api/{project_id}/{api}/"


def send_envelope():
    envelope = """
{"event_id":"9ec79c33ec9942ab8353589fcb2e04dc","email":"john@me.com","name":"John Me","comments":"It broke."}\n
"""

    url = url_from_dsn(RELAY_DSN, "envelope")
    headers = {
        "X-Sentry-Auth": "Sentry",
        "sentry_version": "7",
        "sentry_client": "0.0.1",
        "sentry_timestamp": str(time.time()),
        "sentry_key": RELAY_DSN.rsplit("@", 1)[0].rsplit("//")[-1],
    }

    req = requests.post(url, data=envelope, headers=headers)
    import pprint

    pprint.pprint(headers)
    print(req.text)


# XXX: When running tests, how can I prevent post requests from happening?
def process_data(data):
    steps = data["workflow_job"]["steps"]
    send_envelope()
    for s in steps:
        pass
    return {"reason": "WIP"}, 200


if __name__ == "__main__":
    send_envelope()
