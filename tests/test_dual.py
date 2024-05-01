"""Description

Test module for the primal optimization functions of the lib_optimization library."""

# flake8: noqa: F811, F401

import os
import sys
import numpy as np
import pulp as pulp
import pytest


from BatchMonitor import (
    ItemListRequest,
    ItemRequest,
    maxEarnings,
)

from BatchMonitor.lib_optimization import (
    _collecte_data_dual,
    _generate_dual_constraints,
    _generate_dual_objective_function,
    _generate_variable_dual,
)

from .fixture_optimization import (
    Batch_Collection_fixture,
    Batch_lists_fixture,
    ItemListRequest_fixture,
    waited_list_dual,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_generate_variable_dual(ItemListRequest_fixture):
    """Test of the _generate_variable_dual function"""

    variables = _generate_variable_dual(ItemListRequest_fixture)
    waited = waited_list_dual()

    assert variables == waited["variables"]


def test_generate_dual_objective_function(ItemListRequest_fixture):
    """Test of the _generate_dual_objective_function function"""

    variables = _generate_variable_dual(ItemListRequest_fixture)
    objective = _generate_dual_objective_function(variables, ItemListRequest_fixture)
    waited = waited_list_dual()

    assert objective == waited["objective"]


def test_generate_dual_constraints(
    Batch_Collection_fixture, ItemListRequest_fixture
):  # noqa: F811
    """Test of the _generate_dual_constraints function"""

    variables = _generate_variable_dual(ItemListRequest_fixture)
    constraints = _generate_dual_constraints(
        variables, Batch_Collection_fixture, ItemListRequest_fixture
    )
    waited = waited_list_dual()

    assert constraints == waited["constraints"]


def test_collecte_data_dual(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the _collecte_data_dual function"""

    variables, objective, constraints = _collecte_data_dual(
        Batch_Collection_fixture,
        ItemListRequest_fixture,
        minimum_benefit=1000000,
        maximum_benefit=2000000,
    )

    waited = waited_list_dual()
    waited["constraints"]["_C4"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -1000000
        >= 0
    )
    waited["constraints"]["_C5"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -2000000
        <= 0
    )

    assert variables == waited["variables"]
    assert objective == waited["objective"]
    assert constraints == waited["constraints"]


def test_maxEarnings(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the maxEarnings function"""

    waited = {
        "Status": "Optimal",
        "Total benefit": 30.0,
        "Item prices": {
            "apple": 1.0,
            "banana": 0.5,
            "orange": 1.5,
        },
    }

    result = maxEarnings(
        batches=Batch_Collection_fixture, demand_list=ItemListRequest_fixture
    )

    assert result["Status"] == waited["Status"]
    assert result["Total benefit"] == waited["Total benefit"]


def test_discrete_maxEarnings(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the maxEarnings function with discrete values"""

    waited = {
        "Status": "Optimal",
        "Total benefit": 30.0,
        "Item prices": {
            "apple": 2.0,
            "banana": 0.0,
            "orange": 1.0,
        },
    }

    result = maxEarnings(
        batches=Batch_Collection_fixture,
        demand_list=ItemListRequest_fixture,
        category_of_variables="Integer",
    )

    assert result["Status"] == waited["Status"]
    assert result["Total benefit"] == waited["Total benefit"]


def test_ultimate_maxEarnings(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the maxEarnings function with all the parameters"""

    waited = {
        "Status": "Optimal",
        "Total benefit": 20.0,
        "Item prices": {
            "apple": 1.0,
            "banana": 0.0,
            "orange": 1.0,
        },
    }

    result = maxEarnings(
        batches=Batch_Collection_fixture,
        demand_list=ItemListRequest_fixture,
        minimum_benefit=10,
        maximum_benefit=20,
        price_constraints={
            "apple": (0.5, 5),
            "banana": (0, 10),
            "orange": (1, 6),
        },
        category_of_variables="Integer",
        exchange_rate=1.2,
        transport_fee=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
        tax_rate=0.1,
        customs_duty=0.2,
    )

    assert result["Status"] == waited["Status"]
    assert result["Total benefit"] == waited["Total benefit"]


def test_infeasible_maxEarnings(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the maxEarnings function with infeasible values"""

    waited = {"Status": "Infeasible"}
    result = maxEarnings(
        batches=Batch_Collection_fixture,
        demand_list=ItemListRequest_fixture,
        maximum_benefit=1,
        price_constraints={
            "apple": (10, None),
            "banana": (5, 10),
            "orange": (14, 15),
        },
    )

    assert result["Status"] == waited["Status"]


def test_error_maxEarnings(Batch_Collection_fixture, ItemListRequest_fixture):
    """Test of the error of the maxEarnings function"""

    with pytest.raises(ValueError):
        maxEarnings(
            batches=Batch_Collection_fixture,
            demand_list=ItemListRequest_fixture,
            maximum_benefit=1,
            minimum_benefit=2,
            price_constraints={
                "fusils": (10000, None),
                "grenades": (5000, None),
                "chars": (0, None),
                "mitrailleuses": (0, None),
                "bombes": (0, None),
            },
            category_of_variables="Integer",
        )

    with pytest.raises(ValueError):
        maxEarnings(
            batches=Batch_Collection_fixture,
            demand_list=ItemListRequest(items=[ItemRequest("abcd", 100000)]),
        )


def test_maxEarnings_bl(Batch_lists_fixture, ItemListRequest_fixture):
    """Test of the maxEarnings function on a BatchLists object"""

    waited = {
        "Status": "Optimal",
        "Total benefit": 30.0,
        "Item prices": {
            "apple": 1.0,
            "banana": 0.5,
            "orange": 1.5,
        },
    }

    result = maxEarnings(
        batches=Batch_lists_fixture, demand_list=ItemListRequest_fixture
    )

    assert result["Status"] == waited["Status"]
    assert result["Total benefit"] == waited["Total benefit"]
