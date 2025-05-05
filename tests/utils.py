import json


def read_mock_hosts(mock_file):
    """Helper function to read the content written to the mock hosts file."""
    calls = mock_file.mock_calls
    for call in reversed(calls):
        if call.method == "write":
            return call.args[0]
    return ""


def read_mock_state(blocking_manager):
    """Helper function to read the content of the state file."""
    try:
        with open(blocking_manager.state_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
