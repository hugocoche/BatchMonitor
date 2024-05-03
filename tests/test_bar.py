"""Description

Unit tests for the bar progression of the app"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

from BatchMonitor.lib_app import (
    _resolution_progress_bar,
    _animate_progress_bar,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_animate_progress_bar():
    """Test the _animate_progress_bar function."""

    mock_console_print = MagicMock()
    mock_progress = MagicMock()
    mock_sleep = MagicMock()

    with patch("BatchMonitor.lib_app.console.print", mock_console_print), patch(
        "BatchMonitor.lib_app.Progress", mock_progress
    ), patch("time.sleep", mock_sleep):

        _animate_progress_bar("test_object", 10)

    mock_console_print.assert_called_once_with("\n \n")
    mock_progress.assert_called_once()
    mock_sleep.assert_called()


def test_resolution_progress_bar():
    """Test the _resolution_progress_bar function."""

    mock_console_print = MagicMock()
    mock_progress = MagicMock()
    mock_sleep = MagicMock()

    with patch("BatchMonitor.lib_app.console.print", mock_console_print), patch(
        "BatchMonitor.lib_app.Progress", mock_progress
    ), patch("time.sleep", mock_sleep):

        _resolution_progress_bar("test_object")

    mock_console_print.assert_called_once_with("\n \n")
    mock_progress.assert_called_once()
    mock_sleep.assert_called()
