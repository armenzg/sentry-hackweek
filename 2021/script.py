from src.workflow_events import process_data

# XXX: This is a big hack; remove when the time comes
if __name__ == "__main__":
    import json

    data = {}
    with open("tests/fixtures/wf_completed.json") as f:
        data = json.load(f)
    process_data(data)
