import pytest

from app.block import BlockingManager
from app.utils import copy_file


FAKE_HOSTS_PATH = "tests/data/fake_hosts"
NR_OF_BLOCKED_SITES = 12


@pytest.fixture
def fake_hosts_file(tmp_path):
    """Fixture to create a fake hosts file with initial content."""
    hosts_path = tmp_path / "hosts"
    copy_file(FAKE_HOSTS_PATH, hosts_path)
    return str(hosts_path)


@pytest.fixture
def blocking_manager(fake_hosts_file):
    """Fixture to create a BlockingManager instance with the fake hosts file."""
    return BlockingManager(fake_hosts_file)


def test_initialization(blocking_manager, tmp_path):
    assert blocking_manager.hosts_path == str(tmp_path / "hosts")
    assert blocking_manager.redirect == "127.0.0.1"
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES


def test_block(blocking_manager):
    blocking_manager.block("www.example00.com")
    assert "www.example00.com" in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES + 1


def test_unblock(blocking_manager):
    blocking_manager.unblock("www.example1.com")
    assert "www.example1.com" not in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES - 1


def test_multiple_blocks(blocking_manager):
    blocking_manager.block("www.example00.com")
    blocking_manager.block("www.example01.com")
    assert "www.example00.com" in blocking_manager.blocked
    assert "www.example01.com" in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES + 2


def test_multiple_unblocks(blocking_manager):
    blocking_manager.unblock("www.example1.com")
    blocking_manager.unblock("www.example2.com")
    assert "www.example1.com" not in blocking_manager.blocked
    assert "www.example2.com" not in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES - 2


def test_block_unblock(blocking_manager):
    blocking_manager.block("www.example00.com")
    assert "www.example00.com" in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES + 1
    blocking_manager.unblock("www.example00.com")
    assert "www.example00.com" not in blocking_manager.blocked
    assert len(blocking_manager.blocked) == NR_OF_BLOCKED_SITES
