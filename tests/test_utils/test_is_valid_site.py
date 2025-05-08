import pytest
from app.utils import is_valid_site


@pytest.mark.parametrize(
    "site, valid",
    [
        ("example.com", True),
        ("www.example.com", True),
        ("subdomain.example.co.uk", True),
        ("http://example.com", True),
        ("https://www.example.net/path?query=value", True),
        ("example-hyphen.com", True),
        ("ex.ample", True),
        ("192.168.1.1", True),
    ],
)
def test_with_valid_sites(site, valid):
    assert is_valid_site(site) is valid


@pytest.mark.parametrize(
    "site, valid",
    [
        ("local", False),
        ("invalid char ", False),
        ("toolongdomainnameaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com", False),
        (".invalid", False),
        ("invalid.", False),
        ("-invalid.com", False),
        ("invalid-.com", False),
        ("", False),
        (None, False),
        (123, False),
        ("localhost", False),
        ("192.168.1", False),
        ("192.168.l.1", False),
        ("256.168.1.1", False),
    ],
)
def test_with_invalid_sites(site, valid):
    assert is_valid_site(site) is valid