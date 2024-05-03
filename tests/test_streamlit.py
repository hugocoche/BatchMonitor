"""Test for the streamlit app."""

# flake8: noqa: F401, F811
from BatchMonitor import (
    createDatabaseFromBatchLists,
    BatchLists,
    create_df_from_json,
)

from .fixture_optimization import Batch_Collection_fixture
import pandas as pd
from pathlib import Path


def test_createDatabaseFromBatchLists(Batch_Collection_fixture):
    """Test the function createDatabaseFromBatchLists"""

    batch_collection = Batch_Collection_fixture
    batch_lists = BatchLists([batch_collection])
    database = createDatabaseFromBatchLists(batch_lists)
    expected = {
        "seller1_batch 1": {"apple": 3.0, "banana": 2.0, "orange": 4.0, "Total": 10.0},
        "seller1_batch 2": {"apple": 5.0, "banana": 5.0, "orange": 5.0, "Total": 15.0},
        "seller1_batch 3": {"apple": 6.0, "banana": 7.0, "orange": 7.0, "Total": 20.0},
    }

    expected_df = pd.DataFrame(expected)

    assert database.equals(expected_df)


def test_create_df_from_json():
    """Test the function create_df_from_json"""

    bl = BatchLists.from_str(
        strings=[
            "seller1_batch1:10.0; 1xapple, 2xbanana",
            "seller1_batch2:20.0; 3xapple, 4xbanana",
            "seller2_batch1:30.0; 1xapple, 2xbanana",
            "seller2_batch2:40.0; 4xapple, 1xbanana",
            "seller3_batch1:30.0; 1xapple, 2xbanana",
            "seller3_batch2:40.0; 4xapple, 1xbanana",
            "seller4_batch1:30.0; 1xapple, 2xbanana",
            "seller4_batch2:40.0; 4xapple, 1xbanana",
        ]
    )
    bl.to_json("batchlists.json")
    df_bl = pd.read_json("batchlists.json")
    database = create_df_from_json(df_bl)
    waited = pd.DataFrame(
        data={
            "batch1.1": [1.0, 2.0, 10.0, "seller1"],
            "batch2.1": [3.0, 4.0, 20.0, "seller1"],
            "batch1.2": [1.0, 2.0, 30.0, "seller2"],
            "batch2.2": [4.0, 1.0, 40.0, "seller2"],
            "batch1.3": [1.0, 2.0, 30.0, "seller3"],
            "batch2.3": [4.0, 1.0, 40.0, "seller3"],
            "batch1.4": [1.0, 2.0, 30.0, "seller4"],
            "batch2.4": [4.0, 1.0, 40.0, "seller4"],
        },
        index=["apple", "banana", "TOTAL", "Seller"],
    )
    (Path(".").resolve() / "batchlists.json").unlink()
    assert database.equals(waited)
