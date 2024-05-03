"""Descrition:

This file contains the test cases for the ItemRequest dataclass"""

import os
import sys
import pytest
from BatchMonitor import ItemRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def ir_fixture():
    return ItemRequest("apple", 5, 10)


def test_ItemRequest(ir_fixture):
    """Test of the ItemRequest class"""

    assert ir_fixture == ItemRequest("apple", 5, 10)


def test_invalid_ItemRequest():
    """Test of the ItemRequest class with invalid values"""

    with pytest.raises(ValueError):
        ItemRequest("arme 1", -5, 5)

    with pytest.raises(ValueError):
        ItemRequest("arme 1", 5, -5)

    with pytest.raises(ValueError):
        ItemRequest("arme 1", 5, 4)


def test_maximum_quantity_inf_transform_none():
    """Test of the init transformation of maximum_quantity from inf to None"""

    item = ItemRequest("arme 1", 5, float("inf"))
    assert item == ItemRequest("arme 1", 5, None)


def test_hash_ItemRequest(ir_fixture):
    """Test of the hash function of ItemRequest"""

    assert hash(ir_fixture) == hash(ItemRequest("apple", 5, 10))


def test_ItemRequest_from_str(ir_fixture):
    """Test of the from_str function of the ItemRequest class"""

    assert ir_fixture == ItemRequest.from_str("5-10 of apple")


def test_getitem(ir_fixture):
    """Test of the __getitem__ method"""

    assert ir_fixture["name"] == "apple"
    assert ir_fixture["minimum_quantity"] == 5
    assert ir_fixture["maximum_quantity"] == 10
    assert ir_fixture[0] == "apple"
    assert ir_fixture[1] == 5
    assert ir_fixture[2] == 10


def test_error_getitem(ir_fixture):
    """Test of the __getitem__ method with invalid key"""

    with pytest.raises(ValueError):
        ir_fixture["invalid_key"]

    with pytest.raises(IndexError):
        ir_fixture[3]


def test_str_itemRequest(ir_fixture):
    """Test of the __str__ method"""

    assert "apple" in str(ir_fixture)
    assert "5" in str(ir_fixture)
    assert "10" in str(ir_fixture)
    assert "Item name" in str(ir_fixture)
    assert "Minimum Quantity requested" in str(ir_fixture)
    assert "Maximum Quantity requested" in str(ir_fixture)


def test_iter_itemRequest(ir_fixture):
    """Test of the __iter__ method"""

    for i, value in enumerate(ir_fixture):
        if i == 0:
            assert value == "apple"
        elif i == 1:
            assert value == 5
        elif i == 2:
            assert value == 10
        else:
            assert False


def test_eq_itemRequest(ir_fixture):
    """Test of the __eq__ method"""

    assert ir_fixture == ItemRequest("apple", 5, 10)
    assert not ir_fixture == ItemRequest("apple", 5, 11)
    not_implemented = ir_fixture.__eq__(5)
    assert not_implemented is NotImplemented


def test_ne_itemRequest(ir_fixture):
    """Test of the __ne__ method"""

    assert not ir_fixture != ItemRequest("apple", 5, 10)
    assert ir_fixture != ItemRequest("apple", 5, 11)
    not_implemented = ir_fixture.__ne__(5)
    assert not_implemented is NotImplemented
