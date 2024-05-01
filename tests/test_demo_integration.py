"""Description.

Integration tests for the demo commands of the BatchMonitor application"""

import os
import sys
from pathlib import Path
from subprocess import run

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_demo_batchcollection():
    """Test the demo_batchcollection.py command"""

    run(["python", "-m", "BatchMonitor", "demo-batchcollection"])
    waited_path = Path(".").resolve() / "demo_batchcollection.json"
    assert waited_path.exists()
    content = waited_path.read_text()
    assert (
        content
        == """
{
    "batch_list": [
        {
            "name": "batch 1",
            "price": 1.0,
            "items": [
                {
                    "name": "apple",
                    "quantity_in_batch": 2.0
                },
                {
                    "name": "banana",
                    "quantity_in_batch": 5.0
                },
                {
                    "name": "orange",
                    "quantity_in_batch": 6.0
                }
            ]
        },
        {
            "name": "batch 2",
            "price": 2.0,
            "items": [
                {
                    "name": "apple",
                    "quantity_in_batch": 3.0
                },
                {
                    "name": "banana",
                    "quantity_in_batch": 4.0
                },
                {
                    "name": "orange",
                    "quantity_in_batch": 5.0
                }
            ]
        },
        {
            "name": "batch 3",
            "price": 3.0,
            "items": [
                {
                    "name": "apple",
                    "quantity_in_batch": 4.0
                },
                {
                    "name": "banana",
                    "quantity_in_batch": 3.0
                },
                {
                    "name": "orange",
                    "quantity_in_batch": 4.0
                }
            ]
        }
    ],
    "seller": "seller 1"
}
""".strip()
    )
    waited_path.unlink()


def test_demo_batchlists():
    """Test the demo_batchlists.py command"""

    run(["python", "-m", "BatchMonitor", "demo-batchlists"])
    waited_path = Path(".").resolve() / "demo_batchlists.json"
    assert waited_path.exists()
    content = waited_path.read_text()
    assert (
        content
        == """
[
    {
        "batch_list": [
            {
                "name": "batch 1",
                "price": 1.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 2.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 5.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 6.0
                    }
                ]
            },
            {
                "name": "batch 2",
                "price": 2.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 5.0
                    }
                ]
            }
        ],
        "seller": "seller 1"
    },
    {
        "batch_list": [
            {
                "name": "batch 2",
                "price": 2.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 5.0
                    }
                ]
            },
            {
                "name": "batch 3",
                "price": 3.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 4.0
                    }
                ]
            },
            {
                "name": "batch 1",
                "price": 1.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 2.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 5.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 6.0
                    }
                ]
            }
        ],
        "seller": "seller 2"
    },
    {
        "batch_list": [
            {
                "name": "batch 3",
                "price": 3.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 4.0
                    }
                ]
            },
            {
                "name": "batch 1",
                "price": 1.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 2.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 5.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 6.0
                    }
                ]
            },
            {
                "name": "batch 2",
                "price": 2.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 5.0
                    }
                ]
            },
            {
                "name": "batch 4",
                "price": 3.0,
                "items": [
                    {
                        "name": "apple",
                        "quantity_in_batch": 4.0
                    },
                    {
                        "name": "banana",
                        "quantity_in_batch": 3.0
                    },
                    {
                        "name": "orange",
                        "quantity_in_batch": 4.0
                    }
                ]
            }
        ],
        "seller": "seller 3"
    }
]
""".strip()
    )
    waited_path.unlink()


def test_demo_itemlistrequest():
    """Test the demo_itemlistrequest.py command"""

    run(["python", "-m", "BatchMonitor", "demo-itemlistrequest"])
    waited_path = Path(".").resolve() / "demo_itemlistrequest.json"
    assert waited_path.exists()
    content = waited_path.read_text()
    assert (
        content
        == """
{
    "items": [
        {
            "name": "apple",
            "minimum_quantity": 1.0,
            "maximum_quantity": 3.0
        },
        {
            "name": "banana",
            "minimum_quantity": 2.0,
            "maximum_quantity": 5.0
        },
        {
            "name": "orange",
            "minimum_quantity": 3.0,
            "maximum_quantity": 4.0
        }
    ]
}
""".strip()
    )
    waited_path.unlink()
