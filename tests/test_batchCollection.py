"""Description

Test module for the BatchCollection dataclass."""

import os
import sys
import pytest

from BatchMonitor import (
    Batch,
    BatchCollection,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def batch_collection_fixture():
    """Fixture for the BatchCollection class"""

    return BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_BatchCollection(batch_collection_fixture):
    """Test of the BatchCollection class"""

    assert isinstance(batch_collection_fixture, BatchCollection)
    assert batch_collection_fixture.seller == "Default seller"


def test_same_name_several_times_BatchCollection():
    """Test of the BatchCollection class with same names"""

    with pytest.raises(ValueError):
        BatchCollection(
            [
                Batch.from_str("lot1:1; 2xarme 1, 3xarme 2"),
                Batch.from_str("lot1:2; 4xarme 3, 5xarme 4, 6xarme 5"),
            ]
        )


def test_incomplete_Batch(batch_collection_fixture):
    """Test of the addition in the BatchCollection class with incomplete batches"""

    waited = BatchCollection(
        batch_list=[
            Batch.from_str(
                "batch 1:1; 2xapple, 3xbanana, 4xkiwi, 0xpineapple, 0xcherries"
            ),
            Batch.from_str(
                "batch 2:2; 4xapple, 3xpineapple, 0xbanana, 0xkiwi, 0xcherries"
            ),
            Batch.from_str(
                "batch 3:3; 6xapple, 7xbanana, 8xcherries, 0xkiwi, 0xpineapple"
            ),
        ]
    )

    assert batch_collection_fixture == waited


def test_remove_null_item_in_all_batches():
    """Test if the post_init process remove the useless items of the BatchCollection class"""

    bc = BatchCollection(
        [
            Batch.from_str("lot1:1; 2xapple, 3xbanana, 0xkiwi"),
            Batch.from_str("lot2:2; 4xapple, 5xbanana, 0xcherries"),
        ]
    )

    assert bc == BatchCollection(
        [
            Batch.from_str("lot1:1; 2xapple, 3xbanana"),
            Batch.from_str("lot2:2; 4xapple, 5xbanana"),
        ]
    )


def test_raise_warning_incomplete_batch():
    """Test of the BatchCollection warning class with incomplete batches"""

    with pytest.warns(UserWarning):
        BatchCollection(
            [
                Batch.from_str("lot1:1; 2xapple, 3xcherries, 0xkiwi"),
                Batch.from_str("lot2:2; 4xapple, 5xbanana"),
            ]
        )


def test_str_BatchCollection(batch_collection_fixture):
    """Test of the str method of the BatchCollection class"""

    output = str(batch_collection_fixture)

    assert "Default seller" in output
    assert "Batch" in output
    assert "1" in output
    assert "Item name"
    assert "Price" in output
    assert "Quantity" in output


def test_get_item_in_batchCollection(batch_collection_fixture):
    """Test of the getitem function of the BatchCollection class"""

    assert batch_collection_fixture["seller"] == "Default seller"
    assert batch_collection_fixture["batch_list"] == batch_collection_fixture.batch_list
    assert batch_collection_fixture[0] == batch_collection_fixture.batch_list[0]


def test_error_get_item_in_batchCollection(batch_collection_fixture):
    """Test of the getitem function of the BatchCollection class"""

    with pytest.raises(IndexError):
        batch_collection_fixture[10]
    with pytest.raises(KeyError):
        batch_collection_fixture["error"]


def test_iter_batchCollection(batch_collection_fixture):
    """Test of the iter function of the BatchCollection class"""

    for batch in batch_collection_fixture:
        assert isinstance(batch, Batch)


def test_len_batchCollection(batch_collection_fixture):
    """Test of the len function of the BatchCollection class"""

    assert len(batch_collection_fixture) == 3


def test_contains_batchCollection(batch_collection_fixture):
    """Test of the contains function of the BatchCollection class"""

    assert "batch 1" in batch_collection_fixture
    assert "batch 4" not in batch_collection_fixture


def test_hash_batchCollection(batch_collection_fixture):
    """Test of the hash function of the BatchCollection class"""

    assert isinstance(hash(batch_collection_fixture), int)


def test_add_batchCollection(batch_collection_fixture):
    """Test of the add function of the BatchCollection class"""

    bc_to_add = BatchCollection(
        seller="seller1",
        batch_list=[
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ],
    )
    assert batch_collection_fixture + bc_to_add == BatchCollection(
        seller="Default seller + seller1",
        batch_list=[
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ],
    )


def test_add_same_batch_name_batchCollection(batch_collection_fixture):
    """Test of the add function of the BatchCollection class with same batch names"""

    bc_to_add = BatchCollection(
        seller="seller1",
        batch_list=[
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ],
    )
    assert batch_collection_fixture + bc_to_add == BatchCollection(
        seller="Default seller + seller1",
        batch_list=[
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 1 from seller1:1; 2xapple, 3xbanana, 4xkiwi"),
        ],
    )


def test_eq_batchCollection(batch_collection_fixture):
    """Test of the eq function of the BatchCollection class"""

    assert batch_collection_fixture == batch_collection_fixture
    assert not batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    not_implemented = batch_collection_fixture.__eq__("apple")
    assert not_implemented is NotImplemented


def test_ne_batchCollection(batch_collection_fixture):
    """Test of the ne function of the BatchCollection class"""

    assert not batch_collection_fixture != batch_collection_fixture
    assert batch_collection_fixture != BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    not_implemented = batch_collection_fixture.__ne__("apple")
    assert not_implemented is NotImplemented


def test_le_batchCollection(batch_collection_fixture):
    """Test of the le function of the BatchCollection class"""

    assert batch_collection_fixture <= batch_collection_fixture
    assert batch_collection_fixture <= BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    assert not batch_collection_fixture <= BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_lt_batchCollection(batch_collection_fixture):
    """Test of the lt function of the BatchCollection class"""

    assert not batch_collection_fixture < batch_collection_fixture
    assert batch_collection_fixture < BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    assert not batch_collection_fixture < BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_ge_batchCollection(batch_collection_fixture):
    """Test of the ge function of the BatchCollection class"""

    assert batch_collection_fixture >= batch_collection_fixture
    assert batch_collection_fixture >= BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    assert not batch_collection_fixture >= BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_gt_batchCollection(batch_collection_fixture):
    """Test of the gt function of the BatchCollection class"""

    assert not batch_collection_fixture > batch_collection_fixture
    assert batch_collection_fixture > BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )
    assert not batch_collection_fixture > BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_are_equal_batchCollection(batch_collection_fixture):
    """Test of the are_equal method of the BatchCollection class"""

    bc_to_compare = BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple"),
            Batch.from_str("batch 2:2; 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )
    assert not batch_collection_fixture.are_equal(bc_to_compare)
    assert batch_collection_fixture.are_equal(
        BatchCollection(
            [
                Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
                Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
                Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            ]
        )
    )


def test_batchCollection_from_str(batch_collection_fixture):
    """Test of the from_str method of the BatchCollection class"""

    waited = BatchCollection.from_str(
        "batch 1:1; 2xapple, 3xbanana, 4xkiwi",
        "batch 2:2; 4xapple, 3xpineapple",
        "batch 3:3; 6xapple, 7xbanana, 8xcherries",
        seller="Default seller",
    )

    assert batch_collection_fixture == waited


def test_add_batch_in_batchCollection(batch_collection_fixture):
    """Test of the add_batch method of the BatchCollection class"""

    batch_collection_fixture.add_batch(
        Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi")
    )

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_add_several_batches_in_batchCollection(batch_collection_fixture):
    """Test of the add_batch method of the BatchCollection class"""

    batch_collection_fixture.add_batch(
        Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
        Batch.from_str("batch 5:5; 2xapple, 3xbanana, 4xkiwi"),
        Batch.from_str("batch 6:6; 2xapple, 3xbanana, 4xkiwi"),
    )

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
            Batch.from_str("batch 4:4; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 5:5; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 6:6; 2xapple, 3xbanana, 4xkiwi"),
        ]
    )


