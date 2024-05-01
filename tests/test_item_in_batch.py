"""Description:

Tests for the Item_In_Batch dataclass.
"""

import os
import sys
import pytest

from BatchMonitor import Item_in_batch

from BatchMonitor.lib_batches import Incompatible_negative_value

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def ib_fixture():
    return Item_in_batch("apple", 5.0)


def test_Item_in_batch(ib_fixture):
    """Test of the Item_in_batch class"""

    assert ib_fixture.name == "apple"
    assert ib_fixture.quantity_in_batch == 5.0
    assert ib_fixture == Item_in_batch("apple", 5.0)
    assert isinstance(ib_fixture, Item_in_batch)


def test_Item_in_batch_invalid_quantity():
    """Test of the Item_in_batch class with invalid values"""

    with pytest.raises(Incompatible_negative_value):
        Item_in_batch("apple", -5.0)


def test_Item_in_batch_from_str(ib_fixture):
    """Test of the from_str function of the Item_in_batch class"""

    assert ib_fixture == Item_in_batch.from_str("5xapple")


def test_hash_Item_in_batch(ib_fixture):
    """Test of the hash function of Item_in_batch"""

    assert hash(ib_fixture) == hash(Item_in_batch("apple", 5.0))


def test_eq_Item_in_batch(ib_fixture):
    """Test of the eq function of Item_in_batch"""

    assert ib_fixture == Item_in_batch("apple", 5.0)
    assert not ib_fixture == Item_in_batch("apple", 6.0)
    assert not ib_fixture == Item_in_batch("orange", 5.0)
    not_implemented = ib_fixture.__eq__("apple")
    assert not_implemented is NotImplemented


def test_ne_Item_in_batch(ib_fixture):
    """Test of the ne function of Item_in_batch"""

    assert not ib_fixture != Item_in_batch("apple", 5.0)
    assert ib_fixture != Item_in_batch("apple", 6.0)
    assert ib_fixture != Item_in_batch("orange", 5.0)
    not_implemented = ib_fixture.__ne__("apple")
    assert not_implemented is NotImplemented


def test_get_item_in_batch(ib_fixture):
    """Test of the __get_item__ function of Item_in_batch"""

    assert ib_fixture["name"] == "apple" == ib_fixture.name == ib_fixture[0]
    assert (
        ib_fixture["quantity_in_batch"]
        == 5.0
        == ib_fixture.quantity_in_batch
        == ib_fixture[1]
    )


def test_invalid_get_item_in_batch(ib_fixture):
    """Test of the __get_item__ function of Item_in_batch with invalid values"""

    with pytest.raises(KeyError):
        ib_fixture["invalid_key"]
    with pytest.raises(IndexError):
        ib_fixture[2]


def test_iter_item_in_batch(ib_fixture):
    """Test of the __iter__ function of Item_in_batch"""

    assert list(ib_fixture) == ["apple", 5.0]
    for index, value in enumerate(ib_fixture):
        assert value == ib_fixture[index]


def test_str_item_in_batch(ib_fixture):
    """Test of the __str__ function of Item_in_batch"""

    output = str(ib_fixture)
    assert "apple" in output
    assert "5.0" in output
    assert "Item name" in output
    assert "Quantity in batch" in output
