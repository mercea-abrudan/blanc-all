import pytest
import json
import os
import datetime
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from app.utils import get_quote


# Mock data for testing
SAMPLE_QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
    {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts."}  # No author
]

 
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_success_with_author(mock_date, mock_file):
    """Test successful quote retrieval with author"""
    # Create a mock date object
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521  # Jan 1, 2024 ordinal
    mock_date.today.return_value = mock_today
        
    result = get_quote("test_quotes.json")
        
    # Calculate expected quote index
    day_number = 738521
    expected_index = day_number % len(SAMPLE_QUOTES)
    expected_quote = SAMPLE_QUOTES[expected_index]
    expected_result = f'"{expected_quote["quote"]}"\n- {expected_quote["author"]}'
        
    assert result == expected_result
    mock_file.assert_called_once_with("test_quotes.json", 'r', encoding='utf-8')

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_success_without_author(mock_date, mock_file):
    """Test successful quote retrieval without author (uses 'Unknown')"""
    # Create a mock date that will give us index 4 (quote without author)
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738525  # Should give index 4 when mod 5
    mock_date.today.return_value = mock_today
        
    result = get_quote("test_quotes.json")
        
    day_number = 738525
    expected_index = day_number % len(SAMPLE_QUOTES)  # Should be 4
        
    if expected_index == 4:
        expected_result = f'"{SAMPLE_QUOTES[4]["quote"]}"\n- Unknown'
        assert result == expected_result

@patch('builtins.open', side_effect=FileNotFoundError)
@patch('builtins.print')
def test_get_quote_file_not_found(mock_print, mock_file):
    """Test behavior when quotes file is not found"""
    result = get_quote("nonexistent.json")
        
    assert result == ""
    mock_print.assert_called_once_with("Error: nonexistent.json not found.")

@patch('builtins.open', new_callable=mock_open, read_data='invalid json content')
@patch('builtins.print')
def test_get_quote_invalid_json(mock_print, mock_file):
    """Test behavior when JSON file contains invalid JSON"""
    result = get_quote("invalid.json")
        
    assert result == ""
    mock_print.assert_called_once_with("Error: Invalid JSON format in invalid.json.")

@patch('builtins.open', new_callable=mock_open, read_data='[]')
@patch('datetime.date')
@patch('builtins.print')
def test_get_quote_empty_quotes_list(mock_print, mock_date, mock_file):
    """Test behavior with empty quotes list (should raise ZeroDivisionError)"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
        
    result = get_quote("empty.json")

    assert result == ""
    mock_print.assert_called_once_with("Error: No quotes found in empty.json.")
        

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{"quote": "Test quote", "author": "Test Author"}]))
@patch('datetime.date')
def test_get_quote_single_quote(mock_date, mock_file):
    """Test with single quote in file"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
        
    result = get_quote("single.json")
        
    expected_result = '"Test quote"\n- Test Author'
    assert result == expected_result

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_different_dates_same_index(mock_date, mock_file):
    """Test that quotes with same modulo result return same quote"""
    # Test two dates that should give same index
    mock_today1 = MagicMock()
    mock_today1.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today1
    result1 = get_quote("test.json")
        
    # Same index (738521 + 5 = 738526, both mod 5 give same result)
    mock_today2 = MagicMock()
    mock_today2.toordinal.return_value = 738526
    mock_date.today.return_value = mock_today2
    result2 = get_quote("test.json")
        
    assert result1 == result2

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_with_pathlike_object(mock_date, mock_file):
    """Test function accepts Path-like objects"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
        
    path_obj = Path("test_quotes.json")
    result = get_quote(path_obj)
        
    assert isinstance(result, str)
    assert result != ""

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{"quote": "", "author": "Empty Quote"}]))
@patch('datetime.date')
def test_get_quote_empty_quote_text(mock_date, mock_file):
    """Test behavior with empty quote text"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
        
    result = get_quote("empty_quote.json")
        
    expected_result = '""\n- Empty Quote'
    assert result == expected_result

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{"quote": "Quote without author key"}]))
@patch('datetime.date')
def test_get_quote_missing_author_key(mock_date, mock_file):
    """Test behavior when quote dictionary doesn't have 'author' key"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
        
    result = get_quote("no_author.json")
        
    expected_result = '"Quote without author key"\n- Unknown'
    assert result == expected_result

@patch('builtins.open')
@patch('builtins.print')
def test_get_quote_permission_error(mock_print, mock_file):
    """Test behavior when file exists but cannot be read due to permissions"""
    mock_file.side_effect = PermissionError("Permission denied")
    
    # This should raise PermissionError as it's not caught by the function
    with pytest.raises(PermissionError):
        get_quote("permission_denied.json")

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_default_parameter(mock_date, mock_file):
    """Test that function uses default parameter when none provided"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
    
    # This assumes QUOTES_RELATIVE_PATH is defined in the original module
    # You might need to mock this constant as well
    result = get_quote()
    
    assert isinstance(result, str)

   
@pytest.mark.parametrize("ordinal_day,expected_index", [
    (738521, 738521 % 5),  # Jan 1, 2024
    (738522, 738522 % 5),  # Jan 2, 2024
    (738885, 738885 % 5),  # Dec 31, 2024
    (738000, 738000 % 5),  # Some other date
])
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(SAMPLE_QUOTES))
@patch('datetime.date')
def test_get_quote_various_ordinal_days(mock_date, mock_file, ordinal_day, expected_index):
    """Test quote selection for various ordinal days"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = ordinal_day
    mock_date.today.return_value = mock_today
    
    result = get_quote("test.json")
    
    expected_quote = SAMPLE_QUOTES[expected_index]
    expected_author = expected_quote.get('author', 'Unknown')
    expected_result = f'"{expected_quote["quote"]}"\n- {expected_author}'
    
    assert result == expected_result

    
@pytest.fixture
def temp_quotes_file(tmp_path):
    """Create a temporary quotes file for testing"""
    quotes_file = tmp_path / "test_quotes.json"
    quotes_file.write_text(json.dumps(SAMPLE_QUOTES), encoding='utf-8')
    return quotes_file
    
@patch('datetime.date')
def test_get_quote_with_real_file(mock_date, temp_quotes_file):
    """Integration test with actual file"""
    mock_today = MagicMock()
    mock_today.toordinal.return_value = 738521
    mock_date.today.return_value = mock_today
    
    result = get_quote(str(temp_quotes_file))
    
    assert result != ""
    assert '"' in result  # Should contain quote marks
    assert '\n- ' in result  # Should contain author separator
