"""Description

Integration tests for the initialization commands of BatchMonitor application"""

import os
import sys


from unittest.mock import patch, MagicMock, call

import pytest
import numpy as np
from rich.text import Text

from BatchMonitor.__main__ import (
    BatchCollection,
    BatchLists,
    ItemListRequest,
    _create_object_from_json,
    _init_solve,
)

from BatchMonitor.lib_app import (
    _bc_creation,
    _number_creation,
    _bl_creation,
    _init_app,
    MARKDOWN_DESCRIPTION,
    MARKDOWN_TITLE,
    _init_problem,
    _jaune,
    _init_batchtype,
    _init_category_of_batch_quantities,
    _init_batch_constraints,
    _batch_transformation,
    _init_category_of_item_prices,
    _init_item_prices_constraints,
    _init_maxEarnings,
    _init_minBatchExpense,
    _init_objective_function_constraints,
    _init_objective_function_constraints_prompt,
    _init_rates,
    _item_request_creation,
    _transform_string_category,
    _verify_rates,
    _verify_valid_ilr,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def bc_fixture():
    bc = BatchCollection.from_str(
        "batch 1: 1; 2xapple, 5xbanana, 6xorange",
        "batch 2: 2; 3xapple, 4xbanana, 5xorange",
        "batch 3: 3; 4xapple, 3xbanana, 4xorange",
        seller="seller 1",
    )
    return bc


@pytest.fixture
def bl_fixture():
    bl = BatchLists.from_str(
        strings=[
            "seller 1_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 1_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 2_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 2_batch 3: 3; 4xapple, 3xbanana, 4xorange",
            "seller 2_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 3_batch 3: 3; 4xapple, 3xbanana, 4xorange",
            "seller 3_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 3_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 3_batch 4: 3; 4xapple, 3xbanana, 4xorange",
        ]
    )
    return bl


@pytest.fixture
def ilr_fixture():
    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of orange",
    )
    return ilr


@pytest.fixture
def bad_ilr_fixture():
    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of zzzzzzz",
    )
    return ilr


def batch_collection_json():
    bc = BatchCollection.from_str(
        "batch 1: 1; 2xapple, 5xbanana, 6xorange",
        "batch 2: 2; 3xapple, 4xbanana, 5xorange",
        "batch 3: 3; 4xapple, 3xbanana, 4xorange",
        seller="seller 1",
    )
    bc.to_json("demo_batchcollection.json")


def batchlists_json():
    bl = BatchLists.from_str(
        strings=[
            "seller 1_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 1_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 2_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 2_batch 3: 3; 4xapple, 3xbanana, 4xorange",
            "seller 2_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 3_batch 3: 3; 4xapple, 3xbanana, 4xorange",
            "seller 3_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 3_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 3_batch 4: 3; 4xapple, 3xbanana, 4xorange",
        ]
    )
    bl.to_json("demo_batchlists.json")


def ilr_json():
    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of orange",
    )
    ilr.to_json("demo_itemlistrequest.json")


def bad_ilr_json():
    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of zzzzzzz",
    )
    ilr.to_json("bad_demo_itemlistrequest.json")


def prompt_test_style(mock_input, text):
    final_text = Text(text + ": ")
    final_text.stylize("cyan", 0, len(text))
    return mock_input.assert_called_once_with(final_text, password=False, stream=None)


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    batch_collection_json()
    batchlists_json()
    ilr_json()
    bad_ilr_json()


def test_init_app():
    """Test of the _init_app function of the BatchMonitor application"""

    with patch("BatchMonitor.lib_app.console.print") as mock_print:
        _init_app()
        assert mock_print.call_count == 3
        assert mock_print.call_args_list[0][0][0].markup == MARKDOWN_TITLE
        assert mock_print.call_args_list[1][0][0] == 5 * ":rocket:"
        assert mock_print.call_args_list[2][0][0].markup == MARKDOWN_DESCRIPTION


def test_init_problem():
    """Test of the _init_problem function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["ddd", "minBatchExpense"],
    ) as mock_prompt:
        problem = _init_problem()
        assert problem == "minBatchExpense"
        mock_prompt.assert_called_with(
            f"Which problem do you want to resolve ? [{_jaune}](minBatchExpense/maxEarnings/both)"
        )
        mock_prompt.call_count == 2


def test_init_batchtype_one():
    """Test of the _init_batchtype function of the BatchMonitor application for one seller"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt", return_value="one"
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._bc_creation",
        return_value=(5, ["batch1", "batch2"]),
    ) as mock_bc_creation:
        number_of_batches, batch_list = _init_batchtype()
        assert number_of_batches == 5
        assert batch_list == ["batch1", "batch2"]
        mock_prompt.assert_called_once_with(
            f"Do you have one seller or multiple sellers ? [{_jaune}](one/multiple)"
        )
        mock_bc_creation.assert_called_once()


