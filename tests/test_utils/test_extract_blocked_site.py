import pytest
from app.utils import extract_blocked_site


@pytest.mark.parametrize(
    "hosts_line, expected_site",
    [
        ("127.0.0.1 www.facebook.com  # blocked this page", "www.facebook.com"),
        ("127.0.0.1 facebook.com", "facebook.com"),
        ("127.0.0.1 youtube.com", "youtube.com"),
        ("127.0.0.1 www.youtube.com # some comment", "www.youtube.com"),
        ("127.0.0.1 www.youtube.com/channel_name", "www.youtube.com/channel_name"),
        ("127.0.0.1 www.facebook.com/page_name", "www.facebook.com/page_name"),
        ("127.0.0.1 sub.domain.example.co.uk", "sub.domain.example.co.uk"),
        ("127.0.0.1 123.456.789.012", "123.456.789.012"),  # Might be a local IP block
        ("127.0.0.2 www.example.com", "www.example.com"),
    ],
)
def test_extract_valid_blocked_sites(hosts_line, expected_site):
    assert extract_blocked_site(hosts_line) == expected_site


@pytest.mark.parametrize(
    "hosts_line",
    [
        ("# 127.0.0.1 another.com"),
        ("127.0.0.1"),
        (" "),
        (""),
    ],
)
def test_extract_no_blocked_site(hosts_line):
    assert extract_blocked_site(hosts_line) is None


def test_extract_no_site_after_redirect_ip():
    hosts_line = "127.0.0.1  # comment"
    assert extract_blocked_site(hosts_line) is None


def test_extract_site_with_multiple_spaces():
    hosts_line = "127.0.0.1   another.site.com  # comment"
    assert extract_blocked_site(hosts_line) == "another.site.com"
