"""Description.

Tests for the lib_format module."""

import os
import sys
import pytest

from BatchMonitor import (
    format_batch_collection,
    format_batch_lists,
    format_itemlistRequest,
    format_maxEarnings,
    format_minBatchExpense,
    ItemListRequest,
    minBatchExpense,
    maxEarnings,
    ItemRequest,
)

# flake8: noqa: F401
from tests import (
    batch_fixture,
    batch_collection_fixture,
    batchlists_fixture,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def format_bc_fixture(batch_collection_fixture):  # noqa
    return format_batch_collection(batch_collection_fixture)


@pytest.fixture
def format_bl_fixture(batchlists_fixture):  # noqa
    return format_batch_lists(batchlists_fixture)


@pytest.fixture
def format_ilr_fixture(ilr_fixture):
    return format_itemlistRequest(ilr_fixture)


@pytest.fixture
def format_mbe_bc_fixture(batch_collection_fixture, ilr_fixture):  # noqa
    mbe = minBatchExpense(
        batch_collection_fixture, ilr_fixture, category_of_variables="Integer"
    )
    return format_minBatchExpense(mbe)


@pytest.fixture
def format_me_bc_fixture(batch_collection_fixture, ilr_fixture):  # noqa
    me = maxEarnings(
        batch_collection_fixture, ilr_fixture, category_of_variables="Integer"
    )
    return format_maxEarnings(me)


@pytest.fixture
def format_mbe_bl_fixture(batchlists_fixture, ilr_fixture):  # noqa
    mbe = minBatchExpense(batchlists_fixture, ilr_fixture)
    return format_minBatchExpense(mbe)


@pytest.fixture
def format_me_bl_fixture(batchlists_fixture, ilr_fixture):  # noqa
    me = maxEarnings(batchlists_fixture, ilr_fixture)
    return format_maxEarnings(me)


@pytest.fixture
def ilr_fixture():
    return ItemListRequest([ItemRequest("apple", 1, 6)])


def test_format_bc(format_bc_fixture):
    """Test the format_batch_collection function."""

    assert "The batches sold by Default seller\n" == str(format_bc_fixture.title)

    for column, header, text in zip(
        format_bc_fixture.columns,
        ("Batch", "Price", "Items"),
        ("batch 1", "1.0", "2 apple\n3 banana\n4 kiwi"),
    ):
        assert column.header == header
        assert text in (str(cell) for cell in column._cells)


def test_format_bl(format_bl_fixture):
    """Test the format_batch_lists function."""

    assert "The batches sold by each seller\n" == str(format_bl_fixture.title)

    for column, header, text in zip(
        format_bl_fixture.columns,
        ("Seller", "Batch", "Price", "Items"),
        ("seller1", "batch 1", "1.0", "2 apple\n3 banana\n\n"),
    ):
        assert column.header == header
        assert text in (str(cell) for cell in column._cells)


def test_format_ilr(format_ilr_fixture):
    """Test the format_itemlistRequest function."""

    assert "The items requested by the customer\n" == str(format_ilr_fixture.title)
    for column, header, text in zip(
        format_ilr_fixture.columns,
        ("Item", "Minimum Quantity", "Maximum Quantity"),
        ("apple", "1", "6"),
    ):
        assert column.header == header
        assert text in (str(cell) for cell in column._cells)


def test_format_mbe_bc(format_mbe_bc_fixture):
    """Test the format_maxEarnings function with a BatchCollection object."""

    assert "Results of the batch expenditure minimization problem" == str(
        format_mbe_bc_fixture.title
    )
    for column in format_mbe_bc_fixture.columns:
        for cell in column._cells:
            if "\n" in cell:
                for line in cell.split("\n"):
                    assert line in (
                        "Status",
                        "Total cost",
                        "Batch quantities",
                        "Expense per seller",
                        "Optimal",
                        "1.0",
                        "[red]batch 1 :[/red] 1.0",
                        "[red]batch 2 :[/red] 0.0",
                        "[red]batch 3 :[/red] 0.0",
                    )
            else:
                assert cell in (
                    "Status",
                    "Total cost",
                    "Batch quantities",
                    "Expense per seller",
                    "Optimal",
                    "1.0",
                    "[red]batch 1 :[/red] 1.0",
                    "[red]batch 2 :[/red] 0.0",
                    "[red]batch 3 :[/red] 0.0",
                )


def test_format_me_bc(format_me_bc_fixture):
    """Test the format_maxEarnings function with a BatchCollection object."""

    assert "Results of the earnings maximization problem" == str(
        format_me_bc_fixture.title
    )
    for column in format_me_bc_fixture.columns:
        for cell in column._cells:
            if "\n" in cell:
                for line in cell.split("\n"):
                    assert line in (
                        "Status",
                        "Total benefit",
                        "Item prices",
                        "Optimal",
                        "0.0",
                        "[red]apple :[/red] 0.0",
                        "[red]cherries :[/red] 0.0",
                        "[red]pineapple :[/red] 0.0",
                        "[red]kiwi :[/red] 0.0",
                        "[red]banana :[/red] 0.0",
                    )
            else:
                assert cell in (
                    "Status",
                    "Total benefit",
                    "Item prices",
                    "Optimal",
                    "0.0",
                    "[red]apple :[/red] 0.0",
                    "[red]cherries :[/red] 0.0",
                    "[red]pineapple :[/red] 0.0",
                    "[red]kiwi :[/red] 0.0",
                    "[red]banana :[/red] 0.0",
                )


def test_format_mbe_bl(format_mbe_bl_fixture):
    """Test the format_maxEarnings function with a BatchLists object."""

    assert "Results of the batch expenditure minimization problem" == str(
        format_mbe_bl_fixture.title
    )
    for column in format_mbe_bl_fixture.columns:
        for cell in column._cells:
            if "\n" in cell:
                for line in cell.split("\n"):
                    assert line in (
                        "Status",
                        "Total cost",
                        "Batch quantities",
                        "Expense per seller",
                        "Optimal",
                        "0.5",
                        "[red]seller1_batch 1 :[/red] 0.5",
                        "[red]seller1_batch 2 :[/red] 0.0",
                        "[red]seller2_batch 3 :[/red] 0.0",
                        "[red]seller2_batch 4 :[/red] 0.0",
                        "[red]seller1 :[/red] 0.5",
                        "[red]seller2 :[/red] 0.0",
                    )
            else:
                assert cell in (
                    "Status",
                    "Total cost",
                    "Batch quantities",
                    "Expense per seller",
                    "Optimal",
                    "0.5",
                    "[red]seller1_batch 1 :[/red] 0.5",
                    "[red]seller1_batch 2 :[/red] 0.0",
                    "[red]seller2_batch 3 :[/red] 0.0",
                    "[red]seller2_batch 4 :[/red] 0.0",
                    "[red]seller1 :[/red] 0.5",
                    "[red]seller2 :[/red] 0.0",
                )


def test_format_me_bl(format_me_bl_fixture):
    """Test the format_maxEarnings function with a BatchLists object."""

    assert "Results of the earnings maximization problem" == str(
        format_me_bl_fixture.title
    )
    for column in format_me_bl_fixture.columns:
        for cell in column._cells:
            if "\n" in cell:
                for line in cell.split("\n"):
                    assert line in (
                        "Status",
                        "Total benefit",
                        "Item prices",
                        "Optimal",
                        "0.5",
                        "[red]apple :[/red] 0.5",
                        "[red]pineapple :[/red] 0.0",
                        "[red]orange :[/red] 0.0",
                        "[red]strawberry :[/red] 0.0",
                        "[red]cherries :[/red] 0.0",
                        "[red]banana :[/red] 0.0",
                    )
            else:
                assert cell in (
                    "Status",
                    "Total benefit",
                    "Item prices",
                    "Optimal",
                    "0.5",
                    "[red]apple :[/red] 0.5",
                    "[red]pineapple :[/red] 0.0",
                    "[red]orange :[/red] 0.0",
                    "[red]strawberry :[/red] 0.0",
                    "[red]cherries :[/red] 0.0",
                    "[red]banana :[/red] 0.0",
                )


def test_format_infeasible_problem(batch_collection_fixture, ilr_fixture):  # noqa: F811
    """Test the format functions when the problem is infeasible."""

    mbe = minBatchExpense(
        batch_collection_fixture, ilr_fixture, minimum_expense=0, maximum_expense=0.0001
    )
    assert "The problem is infeasible." == format_minBatchExpense(mbe)

    me = maxEarnings(
        batch_collection_fixture,
        ilr_fixture,
        minimum_benefit=1000000000000000,
        maximum_benefit=1000000000000001,
    )
    assert "The problem is infeasible." == format_maxEarnings(me)
