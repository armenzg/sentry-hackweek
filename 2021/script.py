from src.workflow_events import process_data

# XXX: This script helps us ingest a workflow from a json file
if __name__ == "__main__":
    import json

    data = {}
    # XXX: Rather hard-coded
    with open("tests/fixtures/failed_workflow.json") as f:
        data = json.load(f)
    process_data(data)