def test_init_batchtype_multiple():
    """Test of the _init_batchtype function of the BatchMonitor application for multiple sellers"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt", side_effect=["22", "multiple"]
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._bl_creation",
        return_value=(3, ["batchA", "batchB"]),
    ) as mock_bl_creation:
        number_of_batches, batch_list = _init_batchtype()
        assert number_of_batches == 3
        assert batch_list == ["batchA", "batchB"]
        mock_prompt.assert_called_with(
            f"Do you have one seller or multiple sellers ? [{_jaune}](one/multiple)"
        )
        mock_prompt.call_count == 2
        mock_bl_creation.assert_called_once()


def test_init_solve():
    """Test of the _init_solve function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.__main__._styled_prompt",
        side_effect=["BatchCollection", "minBatchExpense"],
    ):
        batch_type, problem_type = _init_solve()

    assert batch_type == "BatchCollection"
    assert problem_type == "minBatchExpense"

    with patch(
        "BatchMonitor.__main__._styled_prompt",
        side_effect=["BatchList", "maxEarnings"],
    ):
        batch_type, problem_type = _init_solve()

    assert batch_type == "BatchList"
    assert problem_type == "maxEarnings"


def test_create_object_from_json(bc_fixture, ilr_fixture, bl_fixture):
    """Test of the _create_object_from_json function of the BatchMonitor application"""

    bc, ilr, number_of_bc = _create_object_from_json(
        "BatchCollection", "demo_batchcollection.json", "demo_itemlistrequest.json"
    )
    assert bc == bc_fixture
    assert ilr == ilr_fixture
    assert number_of_bc == 3

    bl, ilr, number_of_bl = _create_object_from_json(
        "BatchLists", "demo_batchlists.json", "demo_itemlistrequest.json"
    )
    assert bl == bl_fixture
    assert ilr == ilr_fixture
    assert number_of_bl == 9


def test_error_create_object_from_json():
    """Test of the errors of the _create_object_from_json function of the BatchMonitor application"""

    with pytest.raises(SystemExit):
        _create_object_from_json(
            "BatchCollection",
            "demo_batchcollection.json",
            "bad_demo_itemlistrequest.json",
        )

    with pytest.raises(SystemExit):
        _create_object_from_json(
            "BatchLists", "demo_batchlists.json", "bad_demo_itemlistrequest.json"
        )

    with pytest.raises(SystemExit):
        _create_object_from_json(
            "BatchCollection", "demo_batchlists.json", "demo_itemlistrequest.json"
        )


def test_number_creation():
    """Test of the _number_creation function of the BatchMonitor application"""

    with patch("rich.console.Console.input", return_value="3") as mock_input:
        number = _number_creation("Batches")
    prompt_test_style(mock_input, "\nHow many Batches do you want to create ?")
    assert number == 3

    with patch("rich.console.Console.input", return_value="555555") as mock_input:
        number = _number_creation("Batches")
    prompt_test_style(mock_input, "\nHow many Batches do you want to create ?")
    assert number == 555555


def test_invalid_number_creation():
    """Test of the _number_creation function of the BatchMonitor application with invalid input"""

    with patch(
        "rich.console.Console.input", side_effect=["badinput", "-3", "3"]
    ), patch("BatchMonitor.lib_app._style_invalid_choice") as mock_style_invalid_choice:
        number = _number_creation("Batches")
    assert mock_style_invalid_choice.call_count == 2
    assert number == 3


def test_bc_creation():
    """Test of the _bc_creation function of the BatchMonitor application"""

    with patch("BatchMonitor.lib_app._style_h2") as mock_style_h2, patch(
        "BatchMonitor.lib_app._number_creation", return_value=3
    ) as mock_number_creation, patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=[
            "seller",
            "Batch1:10; 1xapple, 2xbanana",
            "Batch2:10; 1xapple, 2xbanana",
            "Batch3:10; 1xapple, 2xbanana",
        ],
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._styled_echo"
    ) as mock_styled_echo, patch(
        "BatchMonitor.lib_app.BatchCollection"
    ) as mock_BatchCollection, patch(
        "BatchMonitor.lib_app.Batch.from_str"
    ) as mock_from_str, patch(
        "BatchMonitor.lib_app._animate_progress_bar"
    ) as mock_animate_progress_bar:
        mock_BatchCollection.return_value = MagicMock()
        mock_from_str.return_value = MagicMock()

        number_of_batches, bc = _bc_creation()

        mock_style_h2.assert_called_once_with("BATCHES CREATION : BATCH COLLECTION")
        mock_number_creation.assert_called_once_with(object="batches")
        assert mock_styled_prompt.call_args_list == [
            call("Enter the name of the seller"),
            call("\n[red]⠹ 33.33% : [/red]Enter the Batch n°1"),
            call("\n[red]⠹ 66.67% : [/red]Enter the Batch n°2"),
            call("\n[red]⠹ 100.0% : [/red]Enter the Batch n°3"),
        ]
        assert mock_styled_echo.call_count == 2
        mock_BatchCollection.assert_called_once_with(seller="seller")
        assert mock_from_str.call_count == 3
        mock_animate_progress_bar.assert_called_once_with(
            "Initialization of the problems", 3
        )
        assert number_of_batches == 3
        assert bc == mock_BatchCollection.return_value


