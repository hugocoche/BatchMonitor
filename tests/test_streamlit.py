"""Test for the streamlit app."""

# flake8: noqa: F401, F811
from BatchMonitor import (
    createDatabaseFromBatchLists,
    BatchLists,
)
from .fixture_optimization import Batch_Collection_fixture
import pandas as pd


def test_createDatabaseFromBatchLists(Batch_Collection_fixture):
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
