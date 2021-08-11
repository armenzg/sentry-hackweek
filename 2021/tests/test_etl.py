from src.lib import generate_transaction
from .fixtures import *

# XXX: How do we test when timestamps and uuids change?
# XXX: We also need to deal with requests happening
def test_generate_transaction(completed_workflow, generated_transaction):
    assert generate_transaction(completed_workflow["workflow_job"]) == (
        generated_transaction
    )
