"""Description

Test module for the primal optimization functions of the lib_optimization library."""

# flake8: noqa: F811, F401

import os
import sys
import numpy as np
import pulp as pulp
import pytest

from BatchMonitor import (
    Batch,
    BatchCollection,
)
from BatchMonitor import (
    BatchLists,
    ItemListRequest,
    ItemRequest,
    minBatchExpense,
)
from BatchMonitor.lib_optimization import (
    _generate_variables_primal,
    _generate_primal_objective_function,
    _generate_primal_constraints,
    _collecte_data_primal,
    _expense_per_each_seller,
    _transform_batch_list,
)

from .fixture_optimization import (
    Batch_Collection_fixture,
    Batch_lists_fixture,
    ItemListRequest_fixture,
    waited_list_primal,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_generate_variables_primal(Batch_Collection_fixture):
    """Test of the _generate_variables_primal function"""

    variables = _generate_variables_primal(Batch_Collection_fixture)
    waited = waited_list_primal()
    assert variables == waited["variables"]


def test_generate_primal_objective_function(Batch_Collection_fixture):
    """Test of the _generate_primal_objective_function function"""

    variables = _generate_variables_primal(Batch_Collection_fixture)
    objective = _generate_primal_objective_function(variables, Batch_Collection_fixture)
    waited = waited_list_primal()

    assert objective == waited["objective"]


def test_generate_primal_constraints(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the _generate_primal_constraints function"""

    variables = _generate_variables_primal(Batch_Collection_fixture)
    constraints = _generate_primal_constraints(
        variables, Batch_Collection_fixture, ItemListRequest_fixture
    )

    assert len(constraints) == 3
    waited = waited_list_primal()

    assert constraints == waited["constraints"]


def test_collecte_data_primal(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the _collecte_data_primal function"""
    variables, objective, constraints = _collecte_data_primal(
        Batch_Collection_fixture, ItemListRequest_fixture
    )

    assert variables == waited_list_primal()["variables"]
    assert objective == waited_list_primal()["objective"]
    assert constraints == waited_list_primal()["constraints"]


def test_expense_per_each_seller():
    """Test of the _expense_per_each_seller function"""

    batch_lists = BatchLists.from_str(
        strings=[
            "seller 1_batch 1: 10; 3xapple, 2xbanana, 4xorange",
            "seller 2_batch 2: 15; 5xapple, 5xbanana, 5xorange",
            "seller 3_batch 3: 20; 6xapple, 7xbanana, 7xorange",
            "seller 1_batch 4: 100; 50xapple, 50xbanana, 50xorange",
        ]
    )
    prices = [batch.price for batches in batch_lists for batch in batches]
    test = {
        "seller1_batch 1": 0.0,
        "seller1_batch 4": 100.0,
        "seller2_batch 2": 200.0,
        "seller3_batch 3": 300.0,
    }
    waited = {
        "seller1": 0 * prices[0] + 100 * prices[1],
        "seller2": 200 * prices[2],
        "seller3": 300 * prices[3],
    }

    result = _expense_per_each_seller(_transform_batch_list(batch_lists), test)

    assert result == waited


def test_minBatchExpense(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the minBatchExpense function"""

    waited = {"Status": "Optimal", "Total cost": 30.0}
    result = minBatchExpense(Batch_Collection_fixture, ItemListRequest_fixture)

    assert result["Status"] == waited["Status"]
    assert result["Total cost"] == waited["Total cost"]


def test_discrete_minBatchExpense(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the minBatchExpense function with discrete variables"""

    waited = {"Status": "Optimal", "Total cost": 30.0}
    result = minBatchExpense(
        Batch_Collection_fixture,
        ItemListRequest_fixture,
        category_of_variables="Integer",
    )

    assert result["Status"] == waited["Status"]
    assert result["Total cost"] == waited["Total cost"]


def test_minBatchExpense_2(Batch_lists_fixture, ItemListRequest_fixture):
    """Test of the minBatchExpense function on BatchLists object"""

    waited = {
        "Status": "Optimal",
        "Total cost": 30.0,
        "batches_name": {
            "seller 1_batch 1": 0.0,
            "seller 1_batch 2": 2.0,
            "seller 2_batch 3": 0.0,
        },
    }
    result = minBatchExpense(Batch_lists_fixture, ItemListRequest_fixture)

    assert result["Status"] == waited["Status"]
    assert result["Total cost"] == waited["Total cost"]
    assert result["Batch quantities"].keys() == waited["batches_name"].keys()


def test_ultimate_minBatchExpense():
    """Test of the minBatchExpense function with all parameters"""

    waited = {
        "Status": "Optimal",
        "Total cost": 23.5224,
        "Batch quantities": {"batch1": 0.0, "batch2": 1.2},
    }

    batches = BatchCollection(
        seller="type",
        batch_list=[
            Batch.from_str("batch1:10; 3xapple, 2xbanana"),
            Batch.from_str("batch2:15; 5xapple, 5xbanana"),
        ],
    )

    items = ItemListRequest([ItemRequest("apple", 3, 6), ItemRequest("banana", 6, 9)])
    result = minBatchExpense(
        batches,
        items,
        category_of_variables="Continuous",
        exchange_rate=0.9,
        transport_fee=np.array([0.3, 0.1, 0.4]),
        tax_rate=np.array([0.2, 0.1, 0.3]),
        customs_duty=0.2,
        batch_constraints=dict(batch1=(0, 50), batch2=(0, 1000), batch3=(0, 100)),
        minimum_expense=20,
        maximum_expense=100,
    )

    assert result["Status"] == waited["Status"]
    assert result["Total cost"] == waited["Total cost"]


def test_infeasible_minBatchExpense(Batch_Collection_fixture):
    """Test of the minBatchExpense function with infeasible values"""

    waited = {"Status": "Infeasible"}
    result = minBatchExpense(
        Batch_Collection_fixture,
        ItemListRequest(
            [ItemRequest("apple", 1000000), ItemRequest("banana", 2000000)]
        ),
        maximum_expense=1000,
    )

    assert result == waited


def test_error_minBatchExpense(Batch_Collection_fixture):
    """Test of the error of the minBatchExpense function"""

    with pytest.raises(ValueError):
        minBatchExpense(
            Batch_Collection_fixture,
            ItemListRequest(
                [ItemRequest("apple", 1000000), ItemRequest("banana", 2000000)]
            ),
            minimum_expense=1000,
            maximum_expense=500,
        )

    with pytest.raises(ValueError):
        minBatchExpense(
            Batch_Collection_fixture,
            ItemListRequest(
                [ItemRequest("date", 1000000), ItemRequest("banana", 2000000)]
            ),
            minimum_expense=1000,
            maximum_expense=10000,
        )


def test_minBatchExpenseBatchlists(ItemListRequest_fixture):
    lists_of_batches = BatchLists(
        batchlists=[
            BatchCollection(
                seller="MALANDRIN",
                batch_list=[
                    Batch.from_str("batch1:10; 3xapple, 2xbanana, 4xorange"),
                    Batch.from_str("batch2:15; 5xapple, 5xbanana, 5xorange"),
                ],
            ),
            BatchCollection(
                seller="DETAILIN",
                batch_list=[Batch.from_str("batch3:20; 6xapple, 7xbanana, 7xorange")],
            ),
        ]
    )

    waited = {
        "Status": "Optimal",
        "Total cost": 30.0,
        "Batch quantities": {
            "MALANDRIN_batch1": 0.0,
            "MALANDRIN_batch2": 2.0,
            "DETAILIN_batch3": 0.0,
        },
        "Expense per seller": {
            "MALANDRIN": 30.0,
            "DETAILIN": 0.0,
        },
    }

    assert minBatchExpense(lists_of_batches, ItemListRequest_fixture) == waited
