# import json
import os
import pytest
import time

# from unittest import mock
from app.block import BlockingManager

# from tests.utils import read_mock_hosts
# from tests.utils import read_mock_state


@pytest.fixture
def mock_hosts_path(tmp_path):
    """Fixture to provide a temporary hosts file path."""
    return str(tmp_path / "hosts")


@pytest.fixture
def blocking_manager(mock_hosts_path):
    """Fixture to create a BlockingManager instance with a mock hosts path."""
    return BlockingManager(
        mock_hosts_path, state_file=str(mock_hosts_path) + ".state.json"
    )


def test_initialization(blocking_manager):
    assert os.path.isfile(blocking_manager.state_file)
    assert blocking_manager.redirect == "127.0.0.1"
    assert blocking_manager.indefinitely_blocked == set()
    assert blocking_manager.temporarily_blocked == {}


def test_get_blocked_sites(blocking_manager):
    blocking_manager.indefinitely_blocked.add("indefinite.com")
    blocking_manager.temporarily_blocked["temporary.com"] = time.time() + 60
    blocked = blocking_manager.get_blocked_sites()
    assert "indefinite.com" in blocked
    assert "temporary.com" in blocked


# def test_block_indefinitely(blocking_manager, mock_hosts_path, mocker):
# mock_open = mocker.patch(
#     'builtins.open',
#     new_callable=mock.mock_open,
#     read_data=""
# )
#     blocking_manager.block_indefinitely("example.com")
#     mock_open.assert_any_call(mock_hosts_path, 'r+')
#     mock_open().write.assert_any_call("127.0.0.1 example.com\n")
#     assert "example.com" in blocking_manager.indefinitely_blocked
#     state = read_mock_state(blocking_manager)
#     assert "example.com" in state.get('indefinitely_blocked', [])

# def test_block_temporarily(blocking_manager, mock_hosts_path, mocker):
# mock_open = mocker.patch(
#     'builtins.open',
#     new_callable=mock.mock_open,
#     read_data=""
# )
#     blocking_manager.block_temporarily("temporary.com", 10)
#     mock_open.assert_any_call(mock_hosts_path, 'r+')
#     mock_open().write.assert_any_call(mock.ANY)  # We just check that write was called
#     assert "temporary.com" in blocking_manager.temporarily_blocked
#     state = read_mock_state(blocking_manager)
#     assert "temporary.com" in state.get('temporarily_blocked', {})

# def test_unblock(blocking_manager, mock_hosts_path, mocker):
# mock_open = mocker.patch(
#     'builtins.open',
#     new_callable=mock.mock_open,
#     read_data="127.0.0.1 example.com\n127.0.0.1 temporary.com\n"
# )
#     blocking_manager.indefinitely_blocked.add("example.com")
#     blocking_manager.temporarily_blocked["temporary.com"] = time.time() + 60
#     blocking_manager.unblock("example.com")
#     mock_open.assert_any_call(mock_hosts_path, 'r+')
#     content = read_mock_hosts(mock_open)
#     assert "example.com" not in content
#     assert "temporary.com" in content
#     assert "example.com" not in blocking_manager.indefinitely_blocked
#     assert "example.com" not in blocking_manager.temporarily_blocked
#     state = read_mock_state(blocking_manager)
#     assert "example.com" not in state.get('indefinitely_blocked', [])
#     assert "example.com" not in state.get('temporarily_blocked', {})

# def test_check_expired_blocks(blocking_manager, mock_hosts_path, mocker):
# mock_open = mocker.patch(
#     'builtins.open',
#     new_callable=mock.mock_open,
#     read_data="127.0.0.1 expired.com\n127.0.0.1 still_active.com\n"
# )
#     blocking_manager.temporarily_blocked["expired.com"] = time.time() - 1
#     blocking_manager.temporarily_blocked["still_active.com"] = time.time() + 60
#     blocking_manager._check_expired_blocks()
#     assert "expired.com" not in blocking_manager.temporarily_blocked
#     assert "still_active.com" in blocking_manager.temporarily_blocked
#     content = read_mock_hosts(mock_open)
#     assert "expired.com" not in content
#     assert "still_active.com" in content
#     state = read_mock_state(blocking_manager)
#     assert "expired.com" not in state.get('temporarily_blocked', {})
#     assert "still_active.com" in state.get('temporarily_blocked', {})

# def test_load_and_save_state(blocking_manager, mock_hosts_path, mocker):
#     initial_state = {
#         'indefinitely_blocked': ['persisted.com'],
#         'temporarily_blocked': {'later.com': time.time() + 120}
#     }
# mock_file = mocker.patch(
#     'builtins.open',
#     mock.mock_open(read_data=json.dumps(initial_state))
#     )
#     new_manager = BlockingManager(mock_hosts_path)
#     assert new_manager.indefinitely_blocked == {'persisted.com'}
#     assert 'later.com' in new_manager.temporarily_blocked

#     new_manager.block_indefinitely("another.com")
#     state = read_mock_state(new_manager)
#     assert "persisted.com" in state.get('indefinitely_blocked', [])
#     assert "another.com" in state.get('indefinitely_blocked', [])
#     assert 'later.com' in state.get('temporarily_blocked', {})

# def test_update_hosts_file(blocking_manager, mock_hosts_path, mocker):
# mock_open = mocker.patch(
#     'builtins.open',
#     new_callable=mock.mock_open,
#     read_data="some existing line\n127.0.0.1 old_blocked.com\n"
#     )
#     blocking_manager.indefinitely_blocked.add("new_blocked.com")
#     blocking_manager.temporarily_blocked["temp_blocked.net"] = time.time() + 60
#     blocking_manager._update_hosts_file()
#     content = read_mock_hosts(mock_open)
#     assert "some existing line" in content
#     assert "old_blocked.com" not in content  # Should be removed if no longer in state
#     assert "127.0.0.1 new_blocked.com" in content
#     assert "127.0.0.1 temp_blocked.net" in content
