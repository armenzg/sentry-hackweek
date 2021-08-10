from src.lib import process_data
from .fixtures import *


# XXX: When running tests we will have to mock sending envelopers to relay
def test_process_data(completed_workflow):
    assert process_data(completed_workflow) == ({"reason": "WIP"}, 200)
