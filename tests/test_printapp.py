"""Descrition:

Test the print functions of the app."""

import os
import sys

import pytest
from unittest.mock import patch, MagicMock

from BatchMonitor.lib_app import (
    _printed_both,
    _printed_mbe,
    _printed_me,
)
from rich.table import Table


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_printed_me():
    """Test the _printed_me function"""

    mock_style_h2 = MagicMock()
    mock_animate_progress_bar = MagicMock()
    mock_resolution_progress_bar = MagicMock()
    mock_console_print = MagicMock()

    lay_batch = Table()
    lay_ilr = Table()
    lay_me = Table()

    with patch("BatchMonitor.lib_app._style_h2", mock_style_h2), patch(
        "BatchMonitor.lib_app._animate_progress_bar", mock_animate_progress_bar
    ), patch(
        "BatchMonitor.lib_app._resolution_progress_bar",
        mock_resolution_progress_bar,
    ), patch(
        "BatchMonitor.lib_app.console.print", mock_console_print
    ):

        _printed_me(lay_batch, lay_ilr, lay_me)

    mock_style_h2.assert_any_call("INITIALIZATION OF THE MAX EARNINGS PROBLEM")
    mock_animate_progress_bar.assert_called_once_with(
        "Initialization of the problem", total=2
    )
    mock_style_h2.assert_any_call("RESOLUTION OF THE MAX EARNINGS PROBLEM")
    mock_resolution_progress_bar.assert_called_once_with("Resolution of the problem")
    mock_console_print.assert_called()


def test_printed_mbe():
    """Test the _printed_mbe function"""

    mock_style_h2 = MagicMock()
    mock_resolution_progress_bar = MagicMock()
    mock_console_print = MagicMock()

    lay_batch = Table()
    lay_ilr = Table()
    lay_mbe = Table()

    with patch("BatchMonitor.lib_app._style_h2", mock_style_h2), patch(
        "BatchMonitor.lib_app._resolution_progress_bar",
        mock_resolution_progress_bar,
    ), patch("BatchMonitor.lib_app.console.print", mock_console_print):
        _printed_mbe(lay_batch, lay_ilr, lay_mbe)

    mock_style_h2.assert_any_call(
        "INITIALIZATION OF THE BATCH EXPENDITURE MINIMIZATION PROBLEM"
    )
    mock_style_h2.assert_any_call(
        "RESOLUTION OF THE BATCH EXPENDITURE MINIMIZATION PROBLEM"
    )
    mock_resolution_progress_bar.assert_any_call("Resolution of the problem")
    mock_console_print.assert_called()


def test_printed_both():
    """Test the _printed_both function"""

    mock_style_h2 = MagicMock()
    mock_resolution_progress_bar = MagicMock()
    mock_console_print = MagicMock()
    mock_layout = MagicMock()

    lay_batch = Table()
    lay_ilr = Table()
    lay_mbe = Table()
    lay_me = Table()

    with patch("BatchMonitor.lib_app._style_h2", mock_style_h2), patch(
        "BatchMonitor.lib_app._resolution_progress_bar",
        mock_resolution_progress_bar,
    ), patch("BatchMonitor.lib_app.console.print", mock_console_print), patch(
        "BatchMonitor.lib_app.Layout", mock_layout
    ):

        _printed_both(lay_batch, lay_ilr, lay_mbe, lay_me)

    mock_style_h2.assert_any_call(
        "INITIALIZATION OF THE MIN BATCH EXPENSE AND MAX EARNINGS PROBLEMS"
    )
    mock_style_h2.assert_any_call(
        "RESOLUTION OF THE MIN BATCH EXPENSE AND MAX EARNINGS PROBLEMS"
    )
    mock_resolution_progress_bar.assert_any_call("Resolution of the problems")
    mock_layout.assert_called()
    mock_console_print.assert_called()
