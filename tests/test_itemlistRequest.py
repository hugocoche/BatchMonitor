"""Descrition:

This file contains the test cases for the ItemlistRequest dataclass"""

import os
import sys
import pytest
from BatchMonitor import ItemListRequest, ItemRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def ilr_fixture():
    return ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )


def test_ItemListRequest(ilr_fixture):
    """Test of the ItemListRequest class"""

    assert ilr_fixture == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )


def test_error_unique_item(ilr_fixture):
    """Test of the error raised when the item is not unique"""

    with pytest.raises(ValueError):
        ItemListRequest(
            [
                ItemRequest("apple", 5, 6),
                ItemRequest("apple", 7, 8),
                ItemRequest("orange", 9, 10),
            ]
        )


def test_init_empty_ilr():
    """Test of the error raised when the item list is empty"""

    ilr = ItemListRequest([])
    assert ilr == ItemListRequest([])


def test_str_ilr(ilr_fixture):
    """Test of the str function of the ItemListRequest class"""

    assert "Item name" in str(ilr_fixture)
    assert "Maximum Quantity requested" in str(ilr_fixture)
    assert "Minimum Quantity requested" in str(ilr_fixture)


def test_get_item(ilr_fixture):
    """Test of the get_item function of the ItemListRequest class"""

    assert ilr_fixture["items"] == [
        ItemRequest("apple", 5, 6),
        ItemRequest("banana", 7, 8),
        ItemRequest("orange", 9, 10),
    ]
    assert ilr_fixture[0] == ItemRequest("apple", 5, 6)
    assert ilr_fixture[1] == ItemRequest("banana", 7, 8)
    assert ilr_fixture[2] == ItemRequest("orange", 9, 10)
    with pytest.raises(IndexError):
        ilr_fixture[3]


def test_len_ilr(ilr_fixture):
    """Test of the len function of the ItemListRequest class"""

    assert len(ilr_fixture) == 3


def test_iter_ilr(ilr_fixture):
    """Test of the iter function of the ItemListRequest class"""

    for i, item in enumerate(ilr_fixture):
        assert item == ilr_fixture[i]


def test_hash_ilr(ilr_fixture):
    """Test of the hash function of the ItemListRequest class"""

    assert hash(ilr_fixture) == hash(
        (
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        )
    )


def test_eq_ilr(ilr_fixture):
    """Test of the eq function of the ItemListRequest class"""

    assert ilr_fixture == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert not ilr_fixture == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 11),
        ]
    )
    not_implemented = ilr_fixture.__eq__(5)
    assert not_implemented is NotImplemented


def test_ne_ilr(ilr_fixture):
    """Test of the ne function of the ItemListRequest class"""

    assert ilr_fixture != ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 11),
        ]
    )
    assert not ilr_fixture != ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    not_implemented = ilr_fixture.__ne__(5)
    assert not_implemented is NotImplemented


def test_lt_ilr(ilr_fixture):
    """Test of the lt function of the ItemListRequest class"""

    assert not ilr_fixture < ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
        ]
    )
    assert not ilr_fixture < ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert ilr_fixture < ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_le_ilr(ilr_fixture):
    """Test of the le function of the ItemListRequest class"""

    assert not ilr_fixture <= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
        ]
    )
    assert ilr_fixture <= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert ilr_fixture <= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_ge_ilr(ilr_fixture):
    """Test of the ge function of the ItemListRequest class"""

    assert ilr_fixture >= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
        ]
    )
    assert ilr_fixture >= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert not ilr_fixture >= ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_gt_ilr(ilr_fixture):
    """Test of the gt function of the ItemListRequest class"""

    assert ilr_fixture > ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
        ]
    )
    assert not ilr_fixture > ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert not ilr_fixture > ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_contains_ilr(ilr_fixture):
    """Test of the contains function of the ItemListRequest class"""

    assert ItemRequest("apple", 5, 6) in ilr_fixture
    assert ItemRequest("banana", 7, 8) in ilr_fixture
    assert ItemRequest("orange", 9, 10) in ilr_fixture
    assert ItemRequest("cherries", 9, 10) not in ilr_fixture


def test_add_ilr(ilr_fixture):
    """Test of the add function of the ItemListRequest class"""

    ilr = ilr_fixture + ItemListRequest(
        [
            ItemRequest("cherries", 9, 10),
        ]
    )
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_error_add_ilr(ilr_fixture):
    """Test of the error raised when the item is not unique"""

    with pytest.raises(ValueError):
        ilr_fixture + ItemListRequest(
            [
                ItemRequest("apple", 5, 6),
                ItemRequest("banana", 7, 8),
                ItemRequest("orange", 9, 10),
            ]
        )


def test_from_str_ItemListRequest(ilr_fixture):
    """Test of the from_str function of the ItemListRequest class"""

    request_items = ItemListRequest.from_str(
        "5-6 of apple", "7-8 of banana", "9-10 of orange"
    )
    assert request_items == ilr_fixture