def test_bc_creation_bad_input():
    """Test of the _bc_creation function of the BatchMonitor application with bad input"""

    with patch("BatchMonitor.lib_app._style_h2") as mock_style_h2, patch(
        "BatchMonitor.lib_app._number_creation", return_value=1
    ) as mock_number_creation, patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["seller", "BadInput", "Batch1:10; 1xapple, 2xbanana"],
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._styled_echo"
    ) as mock_styled_echo, patch(
        "BatchMonitor.lib_app.BatchCollection"
    ) as mock_BatchCollection, patch(
        "BatchMonitor.lib_app.Batch.from_str",
        side_effect=[ValueError, MagicMock()],
    ) as mock_from_str, patch(
        "BatchMonitor.lib_app._animate_progress_bar"
    ) as mock_animate_progress_bar, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        mock_BatchCollection.return_value = MagicMock()

        number_of_batches, bc = _bc_creation()

        mock_style_h2.assert_called_once_with("BATCHES CREATION : BATCH COLLECTION")
        mock_number_creation.assert_called_once_with(object="batches")
        assert mock_styled_prompt.call_args_list == [
            call("Enter the name of the seller"),
            call("\n[red]⠹ 100.0% : [/red]Enter the Batch n°1"),
            call("\n[red]⠹ 100.0% : [/red]Enter the Batch n°1"),
        ]
        assert mock_styled_echo.call_count == 4
        mock_BatchCollection.assert_called_once_with(seller="seller")
        assert mock_from_str.call_count == 2
        mock_animate_progress_bar.assert_called_once_with(
            "Initialization of the problems", 1
        )
        mock_style_invalid_choice.assert_called_once_with(
            "Invalid format.\nHave you entered two batches with the same name for the same seller?\nIf so, please change the name of one of the batches"
        )
        assert number_of_batches == 1
        assert bc == mock_BatchCollection.return_value


def test_bl_creation():
    """Test of the _bl_creation function of the BatchMonitor application"""

    with patch("BatchMonitor.lib_app._style_h2") as mock_style_h2, patch(
        "BatchMonitor.lib_app._number_creation", return_value=1
    ) as mock_number_creation, patch(
        "BatchMonitor.lib_app._styled_prompt",
        return_value="Seller1_Batch1:10; 1xapple, 2xbanana",
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._styled_echo"
    ) as mock_styled_echo, patch(
        "BatchMonitor.lib_app.BatchLists"
    ) as mock_BatchLists, patch(
        "BatchMonitor.lib_app.BatchCollection.from_str"
    ) as mock_from_str, patch(
        "BatchMonitor.lib_app._animate_progress_bar"
    ) as mock_animate_progress_bar:
        mock_BatchLists.return_value = MagicMock()
        mock_from_str.return_value = MagicMock()

        number_of_batches, bl = _bl_creation()

        mock_style_h2.assert_called_once_with("BATCHES CREATION : BATCH LISTS")
        mock_number_creation.assert_called_once_with(object="batches")
        mock_styled_prompt.assert_called_once_with(
            "\n[red]⠹ 100.0% : [/red]Enter the Batch n°1"
        )
        assert mock_styled_echo.call_count == 2
        mock_BatchLists.assert_called_once()
        mock_from_str.assert_called_once_with(
            "Batch1:10; 1xapple, 2xbanana", seller="Seller1"
        )
        mock_animate_progress_bar.assert_called_once_with(
            "Initialization of the problems", 1
        )
        assert number_of_batches == 1
        assert bl == mock_BatchLists.return_value


