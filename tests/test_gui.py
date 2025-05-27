import os
from app.gui import LOGO_PATH

def test_logo_file_exists():
    assert os.path.exists(os.path.join("app", LOGO_PATH))
