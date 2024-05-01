"""Description.

Tests for the batch dataclass.
"""

import os
import sys
import pytest

from BatchMonitor import (
    Item_in_batch,
    Batch,
)

from BatchMonitor.lib_batches import Incompatible_negative_value


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def batch_fixture():
    return Batch(
        name="batch 1",
        price=1.0,
        items=[
            Item_in_batch("apple", 1.0),
            Item_in_batch("banana", 2.0),
            Item_in_batch("orange", 3.0),
        ],
    )


def test_Batch(batch_fixture):
    """Test of the Batch class"""

    assert batch_fixture == Batch(
        name="batch 1",
        price=1.0,
        items=[
            Item_in_batch("apple", 1.0),
            Item_in_batch("banana", 2.0),
            Item_in_batch("orange", 3.0),
        ],
    )
    assert isinstance(batch_fixture, Batch)
    assert batch_fixture.name == "batch 1"
    assert batch_fixture.price == 1.0
    assert batch_fixture.items == [
        Item_in_batch("apple", 1.0),
        Item_in_batch("banana", 2.0),
        Item_in_batch("orange", 3.0),
    ]


def test_error_negative_values_Batch():
    """Test of the negative values errors of Batch class"""

    with pytest.raises(Incompatible_negative_value):
        Batch(
            name="batch 1",
            price=-1.0,
            items=[Item_in_batch("apple", 1.0), Item_in_batch("banana", 2.0)],
        )
    with pytest.raises(Incompatible_negative_value):
        Batch(
            name="batch 1",
            price=1.0,
            items=[Item_in_batch("apple", -1.0), Item_in_batch("banana", 2.0)],
        )
    with pytest.raises(Incompatible_negative_value):
        Batch(
            name="batch 1",
            price=1.0,
            items=[Item_in_batch("apple", 1.0), Item_in_batch("banana", -2.0)],
        )


def test_init_empty_Batch():
    """Test of the Batch class with empty items"""

    batch = Batch(name="batch 1", price=1.0, items=[])
    assert batch == Batch(name="batch 1", price=1.0, items=[])


def test_invalid_Batch_name():
    """Test of the Batch class with same name for different items"""

    with pytest.raises(ValueError):
        Batch(
            name="batch 1",
            price=1.0,
            items=[Item_in_batch("apple", 1.0), Item_in_batch("apple", 2.0)],
        )


def test_Batch_from_str(batch_fixture):
    """Test of the from_str function of the Batch class"""

    assert batch_fixture == Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")


def test_hash_Batch(batch_fixture):
    """Test of the hash function of Batch"""

    assert hash(batch_fixture) == hash(
        Batch(
            name="batch 1",
            price=1.0,
            items=[
                Item_in_batch("apple", 1.0),
                Item_in_batch("banana", 2.0),
                Item_in_batch("orange", 3.0),
            ],
        )
    )


def test_str_Batch(batch_fixture):
    """Test of the str function of Batch"""

    output = str(batch_fixture)
    assert "Batch" in output
    assert "Price" in output
    assert "Item name" in output
    assert "Quantity" in output


def test_getitem_Batch(batch_fixture):
    """Test of the getitem function of Batch"""

    assert batch_fixture[0] == Item_in_batch("apple", 1.0)
    assert batch_fixture[1] == Item_in_batch("banana", 2.0)
    assert batch_fixture[2] == Item_in_batch("orange", 3.0)
    assert batch_fixture["name"] == "batch 1"
    assert batch_fixture["price"] == 1.0
    assert batch_fixture["items"] == [
        Item_in_batch("apple", 1.0),
        Item_in_batch("banana", 2.0),
        Item_in_batch("orange", 3.0),
    ]


def test_get_item_error_Batch(batch_fixture):
    """Test of the index error of Batch"""

    with pytest.raises(IndexError):
        batch_fixture[10]
    with pytest.raises(KeyError):
        batch_fixture["invalid_key"]


