from src.lib import process_data


def test_process_data():
    assert process_data({})[0] == {"reason": "WIP"}
