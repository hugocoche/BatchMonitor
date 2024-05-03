"""Description.

Integration tests for the view commands of BatchMonitor application"""

import os
import sys
import pytest
from subprocess import run
from pathlib import Path


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_view_batchcollection():
    """Test of the view_batches command of the BatchMonitor application"""
    run(["python", "-m", "BatchMonitor", "demo-batchcollection"])
    result = run(
        [
            "python",
            "-m",
            "BatchMonitor",
            "view-batches",
            "demo_batchcollection.json",
        ],
        capture_output=True,
    )
    output = result.stdout.decode()

    expected_rows = [
        "The batches sold by seller 1",
        "Batch           │        Price        │ Items",  # Header row
        "batch 1          │         1.0         │ 2 apple",
        "5 banana",
        "6 orange",
        "batch 2          │         2.0         │ 3 apple",
        "4 banana",
        "5 orange",
        "batch 3          │         3.0         │ 4 apple",
        "3 banana",
        "4 orange",
    ]
    for row in expected_rows:
        assert row in output
    (Path(".").resolve() / "demo_batchcollection.json").unlink()


def test_view_batchlists():
    """Test of the view_batchlists command of the BatchMonitor application"""

    run(["python", "-m", "BatchMonitor", "demo-batchlists"])
    result = run(
        [
            "python",
            "-m",
            "BatchMonitor",
            "view-batches",
            "demo_batchlists.json",
        ],
        capture_output=True,
    )
    output = result.stdout.decode()

    expected_rows = [
        "The batches sold by each seller",
        "┌─────────────────────┬───────────────────┬──────────────┬────────────────────┐",
        "│       Seller        │       Batch       │    Price     │ Items              │",
        "│      seller 1       │                   │              │                    │",
        "│                     │      batch 1      │     1.0      │ 2 apple            │",
        "│                     │      batch 2      │     2.0      │ 3 apple            │",
        "│      seller 2       │                   │              │                    │",
        "│                     │      batch 2      │     2.0      │ 3 apple            │",
        "│                     │      batch 3      │     3.0      │ 4 apple            │",
        "│      seller 3       │                   │              │                    │",
        "│                     │      batch 3      │     3.0      │ 4 apple            │",
        "│                     │      batch 1      │     1.0      │ 2 apple            │",
        "└─────────────────────┴───────────────────┴──────────────┴────────────────────┘",
    ]
    for row in expected_rows:
        assert row in output

    (Path(".").resolve() / "demo_batchlists.json").unlink()


def test_view_itemlistrequest():
    """Test of the view-itemlist command of the BatchMonitor application"""

    run(["python", "-m", "BatchMonitor", "demo-itemlistrequest"])
    result = run(
        [
            "python",
            "-m",
            "BatchMonitor",
            "view-ilr",
            "demo_itemlistrequest.json",
        ],
        capture_output=True,
    )
    output = result.stdout.decode()

    expected_rows = [
        "The items requested by the customer",
        "┌──────────────┬───────────────────────────────┬──────────────────────────────┐",
        "│     Item     │       Minimum Quantity        │       Maximum Quantity       │",
        "│    apple     │              1.0              │             3.0              │",
        "│    banana    │              2.0              │             5.0              │",
        "│    orange    │              3.0              │             4.0              │",
        "└──────────────┴───────────────────────────────┴──────────────────────────────┘",
    ]
    for row in expected_rows:
        assert row in output
    (Path(".").resolve() / "demo_itemlistrequest.json").unlink()


def test_raise_error():
    """Test of the errors of the view commands of the BatchMonitor application"""
    run(["python", "-m", "BatchMonitor", "demo-batchcollection"])
    out = run(
        [
            "python",
            "-m",
            "BatchMonitor",
            "view-ilr",
            "demo_batchcollection.json",
        ]
    )
    assert out.returncode == 1

    run(["python", "-m", "BatchMonitor", "demo-itemlistrequest"])
    out = run(
        [
            "python",
            "-m",
            "BatchMonitor",
            "view-batches",
            "demo_itemlistrequest.json",
        ]
    )
    assert out.returncode == 1

    (Path(".").resolve() / "demo_batchcollection.json").unlink()
    (Path(".").resolve() / "demo_itemlistrequest.json").unlink()
