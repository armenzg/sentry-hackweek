import json
from src.lib import process_data

import pytest


@pytest.fixture
def completed_workflow():
    with open("tests/fixtures/wf_completed.json") as f:
        return json.load(f)
