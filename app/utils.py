import datetime
import json
import os
import platform
import shutil
import sys
from urllib.parse import urlparse

QUOTES_RELATIVE_PATH = "../data/quotes.json"


def get_hosts_path():
    """Determines the correct hosts file path based on the OS."""
    if platform.system() == "Windows":
        return "C:\\Windows\\System32\\drivers\\etc\\hosts"
    else:
        print(f"Unsupported operating system: {platform.system()}")
        sys.exit(1)


def copy_file(source: str | os.PathLike, destination: str | os.PathLike):
    """
    Copies a file from the source path to the destination path.

    Args:
        source (str | os.PathLike): The file path of the source file.
        destination (str | os.PathLike): The file path of the destination.

    Returns:
        None
    """
    if os.path.isfile(destination):
        print(f"File already exists at {destination}. Copy operation skipped.")
    else:
        try:
            shutil.copy(source, destination)
            print(
                f"File copied successfully from:to\n{source}\n{os.path.abspath(destination)}"
            )
        except FileNotFoundError:
            print(f"Error: The source file '{source}' was not found.")
        except PermissionError:
            print("Error: Permission denied. Please check your access rights.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def extract_blocked_site(hosts_line: str):
    """
    Extracts the blocked website from a line in the hosts file.

    Args:
        hosts_line (str): A single line from the hosts file.

    Returns:
        str or None: The extracted blocked website if found, otherwise None.
    """
    hosts_line = hosts_line.strip()
    if not hosts_line.startswith("#"):
        parts = hosts_line.split()
        if len(parts) >= 2:
            if "#" not in parts[0] and "#" not in parts[1]:
                return parts[1]
    return None


def is_valid_site(url_or_domain: str):
    """
    Checks if a given string is likely a valid website URL or domain.

    This function uses a combination of checks to determine validity.

    Args:
        url_or_domain (str): The string to check.

    Returns:
        bool: True if the string is likely a valid site, False otherwise.
    """
    if not url_or_domain or not isinstance(url_or_domain, str):
        return False

    # Basic length check
    if len(url_or_domain) > 255:  # Maximum length of a hostname
        return False

    # Check for common invalid characters
    invalid_chars = [
        " ",
        "\t",
        "\n",
        "\r",
        "<",
        ">",
        "[",
        "]",
        "{",
        "}",
        "|",
        "\\",
        "^",
        "`",
    ]
    if any(char in url_or_domain for char in invalid_chars):
        return False

    # Try parsing as a URL
    try:
        parsed_url = urlparse(url_or_domain)
        if parsed_url.scheme and parsed_url.netloc:
            # Has a scheme (http/https) and a network location (domain)
            if "." in parsed_url.netloc:
                return True
    except Exception:
        # Parsing as URL failed, try basic domain checks
        return False

    # Basic IPv4 address check
    parts = url_or_domain.split(".")
    if len(parts) == 4:
        is_ipv4 = True
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                is_ipv4 = False
                break
        if is_ipv4:
            return True

    if "." in url_or_domain:
        parts = url_or_domain.split(".")
        if len(parts) >= 2:
            # Check TLD length (at least 2 characters)
            if len(parts[-1]) >= 2:
                # Check each part for invalid characters and length
                for part in parts:
                    # Empty before or after '.'
                    if not part:
                        return False
                    # Maximum length of a domain label
                    if len(part) > 63:
                        return False
                    # Characters are alphanumeric or '-'
                    if not all(c.isalnum() or c == "-" for c in part):
                        return False
                    # Does not start or end with '-'
                    if part.startswith("-") or part.endswith("-"):
                        return False
                return True

    return False


def get_quote(filepath: str | os.PathLike = QUOTES_RELATIVE_PATH):
    """
    Retrieves a quote from a JSON file based on the current day.

    Args:
        filepath: The path to the JSON file containing quotes.

    Returns:
        A formatted quote string, or an empty string if an error occurs.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            quotes = json.load(file)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}.")
        return ""
    if not quotes:  # Handle empty list of quotes
        print(f"Error: No quotes found in {filepath}.")
        return ""

    today = datetime.date.today()
    day_number = today.toordinal()
    quote_index = day_number % len(quotes)
    selected_quote = quotes[quote_index]
    quote = (
        f"\"{selected_quote['quote']}\"\n- {selected_quote.get('author', 'Unknown')}"
    )
    return quote


def format_quote(full_quote: str, words_per_line: int = 10) -> str:
    """
    Format a quote by wrapping words to specified number per line.

    Args:
        full_quote: Quote string in format 'quote text\n- author'
        words_per_line: Maximum words per line (default: 10)

    Returns:
        Formatted quote with word wrapping

    Raises:
        ValueError: If input format is invalid or words_per_line < 1
    """
    if not isinstance(full_quote, str):
        raise ValueError("full_quote must be a string")

    if words_per_line < 1:
        raise ValueError("words_per_line must be at least 1")

    if "\n" not in full_quote:
        raise ValueError("Invalid quote format: missing newline separator")

    quote_text, author = full_quote.split("\n", 1)
    if "\n" in author:
        raise ValueError("Invalid quote format: expected 'quote\\nauthor' format")

    words = [word for word in quote_text.split() if word]
    if not words:
        raise ValueError("Quote cannot be empty")

    lines = []
    for i in range(0, len(words), words_per_line):
        line_words = words[i : i + words_per_line]
        lines.append(" ".join(line_words))

    # Join all lines and add author
    formatted_quote = "\n".join(lines)
    if author.strip():  # Only add author if it's not empty
        formatted_quote += "\n" + author

    return formatted_quote
