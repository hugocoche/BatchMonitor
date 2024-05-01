"""Description:

Test the style of the app."""

import os
import sys

import pytest

from unittest.mock import patch, MagicMock
from BatchMonitor.lib_app import (
    _style_h2,
    _styled_echo,
    _style_invalid_choice,
    _styled_prompt,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_styled_prompt():
    """Test the _styled_prompt function."""

    mock_prompt_ask = MagicMock()

    with patch("batches_optimization.lib_app.Prompt.ask", mock_prompt_ask):
        _styled_prompt("test_text")

    mock_prompt_ask.assert_called_once_with("[cyan]test_text[/cyan]")


def test_styled_echo():
    """Test the _styled_echo function."""

    mock_console_print = MagicMock()

    with patch("batches_optimization.lib_app.console.print", mock_console_print):
        _styled_echo("test_text")

    mock_console_print.assert_called_once_with("[rgb(255,255,0)]test_text")


def test_style_h2():
    """Test the _style_h2 function."""

    mock_console_print = MagicMock()

    with patch("batches_optimization.lib_app.console.print", mock_console_print):
        _style_h2("test_text")

    assert "magenta" == mock_console_print.call_args_list[0][1]["style"]
    assert "center" == mock_console_print.call_args_list[0][1]["justify"]
    assert "## test_text" == mock_console_print.call_args_list[0][0][1].markup


def test_style_invalid_choice():
    """Test the _style_invalid_choice function."""

    mock_console_print = MagicMock()

    with patch("batches_optimization.lib_app.console.print", mock_console_print):
        _style_invalid_choice("test_text")

    mock_console_print.assert_called_once_with(
        "test_text", ":angry: !", "\n", style="red"
    )