def test_bl_creation_bad_input():
    """Test of the _bl_creation function with bad input"""

    with patch("BatchMonitor.lib_app._style_h2") as mock_style_h2, patch(
        "BatchMonitor.lib_app._number_creation", return_value=1
    ) as mock_number_creation, patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["badinput", "bad_input", "Seller1_Batch1:10; 1xapple, 2xbanana"],
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._styled_echo"
    ) as mock_styled_echo, patch(
        "BatchMonitor.lib_app.BatchLists"
    ) as mock_BatchLists, patch(
        "BatchMonitor.lib_app.BatchCollection.from_str",
        side_effect=[ValueError, MagicMock()],
    ) as mock_from_str, patch(
        "BatchMonitor.lib_app._animate_progress_bar"
    ) as mock_animate_progress_bar, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        mock_BatchLists.return_value = MagicMock()
        mock_from_str.return_value = MagicMock()

        number_of_batches, bl = _bl_creation()

        mock_style_h2.assert_called_once_with("BATCHES CREATION : BATCH LISTS")
        mock_number_creation.assert_called_once_with(object="batches")
        mock_styled_prompt.assert_any_call(
            "\n[red]⠹ 100.0% : [/red]Enter the Batch n°1"
        )
        mock_from_str.assert_any_call("input", seller="bad")
        assert mock_style_invalid_choice.call_count == 2
        assert mock_styled_echo.call_count == 6
        mock_from_str.assert_any_call("Batch1:10; 1xapple, 2xbanana", seller="Seller1")
        mock_animate_progress_bar.assert_called_once_with(
            "Initialization of the problems", 1
        )
        assert number_of_batches == 1
        assert bl == mock_BatchLists.return_value


def test_item_request_creation():
    """Test of the _item_request_creation function of the BatchMonitor application"""

    with patch("BatchMonitor.lib_app._style_h2") as mock_style_h2, patch(
        "BatchMonitor.lib_app._number_creation", return_value=3
    ) as mock_number, patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaa", "1-3 of apple", "2-5 of banana", "3-4 of orange"],
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._styled_echo"
    ) as mock_style_echo, patch(
        "BatchMonitor.lib_app.ItemListRequest"
    ) as mock_ItemListRequest, patch(
        "BatchMonitor.lib_app.ItemRequest.from_str",
        side_effect=[ValueError, MagicMock(), MagicMock(), MagicMock()],
    ) as mock_from_str, patch(
        "BatchMonitor.lib_app._animate_progress_bar"
    ) as mock_animate_progress_bar, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        mock_ItemListRequest.return_value = MagicMock()
        mock_from_str.return_value = MagicMock()

        ilr = _item_request_creation()

        mock_style_h2.assert_called_once_with("ITEM REQUEST CREATION")
        mock_number.assert_called_once_with(object="items")
        assert mock_styled_prompt.call_args_list == [
            call("\n[red]⠹ 33.33% : [/red]Enter the item n°1 you want to request"),
            call("\n[red]⠹ 33.33% : [/red]Enter the item n°1 you want to request"),
            call("\n[red]⠹ 66.67% : [/red]Enter the item n°2 you want to request"),
            call("\n[red]⠹ 100.0% : [/red]Enter the item n°3 you want to request"),
        ]
        assert mock_style_echo.call_count == 4
        assert mock_style_invalid_choice.call_count == 1
        mock_animate_progress_bar.assert_called_once_with(
            "Initialization of the problems", 3
        )
        assert ilr == mock_ItemListRequest.return_value


def test_transform_string_category():
    """Test of the _transform_string_category function of the BatchMonitor application"""

    assert _transform_string_category("continuous") == "Continuous"
    assert _transform_string_category("integer") == "Integer"
    assert _transform_string_category("Continuous") == "Continuous"
    assert _transform_string_category("Integer") == "Integer"


