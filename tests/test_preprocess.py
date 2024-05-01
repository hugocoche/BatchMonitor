"""Description

Test module for the preprocessing functions of the lib_optimization library."""

# flake8: noqa: F811, F401

import os
import sys
import pulp as pulp
import pytest

from BatchMonitor import (
    Batch,
    BatchCollection,
)

from BatchMonitor import (
    ItemListRequest,
    ItemRequest,
)

from BatchMonitor.lib_optimization import (
    _addition_of_unrequested_item,
    _missing_ItemRequest,
    _prepare_the_problem,
    _transform_batch_list,
)

from .fixture_optimization import (
    Batch_Collection_fixture,
    Batch_list_fixture,
    Batch_lists_fixture,
    ItemListRequest_fixture,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_transform_batch_list(Batch_lists_fixture):
    """Test of the function _transform_batch_list"""

    test = _transform_batch_list(Batch_lists_fixture)
    waited = BatchCollection(
        [
            Batch.from_str("seller 1_batch 1: 10; 3xapple, 2xbanana, 4xorange"),
            Batch.from_str("seller 1_batch 2: 15; 5xapple, 5xbanana, 5xorange"),
            Batch.from_str("seller 2_batch 3: 20; 6xapple, 7xbanana, 7xorange"),
        ]
    )

    assert test == waited


def test_missing_ItemRequest():
    """Test of the function _missing_ItemRequest"""

    batches = BatchCollection(
        [
            Batch.from_str("batch1: 1; 1xapple, 2xbanana, 5xorange"),
            Batch.from_str("batch2: 2; 3xorange, 4xstrawberry"),
        ]
    )
    request = ItemListRequest([ItemRequest("apple", 3), ItemRequest("banana", 6)])
    assert not _missing_ItemRequest(batches, request)
    list_missing_ItemRequest = ItemListRequest(
        [
            ItemRequest("apple", 3),
            ItemRequest("banana", 6),
            ItemRequest("date", 0),
        ]
    )
    assert _missing_ItemRequest(batches, list_missing_ItemRequest)


def test__addition_of_unrequested_item():
    """Test of the function _addition_of_unrequested_item"""

    batches = BatchCollection(
        [
            Batch.from_str("batch1: 1; 1xapple, 2xbanana, 10xorange"),
            Batch.from_str("batch2: 2; 3xapple, 4xbanana"),
        ]
    )
    items_requested = ItemListRequest(
        [ItemRequest("apple", 3), ItemRequest("banana", 6)]
    )
    waited = ItemListRequest(
        [
            ItemRequest("apple", 3),
            ItemRequest("banana", 6),
            ItemRequest("orange", 0),
        ]
    )
    test = _addition_of_unrequested_item(batches, items_requested)
    assert test == waited


def test_prepare_the_problem(
    Batch_list_fixture, Batch_Collection_fixture, ItemListRequest_fixture
):
    """Test of the _prepare_the_problem function"""

    batches = _prepare_the_problem(Batch_Collection_fixture, ItemListRequest_fixture)

    assert batches == Batch_Collection_fixture


def test_error_prepare_the_problem(Batch_Collection_fixture):
    """Test of the _prepare_the_problem function"""

    with pytest.raises(ValueError):
        _prepare_the_problem(
            Batch_Collection_fixture, ItemListRequest([ItemRequest("date", 3)])
        )
