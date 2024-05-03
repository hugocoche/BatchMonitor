"""Description

Test module for the serialization method"""

# flake8: noqa: F401, F811
import os
import sys
import json
from BatchMonitor import BatchCollection, BatchLists, ItemListRequest
from tests import batch_collection_fixture, batchlists_fixture, ilr_fixture


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


os.makedirs("tests/serialization_test_object", exist_ok=True)
os.chdir("tests/serialization_test_object")


def test_batch_collection_serialization(batch_collection_fixture):
    """Test of the serialization of a BatchCollection object"""

    batch_collection_fixture.to_json("batch_collection.json")
    assert batch_collection_fixture == BatchCollection.from_json(
        "batch_collection.json"
    )
    os.remove("batch_collection.json")


def test_batchlists_serialization(batchlists_fixture):
    """Test of the serialization of a BatchLists object"""

    batchlists_fixture.to_json("batchlists.json")
    assert batchlists_fixture == BatchLists.from_json("batchlists.json")
    os.remove("batchlists.json")


def test_ilr_serialization(ilr_fixture):
    """Test of the serialization of an ItemListRequest object"""

    ilr_fixture.to_json("ilr.json")
    assert ilr_fixture == ItemListRequest.from_json("ilr.json")
    os.remove("ilr.json")


os.chdir("..")
os.removedirs("serialization_test_object")