def test_init_of_one_category_for_all_batch_quantities():
    """Test of the _init_category_of_batch_quantities function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["ddd", "one", "cc", "continuous"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        category = _init_category_of_batch_quantities(
            BatchLists.from_str(
                strings=[
                    "Seller1_Batch1:10; 1xapple, 2xbanana",
                    "Seller1_Batch2:10; 1xapple, 2xbanana",
                ]
            )
        )
        assert category == "Continuous"
        mock_prompt.assert_any_call(
            "\nDo you want to add one category for all quantity's variables or one category for each quantity's variable ? [rgb(255,255,0)](one/all)"
        )
        mock_prompt.assert_called_with(
            "Enter the category of batch quantity's variable [rgb(255,255,0)](Continuous, Integer)"
        )
        mock_prompt.call_count == 4
        mock_style_invalid_choice.call_count == 1


def test_init_of_category_for_each_batch_quantity():
    """Test of the _init_category_of_batch_quantities function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["ddd", "all", "cc", "continuous", "integer"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        category = _init_category_of_batch_quantities(
            BatchLists.from_str(
                strings=[
                    "Seller1_Batch1:10; 1xapple, 2xbanana",
                    "Seller1_Batch2:10; 1xapple, 2xbanana",
                ]
            )
        )
        assert category == dict(
            Seller1_Batch1="Continuous",
            Seller1_Batch2="Integer",
        )
        mock_prompt.assert_any_call(
            "\nDo you want to add one category for all quantity's variables or one category for each quantity's variable ? [rgb(255,255,0)](one/all)"
        )
        mock_prompt.assert_called_with(
            "Enter the category of batch quantity's variable : Seller1_Batch2. [rgb(255,255,0)](Continuous, Integer)"
        )
        mock_prompt.call_count == 5
        mock_style_invalid_choice.call_count == 1


def test_init_objective_function_constraints_prompt_expense():
    """Test of the _init_objective_function_constraints_prompt function for expenses"""
    choice_prompt, min_prompt, max_prompt, error_prompt = (
        _init_objective_function_constraints_prompt(
            "minimum expense", "maximum expense"
        )
    )
    assert (
        choice_prompt
        == "Do you have minimum expenses constraints, maximum expenses constraints or both ?"
    )
    assert min_prompt == "Enter the minimum expense the customer has to spend."
    assert max_prompt == "Enter the maximum expense the customer can spend."
    assert (
        error_prompt
        == "The expenses must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
    )


def test_init_objective_function_constraints_min_greater_than_max():
    """Test of the _init_objective_function_constraints function for the minimum constraint greater than the maximum constraint"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaa", "both", "zzzz", "10", "5", "10", "20"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._init_objective_function_constraints_prompt",
        return_value=("choice_prompt", "min_prompt", "max_prompt", "error_prompt"),
    ), patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        minimum, maximum = _init_objective_function_constraints(
            "minimum expense", "maximum expense"
        )
        assert minimum == 10.0
        assert maximum == 20.0
        mock_prompt.assert_has_calls(
            [
                call("\nchoice_prompt [rgb(255,255,0)](min/max/both)"),
                call("\nchoice_prompt [rgb(255,255,0)](min/max/both)"),
                call("min_prompt"),
                call("min_prompt"),
                call("max_prompt"),
                call("min_prompt"),
                call("max_prompt"),
            ]
        )
        mock_style_invalid_choice.assert_called_with("error_prompt")
        mock_style_invalid_choice.call_count == 3


def test_init_objective_function_constraints_prompt_benefit():
    """Test of the _init_objective_function_constraints_prompt function for benefits"""

    choice_prompt, min_prompt, max_prompt, error_prompt = (
        _init_objective_function_constraints_prompt(
            "minimum benefit", "maximum benefit"
        )
    )
    assert (
        choice_prompt
        == "Do you have minimum benefits constraints, maximum benefits constraints or both ?"
    )
    assert min_prompt == "Enter the minimum benefit the seller has to earn."
    assert max_prompt == "Enter the maximum benefit the seller can earn."
    assert (
        error_prompt
        == "The benefits must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
    )


def test_init_objective_function_constraints_min():
    """Test of the _init_objective_function_constraints function for the minimum constraint"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaa", "min", "zzzz", "10"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._init_objective_function_constraints_prompt",
        return_value=("choice_prompt", "min_prompt", "max_prompt", "error_prompt"),
    ), patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        minimum, maximum = _init_objective_function_constraints(
            "minimum expense", "maximum expense"
        )
        assert minimum == 10.0
        assert maximum is None
        mock_prompt.assert_has_calls(
            [call("\nchoice_prompt [rgb(255,255,0)](min/max/both)"), call("min_prompt")]
        )
        mock_style_invalid_choice.assert_called_with("error_prompt")
        mock_style_invalid_choice.call_count == 2


def test_init_objective_function_constraints_max():
    """Test of the _init_objective_function_constraints function for the maximum constraint"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaaa", "max", "bbb", "20"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._init_objective_function_constraints_prompt",
        return_value=("choice_prompt", "min_prompt", "max_prompt", "error_prompt"),
    ), patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        minimum, maximum = _init_objective_function_constraints(
            "minimum expense", "maximum expense"
        )
        assert minimum is None
        assert maximum == 20.0
        mock_prompt.assert_has_calls(
            [call("\nchoice_prompt [rgb(255,255,0)](min/max/both)"), call("max_prompt")]
        )
        mock_style_invalid_choice.assert_called_with("error_prompt")
        mock_style_invalid_choice.call_count == 2


def test_init_objective_function_constraints_both():
    """Test of the _init_objective_function_constraints function for both constraints"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt", side_effect=["both", "10", "20"]
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._init_objective_function_constraints_prompt",
        return_value=("choice_prompt", "min_prompt", "max_prompt", "error_prompt"),
    ):
        minimum, maximum = _init_objective_function_constraints(
            "minimum expense", "maximum expense"
        )
        assert minimum == 10.0
        assert maximum == 20.0
        mock_prompt.assert_has_calls(
            [
                call("\nchoice_prompt [rgb(255,255,0)](min/max/both)"),
                call("min_prompt"),
                call("max_prompt"),
            ]
        )