def test_iter_Batch(batch_fixture):
    """Test of the iter function of Batch"""

    for index, item in enumerate(batch_fixture):
        assert item == batch_fixture[index]


def test_len_Batch(batch_fixture):
    """Test of the len function of Batch"""

    assert len(batch_fixture) == 3


def test_eq_Batch(batch_fixture):
    """Test of the eq function of Batch"""

    assert batch_fixture == Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")
    assert not batch_fixture == Batch.from_str("batch 2:1; 1xapple, 2xbanana, 3xorange")

    not_implemented = batch_fixture.__eq__("apple")
    assert not_implemented is NotImplemented


def test_ne_Batch(batch_fixture):
    """Test of the ne function of Batch"""

    assert not batch_fixture != Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")
    assert batch_fixture != Batch.from_str("batch 2:1; 1xapple, 2xbanana, 3xorange")

    not_implemented = batch_fixture.__ne__("apple")
    assert not_implemented is NotImplemented


def test_lt_Batch(batch_fixture):
    """Test of the lt function of Batch"""

    assert batch_fixture < Batch.from_str(
        "batch 2:1; 1xapple, 2xbanana, 3xorange, 4xkiwi"
    )
    assert not batch_fixture < Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")


def test_le_Batch(batch_fixture):
    """Test of the le function of Batch"""

    assert batch_fixture <= Batch.from_str(
        "batch 2:1; 1xapple, 2xbanana, 3xorange, 4xkiwi"
    )
    assert batch_fixture <= Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")
    assert not batch_fixture <= Batch.from_str("batch 1:1; 1xapple, 2xbanana")


def test_gt_Batch(batch_fixture):
    """Test of the gt function of Batch"""

    assert not batch_fixture > Batch.from_str(
        "batch 2:1; 1xapple, 2xbanana, 3xorange, 4xkiwi"
    )
    assert batch_fixture > Batch.from_str("batch 1:1; 1xapple, 2xbanana")


def test_ge_Batch(batch_fixture):
    """Test of the ge function of Batch"""

    assert not batch_fixture >= Batch.from_str(
        "batch 2:1; 1xapple, 2xbanana, 3xorange, 4xkiwi"
    )
    assert batch_fixture >= Batch.from_str("batch 1:1; 1xapple, 2xbanana")
    assert batch_fixture >= Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")


def test_contains_Batch(batch_fixture):
    """Test of the contains function of Batch"""

    assert "apple" in batch_fixture
    assert "banana" in batch_fixture
    assert "kiwi" not in batch_fixture


def test_add_Batch(batch_fixture):
    """Test of the add function of Batch"""

    batch_to_add = Batch.from_str("batch 2:1; 1xapple, 2xbanana, 3xorange, 4xkiwi")
    batch_result = batch_fixture + batch_to_add
    print(batch_result)
    assert batch_result == Batch.from_str(
        "batch 1 + batch 2:2; 2xapple, 4xbanana, 6xorange, 4xkiwi"
    )


def test_add_item_Batch(batch_fixture):
    """Test of the add_item function of Batch"""

    assert batch_fixture.add_item(Item_in_batch("kiwi", 4)) == Batch.from_str(
        "batch 1:1; 1xapple, 2xbanana, 3xorange, 4xkiwi"
    )


def test_add_same_item_Batch(batch_fixture):
    """Test of the add_item function of Batch with same item"""

    assert batch_fixture.add_item(
        Item_in_batch("apple", 4.0), add_quantities=True
    ) == Batch.from_str("batch 1:1; 5xapple, 2xbanana, 3xorange")


def test_add_list_item_Batch(batch_fixture):
    """Test of the add_item function of Batch with a list of items"""

    assert batch_fixture.add_item(
        Item_in_batch("kiwi", 4),
        Item_in_batch("apple", 2),
        add_quantities=True,
    ) == Batch.from_str("batch 1:1; 3xapple, 2xbanana, 3xorange, 4xkiwi")


