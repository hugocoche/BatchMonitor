"""Description

Test module for the primal optimization functions of the lib_optimization library."""

# flake8: noqa: F811, F401

import os
import sys
import pulp as pulp
import pytest

from BatchMonitor.lib_optimization import (
    _generate_dual_constraints,
    _generate_primal_constraints,
    _generate_variable_dual,
)

from .fixture_optimization import (
    Batch_list_fixture,
    ItemListRequest_fixture,
    waited_list_dual,
    waited_list_primal,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_maximum_expense(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _maximum_expense function"""

    variables = waited_list_primal()["variables"]
    waited = waited_list_primal()["constraints"]
    waited["_C4"] = (
        10 * variables["batch 1"]
        + 15 * variables["batch 2"]
        + 20 * variables["batch 3"]
        + -0
        <= 1500000
    )

    test = _generate_primal_constraints(
        variables,
        Batch_list_fixture,
        ItemListRequest_fixture,
        maximum_expense=1500000.0,
    )

    assert test == waited


def test_minimum_expense(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _minimum_expense function"""

    variables = waited_list_primal()["variables"]
    waited = waited_list_primal()["constraints"]
    waited["_C4"] = (
        10 * variables["batch 1"]
        + 15 * variables["batch 2"]
        + 20 * variables["batch 3"]
        + -0
        >= 1500000
    )

    test = _generate_primal_constraints(
        variables,
        Batch_list_fixture,
        ItemListRequest_fixture,
        minimum_expense=1500000.0,
    )

    assert test == waited


def test_apply_expense_constraints(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _apply_expense_constraints function"""

    variables = waited_list_primal()["variables"]
    waited = waited_list_primal()["constraints"]
    waited["_C4"] = (
        10 * variables["batch 1"]
        + 15 * variables["batch 2"]
        + 20 * variables["batch 3"]
        + -0
        >= 1500000
    )
    waited["_C5"] = (
        10 * variables["batch 1"]
        + 15 * variables["batch 2"]
        + 20 * variables["batch 3"]
        + -0
        <= 2000000
    )

    test = _generate_primal_constraints(
        variables,
        Batch_list_fixture,
        ItemListRequest_fixture,
        maximum_expense=2000000.0,
        minimum_expense=1500000.0,
    )

    assert test == waited


def test_error_apply_expense_constraints(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _apply_expense_constraints function with error"""

    with pytest.raises(ValueError):
        _generate_primal_constraints(
            waited_list_primal()["variables"],
            Batch_list_fixture,
            ItemListRequest_fixture,
            maximum_expense=1500000.0,
            minimum_expense=2000000.0,
        )


def test_maximum_benefit(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _maximum_benefit function"""

    variables = _generate_variable_dual(ItemListRequest_fixture)
    constraints = _generate_dual_constraints(
        variables, Batch_list_fixture, ItemListRequest_fixture, maximum_benefit=1000000
    )

    waited = waited_list_dual()["constraints"]
    waited["_C4"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -1000000
        <= 0
    )

    assert constraints == waited


def test_minimum_benefit(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _minimum_benefit function"""

    variables = _generate_variable_dual(ItemListRequest_fixture)
    constraints = _generate_dual_constraints(
        variables, Batch_list_fixture, ItemListRequest_fixture, minimum_benefit=1000000
    )

    waited = waited_list_dual()["constraints"]
    waited["_C4"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -1000000
        >= 0
    )

    assert constraints == waited


def test_apply_benefit_constraints(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _apply_benefit_constraints function"""

    variables = waited_list_dual()["variables"]
    constraints = _generate_dual_constraints(
        variables,
        Batch_list_fixture,
        ItemListRequest_fixture,
        minimum_benefit=1000000,
        maximum_benefit=2000000,
    )

    waited = waited_list_dual()["constraints"]
    waited["_C4"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -1000000
        >= 0
    )
    waited["_C5"] = (
        10 * variables["apple"]
        + 10 * variables["banana"]
        + 10 * variables["orange"]
        + -2000000
        <= 0
    )

    assert constraints == waited


def test_error_apply_benefit_constraints(Batch_list_fixture, ItemListRequest_fixture):
    """Test of the _apply_benefit_constraints function with error"""

    with pytest.raises(ValueError):
        _generate_dual_constraints(
            waited_list_dual()["variables"],
            Batch_list_fixture,
            ItemListRequest_fixture,
            minimum_benefit=2000000,
            maximum_benefit=1000000,
        )
