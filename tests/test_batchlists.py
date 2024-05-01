"""Description

Test module for the BatchLists dataclass."""

import os
import sys
import pytest

from BatchMonitor import Batch, BatchCollection, BatchLists


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def batchlists_fixture():
    """Fixture for the BatchLists class"""
    return BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xstrawberry, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 7xcherries"),
                ],
                "seller2",
            ),
        ]
    )


def test_BatchLists(batchlists_fixture):
    """Test of the BatchLists class"""

    assert isinstance(batchlists_fixture, BatchLists)


def test_same_items_batchlists(batchlists_fixture):
    """Test of the BatchLists class with the same items in the batches"""

    assert batchlists_fixture == BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str(
                        "batch 1:1; 2xapple, 3xbanana, 0xorange, 0xpineapple"
                    ),
                    Batch.from_str(
                        "batch 2:2; 4xorange, 5xpineapple, 0xapple, 0xbanana"
                    ),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str(
                        "batch 3:3; 6xstrawberry, 7xbanana, 0xorange, 0xcherries"
                    ),
                    Batch.from_str(
                        "batch 4:4; 8xorange, 7xcherries, 0xstrawberry, 0xbanana"
                    ),
                ],
                "seller2",
            ),
        ]
    )


def test_add_batch_post_init():
    """Test of the add_batch method of the BatchLists class after the initialization"""

    bl = BatchLists.from_str(
        strings=[
            "seller1_batch 1:1; 2xapple, 3xbanana",
            "seller1_batch 3:3; 6xapple, 7xbanana",
            "seller2_batch 5:5; 10xapple, 11xbanana",
        ]
    )
    waited = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 3:3; 6xapple, 7xbanana"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 5:5; 10xapple, 11xbanana"),
                ],
                "seller2",
            ),
        ]
    )

    assert bl == waited


def test_str_batchLists(batchlists_fixture):
    """Test of the __str__ method of the BatchLists class"""

    assert "Seller" in str(batchlists_fixture)
    assert "Batch" in str(batchlists_fixture)
    assert "Price" in str(batchlists_fixture)
    assert "Item name" in str(batchlists_fixture)


def test_getitem_batchLists(batchlists_fixture):
    """Test of the __getitem__ method of the BatchLists class"""

    waited = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 555xstrawberry, 6666xbanana"),
                    Batch.from_str("batch 4:4; 58xorange, 7777xcherries"),
                ],
                "seller2",
            ),
        ]
    )[0]
    assert batchlists_fixture[0] == waited

    assert batchlists_fixture["batchlists"] == batchlists_fixture.batchlists
    assert batchlists_fixture["seller1"] == waited
    assert not batchlists_fixture[None]


def test_error_getitem_batchLists(batchlists_fixture):
    """Test of the __getitem__ method of the BatchLists class with errors"""

    with pytest.raises(KeyError):
        batchlists_fixture["seller3"]

    with pytest.raises(IndexError):
        batchlists_fixture[3]


def test_hash_batchLists(batchlists_fixture):
    """Test of the __hash__ method of the BatchLists class"""

    assert isinstance(hash(batchlists_fixture), int)


def test_iter_batchLists(batchlists_fixture):
    """Test of the __iter__ method of the BatchLists class"""

    for i, batch in enumerate(batchlists_fixture):
        assert isinstance(batch, BatchCollection)


def test_len_batchLists(batchlists_fixture):
    """Test of the __len__ method of the BatchLists class"""

    assert len(batchlists_fixture) == 2


def test_contains_batchLists(batchlists_fixture):
    """Test of the __contains__ method of the BatchLists class"""

    assert "seller1" in batchlists_fixture
    assert "seller2" in batchlists_fixture
    assert "seller3" not in batchlists_fixture


def test_eq_batchLists(batchlists_fixture):
    """Test of the __eq__ method of the BatchLists class"""

    assert batchlists_fixture == batchlists_fixture
    assert not batchlists_fixture == BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
        ]
    )
    not_implemented = batchlists_fixture.__eq__(1)
    assert not_implemented is NotImplemented


def test_ne_batchLists(batchlists_fixture):
    """Test of the __ne__ method of the BatchLists class"""

    assert not batchlists_fixture != batchlists_fixture
    assert batchlists_fixture != BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
        ]
    )
    not_implemented = batchlists_fixture.__ne__(1)
    assert not_implemented is NotImplemented