def test_init_rates_exchange_rate():
    """Test of the _init_rates function for the exchange rate"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt", side_effect=["aaa", "1"]
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._verify_rates", return_value=True
    ) as mock_verify, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_invalid:
        rates = _init_rates("exchange rate", 3)
        assert rates == 1.0
        mock_invalid.assert_called_once_with(
            "The rates must be numbers.\nFurthermore, the number of rates must be equal to the number of batches or equal to 1."
        )
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nTake the requester's point of view.\n[rgb(255,255,0)](Default: 1,1,....,1 or 1 for all batches) => (batch_cost x exchange rate)[/rgb(255,255,0)]\nEnter the [red]exchange rate[/red] you have for the [red]3[/red] batches"
                ),
                call(
                    "\nTake the requester's point of view.\n[rgb(255,255,0)](Default: 1,1,....,1 or 1 for all batches) => (batch_cost x exchange rate)[/rgb(255,255,0)]\nEnter the [red]exchange rate[/red] you have for the [red]3[/red] batches"
                ),
            ]
        )
        mock_verify.assert_called_once_with(np.array([1]), 3)


def test_init_rates_tax_rate():
    """Test of the _init_rates function for the tax rate"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt", side_effect=["a,b,c", "0,1,2"]
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._verify_rates", return_value=True
    ), patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_invalid:
        rates = _init_rates("tax rate", 3)
        assert (rates == np.array([0, 1, 2])).all()
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nTake the requester's point of view.\n[rgb(255,255,0)](Default: 0,0,....,0 or 0 for all batches) => (batch_cost x (1+tax rate)[/rgb(255,255,0)]\nEnter the [red]tax rate[/red] you have for the [red]3[/red] batches"
                ),
                call(
                    "\nTake the requester's point of view.\n[rgb(255,255,0)](Default: 0,0,....,0 or 0 for all batches) => (batch_cost x (1+tax rate)[/rgb(255,255,0)]\nEnter the [red]tax rate[/red] you have for the [red]3[/red] batches"
                ),
            ]
        )

        mock_invalid.assert_called_once_with(
            "The rates must be numbers.\nFurthermore, the number of rates must be equal to the number of batches or equal to 1."
        )


def test_verify_rates():
    """Test of the _verify_rates function of the BatchMonitor application"""

    assert _verify_rates(np.array([1, 2, 3]), 3)
    assert _verify_rates(np.array([1]), 3)
    assert not _verify_rates(np.array([1, 2, 3]), 2)
    assert not _verify_rates(np.array([1, 2, 3]), 4)


def test_batch_transformation():
    """Test of the _batch_transformation function of the BatchMonitor application"""

    bc = BatchCollection.from_str(
        "seller 1_batch 1: 1; 2xapple, 5xbanana, 6xorange",
        "seller 1_batch 2: 2; 3xapple, 4xbanana, 5xorange",
        "seller 1_batch 3: 3; 4xapple, 3xbanana, 4xorange",
        seller="Default seller",
    )
    bl = BatchLists.from_str(
        strings=[
            "seller 1_batch 1: 1; 2xapple, 5xbanana, 6xorange",
            "seller 1_batch 2: 2; 3xapple, 4xbanana, 5xorange",
            "seller 1_batch 3: 3; 4xapple, 3xbanana, 4xorange",
        ]
    )

    assert _batch_transformation(bc) == bc
    assert _batch_transformation(bl) == bc


