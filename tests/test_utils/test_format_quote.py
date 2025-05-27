import pytest
from app.utils import format_quote


def test_basic_quote_formatting():
    """Test basic quote formatting with default words per line."""
    quote = "To be or not to be that is the question whether tis nobler\n- Shakespeare"
    expected = (
        "To be or not to be that is the question\nwhether tis nobler\n- Shakespeare"
    )
    assert format_quote(quote) == expected


def test_custom_words_per_line():
    """Test formatting with custom words per line."""
    quote = "The quick brown fox jumps over the lazy dog\n- Anonymous"
    expected = "The quick brown fox\njumps over the lazy\ndog\n- Anonymous"
    assert format_quote(quote, words_per_line=4) == expected


def test_single_word_per_line():
    """Test formatting with one word per line."""
    quote = "Hello world test\n- Author"
    expected = "Hello\nworld\ntest\n- Author"
    assert format_quote(quote, words_per_line=1) == expected


def test_quote_shorter_than_words_per_line():
    """Test quote with fewer words than the line limit."""
    quote = "Short quote\n- Author"
    expected = "Short quote\n- Author"
    assert format_quote(quote, words_per_line=10) == expected


def test_exact_word_count_multiple():
    """Test quote with word count that's exact multiple of words_per_line."""
    quote = "One two three four five six seven eight nine ten\n- Author"
    expected = "One two three four five six seven eight nine ten\n- Author"
    assert format_quote(quote, words_per_line=10) == expected

    expected_5 = "One two three four five\nsix seven eight nine ten\n- Author"
    assert format_quote(quote, words_per_line=5) == expected_5


# Test edge cases with authors
def test_empty_author():
    """Test quote with empty author (just whitespace)."""
    quote = "Hello world\n   "
    expected = "Hello world"
    assert format_quote(quote) == expected


def test_author_with_special_characters():
    """Test author with special characters and formatting."""
    quote = "Test quote\n- Dr. John Smith, Ph.D."
    expected = "Test quote\n- Dr. John Smith, Ph.D."
    assert format_quote(quote) == expected


def test_quote_with_extra_whitespace():
    """Test quote with extra whitespace in text."""
    quote = "Hello    world   test   quote\n- Author"
    expected = "Hello world test quote\n- Author"
    assert format_quote(quote, words_per_line=4) == expected


# Test error conditions - Invalid input types
def test_non_string_input():
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="full_quote must be a string"):
        format_quote(123)

    with pytest.raises(ValueError, match="full_quote must be a string"):
        format_quote(None)

    with pytest.raises(ValueError, match="full_quote must be a string"):
        format_quote(["quote", "author"])


def test_invalid_words_per_line():
    """Test that invalid words_per_line values raise ValueError."""
    quote = "Test quote\n- Author"

    with pytest.raises(ValueError, match="words_per_line must be at least 1"):
        format_quote(quote, words_per_line=0)

    with pytest.raises(ValueError, match="words_per_line must be at least 1"):
        format_quote(quote, words_per_line=-1)

    with pytest.raises(ValueError, match="words_per_line must be at least 1"):
        format_quote(quote, words_per_line=-10)


# Test error conditions - Invalid quote format
def test_missing_newline_separator():
    """Test that quotes without newline separator raise ValueError."""
    with pytest.raises(
        ValueError, match="Invalid quote format: missing newline separator"
    ):
        format_quote("Quote without author separator")


def test_multiple_newlines_in_author():
    """Test that multiple newlines in author section raise ValueError."""
    with pytest.raises(
        ValueError, match="Invalid quote format: expected 'quote\\\\nauthor' format"
    ):
        format_quote("Test quote\n- Author\nExtra line")

    with pytest.raises(
        ValueError, match="Invalid quote format: expected 'quote\\\\nauthor' format"
    ):
        format_quote("Test quote\nAuthor\nAnother line\nYet another")


def test_empty_quote_text():
    """Test that empty quote text raises ValueError."""
    with pytest.raises(ValueError, match="Quote cannot be empty"):
        format_quote("\n- Author")

    with pytest.raises(ValueError, match="Quote cannot be empty"):
        format_quote("   \n- Author")


# Test boundary conditions
def test_single_word_quote():
    """Test quote with just one word."""
    quote = "Hello\n- Author"
    expected = "Hello\n- Author"
    assert format_quote(quote) == expected


def test_quote_only_whitespace_with_author():
    """Test quote that's only whitespace but has author."""
    with pytest.raises(ValueError, match="Quote cannot be empty"):
        format_quote("   \t  \n- Valid Author")


# Test special characters and unicode
def test_unicode_characters():
    """Test quote with unicode characters."""
    quote = "Café naïve résumé piñata\n- Unicode Author 中文"
    expected = "Café naïve résumé piñata\n- Unicode Author 中文"
    assert (
        format_quote(quote, words_per_line=2)
        == "Café naïve\nrésumé piñata\n- Unicode Author 中文"
    )


def test_punctuation_handling():
    """Test that punctuation is preserved and handled correctly."""
    quote = "Hello, world! How are you? I'm fine, thanks.\n- Punctuation Test"
    expected = "Hello, world! How are you?\nI'm fine, thanks.\n- Punctuation Test"
    assert format_quote(quote, words_per_line=5) == expected


def test_real_world_quote_example():
    """Test with a real-world quote example."""
    quote = "The only way to do great work is to love what you do\n- Steve Jobs"
    expected = "The only way to do great work is\nto love what you do\n- Steve Jobs"
    assert format_quote(quote, words_per_line=8) == expected