def test_lt_batchLists(batchlists_fixture):
    """Test of the __lt__ method of the BatchLists class"""

    assert batchlists_fixture < BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xstrawberry, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 7xcherries"),
                ],
                "seller2",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 5:5; 10xstrawberry, 11xbanana"),
                    Batch.from_str("batch 6:6; 12xorange, 13xcherries"),
                ],
                "seller3",
            ),
        ]
    )
    assert not batchlists_fixture < BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
        ]
    )

    assert not batchlists_fixture < batchlists_fixture


def test_le_batchLists(batchlists_fixture):
    """Test of the __le__ method of the BatchLists class"""

    assert batchlists_fixture <= BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xstrawberry, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 7xcherries"),
                ],
                "seller2",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 5:5; 10xstrawberry, 11xbanana"),
                    Batch.from_str("batch 6:6; 12xorange, 13xcherries"),
                ],
                "seller3",
            ),
        ]
    )
    assert batchlists_fixture <= batchlists_fixture
    assert not batchlists_fixture <= BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                ],
                "seller1",
            ),
        ]
    )


def test_gt_batchLists(batchlists_fixture):
    """Test of the __gt__ method of the BatchLists class"""

    assert (
        BatchLists(
            [
                BatchCollection(
                    [
                        Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                        Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                    ],
                    "seller1",
                ),
                BatchCollection(
                    [
                        Batch.from_str("batch 3:3; 6xstrawberry, 7xbanana"),
                        Batch.from_str("batch 4:4; 8xorange, 7xcherries"),
                    ],
                    "seller2",
                ),
                BatchCollection(
                    [
                        Batch.from_str("batch 5:5; 10xstrawberry, 11xbanana"),
                        Batch.from_str("batch 6:6; 12xorange, 13xcherries"),
                    ],
                    "seller3",
                ),
            ]
        )
        > batchlists_fixture
    )
    assert (
        not BatchLists(
            [
                BatchCollection(
                    [
                        Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                        Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                    ],
                    "seller1",
                ),
            ]
        )
        > batchlists_fixture
    )

    assert not batchlists_fixture > batchlists_fixture


def test_ge_batchLists(batchlists_fixture):
    """Test of the __ge__ method of the BatchLists class"""

    assert (
        BatchLists(
            [
                BatchCollection(
                    [
                        Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                        Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                    ],
                    "seller1",
                ),
                BatchCollection(
                    [
                        Batch.from_str("batch 3:3; 6xstrawberry, 7xbanana"),
                        Batch.from_str("batch 4:4; 8xorange, 7xcherries"),
                    ],
                    "seller2",
                ),
                BatchCollection(
                    [
                        Batch.from_str("batch 5:5; 10xstrawberry, 11xbanana"),
                        Batch.from_str("batch 6:6; 12xorange, 13xcherries"),
                    ],
                    "seller3",
                ),
            ]
        )
        >= batchlists_fixture
    )
    assert batchlists_fixture >= batchlists_fixture
    assert (
        not BatchLists(
            [
                BatchCollection(
                    [
                        Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                        Batch.from_str("batch 2:2; 4xorange, 5xpineapple"),
                    ],
                    "seller1",
                ),
            ]
        )
        >= batchlists_fixture
    )


def test_add_BatchCollection_batchLists():
    """Test of the add_BatchCollection method of the BatchLists class"""
    bl = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 3:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 4:2; 4xorange, 5xkiwi"),
                ],
                "seller1",
            )
        ]
    )
    bc = BatchCollection(
        [
            Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
            Batch.from_str("batch 2:2; 4xorange, 5xkiwi"),
        ],
        "seller2",
    )
    bl.add_BatchCollection(bc)
    assert len(bl) == 2
    assert bl[1] == bc

    with pytest.raises(ValueError):
        bl.add_BatchCollection(bc)

    bc = BatchCollection.from_str(
        "batch 1:1; 2xapple, 3xbanana",
        "batch 2:2; 4xorange, 5xkiwi",
        seller="seller10",
    )

    assert bl.add_BatchCollection(bc) == bl.from_str(
        strings=[
            "seller1_batch 3:1; 2xapple, 3xbanana",
            "seller1_batch 4:2; 4xorange, 5xkiwi",
            "seller2_batch 1:1; 2xapple, 3xbanana",
            "seller2_batch 2:2; 4xorange, 5xkiwi",
            "seller10_batch 1:1; 2xapple, 3xbanana",
            "seller10_batch 2:2; 4xorange, 5xkiwi",
        ]
    )