def test_error_add_item_Batch(batch_fixture):
    """Test of the add_item function of Batch with error"""

    with pytest.raises(ValueError):
        Batch(name="batch 1", price=1.0, items=[]).add_item(
            Item_in_batch("apple", 1.0), Item_in_batch("apple", 2.0)
        )

    with pytest.raises(ValueError):
        batch_fixture.add_item(Item_in_batch("apple", 1.0))


def test_remove_item_Batch_by_index(batch_fixture):
    """Test of the remove_item function of Batch by one index"""

    assert batch_fixture.remove_item(0) == Batch.from_str(
        "batch 1:1; 2xbanana, 3xorange"
    )


def test_remove_item_Batch_by_name(batch_fixture):
    """Test of the remove_item function of Batch by one name"""

    assert batch_fixture.remove_item(item_name="apple") == Batch.from_str(
        "batch 1:1; 2xbanana, 3xorange"
    )


def test_remove_item_Batch_by_several_index(batch_fixture):
    """Test of the remove_item function of Batch by several index"""

    assert batch_fixture.remove_item(0, 1) == Batch.from_str("batch 1:1; 3xorange")


def test_remove_item_Batch_by_several_name(batch_fixture):
    """Test of the remove_item function of Batch by several name"""

    assert batch_fixture.remove_item(
        item_name="apple", banana="banana"
    ) == Batch.from_str("batch 1:1; 3xorange")


def test_find_item_name_Batch(batch_fixture):
    """Test of the find function of Batch"""

    assert batch_fixture.find_item(item_name="apple") == 0
    assert batch_fixture.find_item("banana") == 1
    assert not batch_fixture.find_item("kiwi")
    assert batch_fixture.find_item(item_name="orange") == 2


def test_find_item_quantity_Batch(batch_fixture):
    """Test of the find function of Batch"""

    assert batch_fixture.find_item(item_quantity=1) == 0
    assert batch_fixture.find_item(item_quantity=2) == 1
    assert batch_fixture.find_item(item_quantity=3) == 2
    batch_fixture.add_item(Item_in_batch("kiwi", 1))
    assert batch_fixture.find_item(item_quantity=1) == [0, 3]
    assert not batch_fixture.find_item(item_quantity=4)


def test_none_find_item_Batch(batch_fixture):
    """Test of the find function of Batch"""

    assert not batch_fixture.find_item()


def test_sort_name_Batch(batch_fixture):
    """Test of the sort function of Batch"""

    batch_fixture.add_item(Item_in_batch("aaaa", 0.5))
    batch_fixture.sort(by="name")
    assert batch_fixture == Batch(
        name="batch 1",
        price=1.0,
        items=[
            Item_in_batch("aaaa", 0.5),
            Item_in_batch("apple", 1.0),
            Item_in_batch("banana", 2.0),
            Item_in_batch("orange", 3.0),
        ],
    )


def test_sort_quantity_Batch(batch_fixture):
    """Test of the sort function of Batch"""

    batch_fixture.add_item(Item_in_batch("kiwi", 0.5))
    batch_fixture.sort(by="quantity")
    assert batch_fixture == Batch(
        name="batch 1",
        price=1.0,
        items=[
            Item_in_batch("kiwi", 0.5),
            Item_in_batch("apple", 1.0),
            Item_in_batch("banana", 2.0),
            Item_in_batch("orange", 3.0),
        ],
    )


def invalid_sort_Batch(batch_fixture):
    """Test of the sort function of Batch"""

    with pytest.raises(ValueError):
        batch_fixture.sort(by="invalid_key")


def test_are_equal_Batch(batch_fixture):
    """Test of the are_equal function of Batch"""

    assert batch_fixture.are_equal(
        Batch.from_str("batch 1:1; 1xapple, 2xbanana, 3xorange")
    )
    assert not batch_fixture.are_equal(Batch.from_str("batch 1:1; 1xapple, 2xbanana"))
