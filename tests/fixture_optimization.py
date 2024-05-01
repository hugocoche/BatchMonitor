"""Description:

This file contains the optimization fixtures for the tests."""

import os
import sys
import pulp as pulp
import pytest

from BatchMonitor.lib_batches import (
    Batch,
    BatchCollection,
    BatchLists,
)

from BatchMonitor.lib_item_request import (
    ItemListRequest,
    ItemRequest,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def Batch_list_fixture():
    return [
        Batch.from_str("batch 1: 10; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2: 15; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3: 20; 6xapple, 7xbanana, 7xorange"),
    ]


@pytest.fixture
def Batch_Collection_fixture():
    return BatchCollection(
        [
            Batch.from_str("batch 1: 10; 3xapple, 2xbanana, 4xorange"),
            Batch.from_str("batch 2: 15; 5xapple, 5xbanana, 5xorange"),
            Batch.from_str("batch 3: 20; 6xapple, 7xbanana, 7xorange"),
        ],
        seller="seller1",
    )


@pytest.fixture
def ItemListRequest_fixture():
    return ItemListRequest(
        [
            ItemRequest("apple", 10),
            ItemRequest("banana", 10),
            ItemRequest("orange", 10),
        ]
    )


@pytest.fixture
def Batch_lists_fixture():
    return BatchLists.from_str(
        strings=[
            "seller 1_batch 1: 10; 3xapple, 2xbanana, 4xorange",
            "seller 1_batch 2: 15; 5xapple, 5xbanana, 5xorange",
            "seller 2_batch 3: 20; 6xapple, 7xbanana, 7xorange",
        ]
    )


def waited_list_primal(cat="Continuous"):
    """a function to get result of pulp"""

    variables = {
        "batch 1": pulp.LpVariable("batch 1", lowBound=0, cat=cat),
        "batch 2": pulp.LpVariable("batch 2", lowBound=0, cat=cat),
        "batch 3": pulp.LpVariable("batch 3", lowBound=0, cat=cat),
    }
    prob = (
        10 * pulp.lpSum([variables["batch 1"]])
        + 15 * pulp.lpSum([variables["batch 2"]])
        + 20 * pulp.lpSum([variables["batch 3"]])
    )
    constraints = dict(
        [
            (
                "_C1",
                3 * variables["batch 1"]
                + 5 * variables["batch 2"]
                + 6 * variables["batch 3"]
                + -10
                >= 0,
            ),
            (
                "_C2",
                2 * variables["batch 1"]
                + 5 * variables["batch 2"]
                + 7 * variables["batch 3"]
                + -10
                >= 0,
            ),
            (
                "_C3",
                4 * variables["batch 1"]
                + 5 * variables["batch 2"]
                + 7 * variables["batch 3"]
                + -10
                >= 0,
            ),
        ]
    )

    return {"variables": variables, "objective": prob, "constraints": constraints}


def waited_list_dual(cat="Continuous"):
    """a function to get result of pulp"""

    variables = {
        "apple": pulp.LpVariable("apple", lowBound=0, cat=cat),
        "banana": pulp.LpVariable("banana", lowBound=0, cat=cat),
        "orange": pulp.LpVariable("orange", lowBound=0, cat=cat),
    }
    prob = (
        10 * pulp.lpSum([variables["apple"]])
        + 10 * pulp.lpSum([variables["banana"]])
        + 10 * pulp.lpSum([variables["orange"]])
    )
    constraints = dict(
        [
            (
                "_C1",
                3 * variables["apple"]
                + 2 * variables["banana"]
                + 4 * variables["orange"]
                + -10
                <= 0,
            ),
            (
                "_C2",
                5 * variables["apple"]
                + 5 * variables["banana"]
                + 5 * variables["orange"]
                + -10
                <= 0,
            ),
            (
                "_C3",
                6 * variables["apple"]
                + 7 * variables["banana"]
                + 7 * variables["orange"]
                + -10
                <= 0,
            ),
        ]
    )

    return {"variables": variables, "objective": prob, "constraints": constraints}
