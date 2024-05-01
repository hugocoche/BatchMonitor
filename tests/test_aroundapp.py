"""Description:

Test other functionalities of the app."""

import os
import sys
import io
import pytest
from unittest.mock import patch, MagicMock

from BatchMonitor.__main__ import _restart_app
from BatchMonitor.lib_app import _thanks

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_restart_app():
    """Test the _restart_app function"""

    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        with patch("sys.stdin", io.StringIO("no\n")):
            with pytest.raises(SystemExit):
                _restart_app()

    stdout = fake_stdout.getvalue()
    assert "Do you want to restart the app ?" in stdout


def test_invalid_choice_restart_app():
    """Test the _style_invalid_choice function"""

    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        with patch("sys.stdin", io.StringIO("invalid\nno\n")):
            with pytest.raises(SystemExit):
                _restart_app()

    stdout = fake_stdout.getvalue()
    assert "Invalid choice. Please choose between yes or no." in stdout


def test_thanks():
    """Test the _thanks function"""

    mock_console_print = MagicMock()

    with patch("BatchMonitor.lib_app.console.print", mock_console_print):
        _thanks()

    mock_console_print.assert_any_call(
        r"""
_________________________________________________________
|     _____  _   _    _    _   _  _  _  _____            |
|       |    |   |  (   )  |\  |  |  /  |        | | |   |
|       |    |___|  |___|  | \ |  | /   |___     | | |   |
|       |    |   |  |   |  |  \|  |/\       |    | | |   |
|       |    |   |  |   |  |   |  |  \  ____|    . . .   |
|________________________________________________________|
""",
        style="white",
        justify="center",
    )
    mock_console_print.assert_any_call(
        r"""
|                                          /\             /\             /\                                        |
|                                         /  \           /  \           /  \                                       |
|                                        /    \         /    \         /    \                                      |
|                                       /______\       /______\       /______\                                     |
|                                       |      |       |      |       |      |                                     |
|                                       |      |       |      |       |      |                                     |
|                                       |  /\  |       |  /\  |       |  /\  |                                     |
|                                       | /  \ |       | /  \ |       | /  \ |                                     |
|                                       |/____\|       |/____\|       |/____\|                                     |
|                                      /|      |\     /|      |\     /|      |\                                    |
|                                     /_|______|_\   /_|______|_\   /_|______|_\                                   |
|                                    |  |      |  | |  |      |  | |  |      |  |                                  |
|                                    |__|______|__| |__|______|__| |__|______|__|                                  |
|                                       |      |       |      |       |      |                                     |
|                                       |      |       |      |       |      |                                     |
""",
        style="white",
        justify="center",
    )