def test_add_item_ilr(ilr_fixture):
    """Test of the add_item function of the ItemListRequest class"""

    ilr = ilr_fixture.add_item(ItemRequest("cherries", 9, 10))
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
        ]
    )


def test_add_several_item_ilr(ilr_fixture):
    """Test of the add_item function of the ItemListRequest class"""

    ilr = ilr_fixture.add_item(
        ItemRequest("cherries", 9, 10),
        ItemRequest("strawberry", 9, 10),
        ItemRequest("blueberry", 9, 10),
    )
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("cherries", 9, 10),
            ItemRequest("strawberry", 9, 10),
            ItemRequest("blueberry", 9, 10),
        ]
    )


def test_error_add_item_ilr(ilr_fixture):
    """Test of the error raised when the item is not unique"""

    with pytest.raises(ValueError):
        ilr_fixture.add_item(ItemRequest("apple", 5, 6))


def test_remove_item_by_index_ilr(ilr_fixture):
    """Test of the remove_item function of the ItemListRequest class"""

    ilr = ilr_fixture.remove_item(1)
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("orange", 9, 10),
        ]
    )


def test_remove_several_item_by_index_ilr(ilr_fixture):
    """Test of the remove_item function of the ItemListRequest class"""

    ilr = ilr_fixture.remove_item(1, 2)
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
        ]
    )


def test_remove_item_by_name_ilr(ilr_fixture):
    """Test of the remove_item function of the ItemListRequest class"""

    ilr = ilr_fixture.remove_item(item_name="banana")
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("orange", 9, 10),
        ]
    )


def test_remove_several_item_by_name_ilr(ilr_fixture):
    """Test of the remove_item function of the ItemListRequest class"""

    ilr = ilr_fixture.remove_item(item_name="banana", orange="orange")
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
        ]
    )


def test_error_remove_item_by(ilr_fixture):
    """Test of the error raised when the item to remove is not in the list"""

    with pytest.raises(ValueError):
        ilr_fixture.remove_item(item_name="cherries")

    with pytest.raises(ValueError):
        ilr_fixture.remove_item(5)


def test_find_item_by_name(ilr_fixture):
    """Test of the find function of the ItemListRequest class"""

    index = ilr_fixture.find(item_name="banana")
    assert index == 1


def test_none_find_item_by_name(ilr_fixture):
    """Test of the error raised when the item to find is not in the list"""

    assert ilr_fixture.find(item_name="cherries") is None


def test_sort_item_by_name(ilr_fixture):
    """Test of the sort function by name of the ItemListRequest class"""

    ilr_fixture.add_item(ItemRequest("aaa", 9, 10))
    ilr = ilr_fixture.sort()
    assert ilr == ItemListRequest(
        [
            ItemRequest("aaa", 9, 10),
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
        ]
    )
    assert ilr_fixture.sort(reverse=True) == ItemListRequest(
        [
            ItemRequest("orange", 9, 10),
            ItemRequest("banana", 7, 8),
            ItemRequest("apple", 5, 6),
            ItemRequest("aaa", 9, 10),
        ]
    )


def test_sort_item_by_max(ilr_fixture):
    """Test of the sort function by maximum quantity of the ItemListRequest class"""

    ilr_fixture.add_item(ItemRequest("aaa", 9, 10))
    ilr = ilr_fixture.sort(by="maximum_quantity")
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("aaa", 9, 10),
        ]
    )
    assert ilr_fixture.sort(by="maximum_quantity", reverse=True) == ItemListRequest(
        [
            ItemRequest("orange", 9, 10),
            ItemRequest("aaa", 9, 10),
            ItemRequest("banana", 7, 8),
            ItemRequest("apple", 5, 6),
        ]
    )


def test_sort_item_by_min(ilr_fixture):
    """Test of the sort function by mininimum quantity of the ItemListRequest class"""

    ilr_fixture.add_item(ItemRequest("aaa", 9, 10))
    ilr = ilr_fixture.sort(by="minimum_quantity")
    assert ilr == ItemListRequest(
        [
            ItemRequest("apple", 5, 6),
            ItemRequest("banana", 7, 8),
            ItemRequest("orange", 9, 10),
            ItemRequest("aaa", 9, 10),
        ]
    )
    assert ilr_fixture.sort(by="minimum_quantity", reverse=True) == ItemListRequest(
        [
            ItemRequest("orange", 9, 10),
            ItemRequest("aaa", 9, 10),
            ItemRequest("banana", 7, 8),
            ItemRequest("apple", 5, 6),
        ]
    )


def test_error_to_json_ilr():
    """Test of the error raised when the item to find is not in the list"""

    with pytest.raises(Exception):
        ItemListRequest.to_json(path="ddddddddd")