def test_add_batchcollection_same_seller(batchlists_fixture):
    """Test of the add_BatchCollection method of the BatchLists class with the same seller"""

    bc = BatchCollection(
        [
            Batch.from_str("batch 5:3; 6xstrawberry, 7xbanana"),
            Batch.from_str("batch 6:4; 8xorange, 7xcherries"),
        ],
        "seller2",
    )
    batchlists_fixture.add_BatchCollection(bc)
    assert len(batchlists_fixture) == 2
    assert batchlists_fixture == BatchLists.from_str(
        strings=[
            "seller1_batch 1:1; 2xapple, 3xbanana",
            "seller1_batch 2:2; 4xorange, 5xpineapple",
            "seller2_batch 3:3; 6xstrawberry, 7xbanana",
            "seller2_batch 4:4; 8xorange, 7xcherries",
            "seller2_batch 5:3; 6xstrawberry, 7xbanana",
            "seller2_batch 6:4; 8xorange, 7xcherries",
        ]
    )


def test_remove_BatchCollection_batchLists():
    """Test of the remove method of the BatchLists class"""
    bl = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xkiwi"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xapple, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 9xkiwi"),
                ],
                "seller2",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 5:5; 10xapple, 11xbanana"),
                    Batch.from_str("batch 6:6; 12xorange, 13xkiwi"),
                ],
                "seller3",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 7:7; 14xapple, 15xbanana"),
                    Batch.from_str("batch 8:8; 16xorange, 17xkiwi"),
                ],
                "seller4",
            ),
        ]
    )
    bl.remove_BatchCollection(index=0)
    assert len(bl) == 3
    assert bl[0].seller == "seller2"
    bl.remove_BatchCollection(seller_name="seller2")
    assert len(bl) == 2
    bl.remove_BatchCollection(index=[0, 1])
    assert len(bl) == 0


def test_no_remove_BatchCollection_batchLists(batchlists_fixture):
    """Test of the remove method of the BatchLists class with 0 value"""

    batchlists_fixture.remove_BatchCollection() == batchlists_fixture


def test_find_batchLists():
    """Test of the find method of the BatchLists class"""
    bl = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xkiwi"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xapple, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 9xkiwi"),
                ],
                "seller2",
            ),
        ]
    )

    assert bl.find(seller="seller1") == 0
    assert not bl.find(seller="seller3")


def test_sort_batchLists():
    """Test of the sort method of the BatchLists class"""
    bl = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 3:3; 6xapple, 7xbanana"),
                    Batch.from_str("batch 4:4; 8xorange, 9xkiwi"),
                    Batch.from_str("batch 5:5; 10xapple, 11xbanana"),
                ],
                "seller2",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 2:2; 4xorange, 5xkiwi"),
                ],
                "seller1",
            ),
        ]
    )
    bl.sort(by="seller")
    assert bl[0].seller == "seller1"
    assert bl[1].seller == "seller2"
    bl.sort(by="number_of_batches", reverse=True)
    assert bl[0].seller == "seller2"


def test_sort_error_batchLists(batchlists_fixture):
    """Test of the sort method of the BatchLists class with errors"""

    with pytest.raises(ValueError):
        batchlists_fixture.sort(by="zzzz", reverse=True)


def test_Batchlists_from_str():
    """Test of the from_str method of the BatchLists class"""

    bl = BatchLists.from_str(
        strings=[
            "seller1_batch 1:1; 2xapple, 3xbanana",
            "seller1_batch 3:3; 6xapple, 7xbanana",
            "seller2_batch 5:5; 10xapple, 11xbanana",
        ]
    )

    waited = BatchLists(
        [
            BatchCollection(
                [
                    Batch.from_str("batch 1:1; 2xapple, 3xbanana"),
                    Batch.from_str("batch 3:3; 6xapple, 7xbanana"),
                ],
                "seller1",
            ),
            BatchCollection(
                [
                    Batch.from_str("batch 5:5; 10xapple, 11xbanana"),
                ],
                "seller2",
            ),
        ]
    )

    assert bl == waited


def test_batchlists_to_json_exception():
    """Test of the to_json method of the BatchLists class with errors"""

    with pytest.raises(Exception):
        BatchLists.to_json(path="ddddddddddddddddd")