def test_init_batch_constraints():
    """Test of the _init_batch_constraints function of the BatchMonitor application"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["both", "1", "2", "3", "4"],
    ) as mock_prompt:
        result = _init_batch_constraints(batch_list)
        expected_result = {
            "batch1": (1.0, 2.0),
            "batch2": (3.0, 4.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum quantity of the batch [red]batch1"),
                call("Enter the maximum quantity of the batch [red]batch1"),
                call("Enter the minimum quantity of the batch [red]batch2"),
                call("Enter the maximum quantity of the batch [red]batch2"),
            ]
        )


def test_init_batch_constraints_min():
    """Test of the _init_batch_constraints function for the minimum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaa", "min", "aaaa", "1", "2"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_batch_constraints(batch_list)
        expected_result = {
            "batch1": (1.0, None),
            "batch2": (2.0, None),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum quantity of the batch [red]batch1"),
                call("Enter the minimum quantity of the batch [red]batch1"),
                call("Enter the minimum quantity of the batch [red]batch2"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The quantities must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_batch_constraints_max():
    """Test of the _init_batch_constraints function for the maximum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaaa", "max", "aaaaa", "1", "2"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_batch_constraints(batch_list)
        expected_result = {
            "batch1": (None, 1.0),
            "batch2": (None, 2.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the maximum quantity of the batch [red]batch1"),
                call("Enter the maximum quantity of the batch [red]batch1"),
                call("Enter the maximum quantity of the batch [red]batch2"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The quantities must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_batch_constraints_both_min_greater_than_max():
    """Test of the _init_batch_constraints function for both constraints with the minimum constraint greater than the maximum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["both", "2", "1", "1", "2", "3", "4"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_batch_constraints(batch_list)
        expected_result = {
            "batch1": (1.0, 2.0),
            "batch2": (3.0, 4.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum quantity of the batch [red]batch1"),
                call("Enter the maximum quantity of the batch [red]batch1"),
                call("Enter the minimum quantity of the batch [red]batch1"),
                call("Enter the maximum quantity of the batch [red]batch1"),
                call("Enter the minimum quantity of the batch [red]batch2"),
                call("Enter the maximum quantity of the batch [red]batch2"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The quantities must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_minBatchExpense():
    """Test of the _init_minBatchExpense function of the BatchMonitor application"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    number_of_batches = len(batch_list)
    category_of_variables = True
    function_constraints = True
    rates = True
    variable_constraints = True

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=[
            "all",
            "Continuous",
            "Integer",
            "both",
            "1",
            "2",
            "1",
            "0",
            "0",
            "0",
            "both",
            "1",
            "2",
            "2",
            "4",
        ],
    ):
        result = _init_minBatchExpense(
            number_of_batches,
            batch_list,
            category_of_variables,
            function_constraints,
            rates,
            variable_constraints,
        )
        expected_result = (
            {
                "batch1": "Continuous",
                "batch2": "Integer",
            },
            1.0,
            2.0,
            1.0,
            0.0,
            0.0,
            0.0,
            {
                "batch1": (1.0, 2.0),
                "batch2": (2.0, 4.0),
            },
        )
        assert result == expected_result


def test_init_minBatchExpense_without_option():
    """Test of the _init_minBatchExpense function of the BatchMonitor application without option"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana, 5xorange",
        seller="seller 1",
    )
    number_of_batches = len(batch_list)
    category_of_variables = False
    function_constraints = False
    rates = False
    variable_constraints = False

    with patch("BatchMonitor.lib_app._styled_prompt"):
        result = _init_minBatchExpense(
            number_of_batches,
            batch_list,
            category_of_variables,
            function_constraints,
            rates,
            variable_constraints,
        )
        expected_result = (
            "Continuous",
            None,
            None,
            1,
            0,
            0,
            0,
            None,
        )
        assert result == expected_result


def test_init_of_one_category_for_all_item_price():
    """Test of the _init_category_of_item_prices function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["ddd", "one", "cc", "continuous"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        category = _init_category_of_item_prices(
            BatchLists.from_str(
                strings=[
                    "Seller1_Batch1:10; 1xapple, 2xbanana",
                    "Seller1_Batch2:10; 1xapple, 2xbanana",
                ]
            )
        )
        assert category == "Continuous"
        mock_prompt.assert_any_call(
            "\nDo you want to add one category for all item price's variables or one category for each item price's variables ? [rgb(255,255,0)](one/all)"
        )
        mock_prompt.assert_called_with(
            "Enter the category of item price's variables [rgb(255,255,0)](Continuous, Integer)"
        )
        mock_prompt.call_count == 4
        mock_style_invalid_choice.call_count == 1


def test_init_of_category_for_each_item_prices():
    """Test of the _init_category_of_item_prices function of the BatchMonitor application"""

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["ddd", "all", "cc", "continuous", "integer"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        category = _init_category_of_item_prices(
            BatchLists.from_str(
                strings=[
                    "Seller1_Batch1:10; 1xapple, 2xbanana",
                    "Seller1_Batch2:10; 1xapple, 2xbanana",
                ]
            )
        )
        assert category == dict(
            apple="Continuous",
            banana="Integer",
        )
        mock_prompt.assert_any_call(
            "\nDo you want to add one category for all item price's variables or one category for each item price's variables ? [rgb(255,255,0)](one/all)"
        )
        mock_prompt.assert_called_with(
            "Enter the category of item price's variable : [red]banana[/red]. [rgb(255,255,0)](Continuous, Integer)"
        )
        mock_prompt.call_count == 5
        mock_style_invalid_choice.call_count == 1


def test_init_item_prices_constraints():
    """Test of the _init_item_prices_constraints function of the BatchMonitor application"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["both", "1", "2", "3", "4"],
    ) as mock_prompt:
        result = _init_item_prices_constraints(batch_list)
        expected_result = {
            "apple": (1.0, 2.0),
            "banana": (3.0, 4.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum price of the item [red]apple"),
                call("Enter the maximum price of the item [red]apple"),
                call("Enter the minimum price of the item [red]banana"),
                call("Enter the maximum price of the item [red]banana"),
            ]
        )


def test_init_item_prices_constraints_min():
    """Test of the _init_item_prices_constraints function for the minimum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaa", "min", "aaaa", "1", "2"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_item_prices_constraints(batch_list)
        expected_result = {
            "apple": (1.0, None),
            "banana": (2.0, None),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum price of the item [red]apple"),
                call("Enter the minimum price of the item [red]apple"),
                call("Enter the minimum price of the item [red]banana"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The prices must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_item_prices_constraints_max():
    """Test of the _init_item_prices_constraints function for the maximum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["aaaaa", "max", "aaaaa", "1", "2"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_item_prices_constraints(batch_list)
        expected_result = {
            "apple": (None, 1.0),
            "banana": (None, 2.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the maximum price of the item [red]apple"),
                call("Enter the maximum price of the item [red]apple"),
                call("Enter the maximum price of the item [red]banana"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The prices must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_item_prices_constraints_both_min_greater_than_max():
    """Test of the _init_item_prices_constraints function for both constraints with the minimum constraint greater than the maximum constraint"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=["both", "2", "1", "1", "2", "3", "4"],
    ) as mock_prompt, patch(
        "BatchMonitor.lib_app._style_invalid_choice"
    ) as mock_style_invalid_choice:
        result = _init_item_prices_constraints(batch_list)
        expected_result = {
            "apple": (1.0, 2.0),
            "banana": (3.0, 4.0),
        }
        assert result == expected_result
        mock_prompt.assert_has_calls(
            [
                call(
                    "\nDo you have minimum prices constraints, maximum prices constraints or both ? [rgb(255,255,0)](min/max/both)"
                ),
                call("Enter the minimum price of the item [red]apple"),
                call("Enter the maximum price of the item [red]apple"),
                call("Enter the minimum price of the item [red]apple"),
                call("Enter the maximum price of the item [red]apple"),
                call("Enter the minimum price of the item [red]banana"),
                call("Enter the maximum price of the item [red]banana"),
            ]
        )
        mock_style_invalid_choice.assert_called_once_with(
            "The prices must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
        )


def test_init_maxEarnings():
    """Test of the _init_minBatchExpense function of the BatchMonitor application"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    number_of_batches = len(batch_list)
    category_of_variables = True
    function_constraints = True
    rates = True
    variable_constraints = True

    with patch(
        "BatchMonitor.lib_app._styled_prompt",
        side_effect=[
            "all",
            "Continuous",
            "Integer",
            "both",
            "1",
            "2",
            "1",
            "0",
            "0",
            "0",
            "both",
            "1",
            "2",
            "2",
            "4",
        ],
    ):
        result = _init_maxEarnings(
            number_of_batches,
            batch_list,
            category_of_variables,
            function_constraints,
            rates,
            variable_constraints,
        )
        expected_result = (
            {
                "apple": "Continuous",
                "banana": "Integer",
            },
            1.0,
            2.0,
            1.0,
            0.0,
            0.0,
            0.0,
            {
                "apple": (1.0, 2.0),
                "banana": (2.0, 4.0),
            },
        )
        assert result == expected_result


def test_init_maxEarnings_without_option():
    """Test of the _init_maxEarnings function of the BatchMonitor application without option"""

    batch_list = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )
    number_of_batches = len(batch_list)
    category_of_variables = False
    function_constraints = False
    rates = False
    variable_constraints = False

    with patch("BatchMonitor.lib_app._styled_prompt"):
        result = _init_maxEarnings(
            number_of_batches,
            batch_list,
            category_of_variables,
            function_constraints,
            rates,
            variable_constraints,
        )
        expected_result = (
            "Continuous",
            None,
            None,
            1,
            0,
            0,
            0,
            None,
        )
        assert result == expected_result


def test_verify_valid_ilr():
    """Test of the _verify_valid_ilr function of the BatchMonitor application"""

    bc = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )

    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of orange",
    )

    assert not _verify_valid_ilr(ilr, bc)

    bc = BatchCollection.from_str(
        "batch1: 1; 2xapple, 5xbanana, 6xorange",
        "batch2: 2; 3xapple, 4xbanana",
        seller="seller 1",
    )

    assert _verify_valid_ilr(ilr, bc)


def test_delete_json_files():
    files_to_delete = [
        "demo_batchcollection.json",
        "demo_batchlists.json",
        "demo_itemlistrequest.json",
        "bad_demo_itemlistrequest.json",
    ]
    for file in files_to_delete:
        os.remove(file)