def test_error_add_batch_in_batchCollection(batch_collection_fixture):
    """Test of the add_batch method of the BatchCollection class"""

    with pytest.raises(ValueError):
        batch_collection_fixture.add_batch(
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
        )


def test_remove_batch_in_batchCollection_by_index(batch_collection_fixture):
    """Test of the remove_batch method of the BatchCollection class"""

    batch_collection_fixture.remove_batch(0)

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_remove_batch_in_batchCollection_by_index_list(batch_collection_fixture):
    """Test of the remove_batch method of the BatchCollection class"""

    batch_collection_fixture.remove_batch(0, 1)

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_remove_batch_in_batchCollection_by_name(batch_collection_fixture):
    """Test of the remove_batch method of the BatchCollection class"""

    batch_collection_fixture.remove_batch(batch_name="batch 2")

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_remove_batch_in_batchCollection_by_name_list(batch_collection_fixture):
    """Test of the remove_batch method of the BatchCollection class"""

    batch_collection_fixture.remove_batch(batch_name="batch 1", batch2="batch 2")

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_find_batchCollection_by_name(batch_collection_fixture):
    """Test of the find method of the BatchCollection class"""

    assert batch_collection_fixture.find("batch 1") == 0
    assert batch_collection_fixture.find("batch 2") == 1
    assert batch_collection_fixture.find("batch 3") == 2
    assert not batch_collection_fixture.find("batch 4")


def test_find_batchCollection_by_price(batch_collection_fixture):
    """Test of the find method of the BatchCollection class"""

    assert batch_collection_fixture.find(batch_price=1) == 0
    assert batch_collection_fixture.find(batch_price=2) == 1
    assert batch_collection_fixture.find(batch_price=3) == 2
    assert not batch_collection_fixture.find(batch_price=4)
    batch_collection_fixture.add_batch(
        Batch.from_str("batch 4:1; 2xapple, 3xbanana, 4xkiwi"),
    )
    assert batch_collection_fixture.find(batch_price=1) == [0, 3]


def test_sort_batchCollection_by_price(batch_collection_fixture):
    """Test of the sort method of the BatchCollection class"""

    batch_collection_fixture.add_batch(
        Batch.from_str("batch 4:0.5; 2xapple, 3xbanana, 4xkiwi"),
    )
    batch_collection_fixture.sort("price")

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch 4:0.5; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_sort_batchCollection_by_name(batch_collection_fixture):
    """Test of the sort method of the BatchCollection class"""

    batch_collection_fixture.add_batch(
        Batch.from_str("batch:0.5; 2xapple, 3xbanana, 4xkiwi"),
    )
    batch_collection_fixture.sort("name")

    assert batch_collection_fixture == BatchCollection(
        [
            Batch.from_str("batch:0.5; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 1:1; 2xapple, 3xbanana, 4xkiwi"),
            Batch.from_str("batch 2:2; 4xapple, 3xpineapple"),
            Batch.from_str("batch 3:3; 6xapple, 7xbanana, 8xcherries"),
        ]
    )


def test_error_to_json_batchCollection():
    """Test of the to_json method of the BatchCollection class"""

    with pytest.raises(Exception):
        BatchCollection.to_json(path="ddddddddddddddd")
