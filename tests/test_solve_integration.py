"""Description:

Integration tests for the solve commands of BatchMonitor application"""

import os
import sys
from io import StringIO
import pytest
from BatchMonitor import BatchCollection, BatchLists, ItemListRequest
from unittest.mock import patch

from BatchMonitor.lib_app import (
    _stages_progress_both,
    _stages_progress_mbe,
    _stages_progress_me,
    _maxEarnings_resolution,
    _minBatchExpense_resolution,
)

from BatchMonitor.__main__ import (
    _solving_problem_choice,
    solve,
    init_and_run,
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def bc_fixture():
    return BatchCollection.from_str(
        "batch1:1; 2xapple, 5xbanana", "batch2:2; 3xapple, 4xbanana", seller="seller1"
    )


@pytest.fixture
def ilr_fixture():
    return ItemListRequest.from_str("1-3 of apple", "4-5 of banana")


@pytest.fixture
def bl_fixture():
    return BatchLists.from_str(
        strings=[
            "seller1_batch1:1; 2xapple, 5xbanana",
            "seller1_batch2:2; 3xapple, 4xbanana",
        ]
    )


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_solving_problem_choice(bc_fixture, ilr_fixture):
    """Test the _solving_problem_choice function"""

    with patch("BatchMonitor.__main__._stages_progress_mbe") as mock_mbe, patch(
        "BatchMonitor.__main__._stages_progress_me"
    ) as mock_me, patch(
        "BatchMonitor.__main__._stages_progress_both"
    ) as mock_both, patch(
        "sys.stdout", new=StringIO()
    ):

        _solving_problem_choice(
            problem_type="minBatchExpense",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        assert mock_mbe.called
        _solving_problem_choice(
            problem_type="maxEarnings",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_me.called

        _solving_problem_choice(
            problem_type="both",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )
        assert mock_both.called


def test_stages_progress_mbe(bc_fixture, ilr_fixture, bl_fixture):
    """Test the _stages_progress_mbe function"""

    with patch(
        "BatchMonitor.lib_app._init_minBatchExpense",
        return_value=["Continuous", 0, 10000000, 1, 0, 0, 0, None],
    ) as mock_init, patch(
        "BatchMonitor.lib_app._minBatchExpense_resolution"
    ) as mock_resolution, patch(
        "BatchMonitor.lib_app.format_batch_collection",
        return_value="batch_collection",
    ) as mock_format_bc, patch(
        "BatchMonitor.lib_app.format_itemlistRequest", return_value="ilr"
    ) as mock_format_ilr, patch(
        "BatchMonitor.lib_app._printed_mbe", return_value="result"
    ) as mock_printed, patch(
        "BatchMonitor.lib_app.format_batch_lists", return_value="batch_lists"
    ) as mock_format_batch_lists:

        _stages_progress_mbe(
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init.assert_called_once()
        mock_resolution.assert_called_once()
        mock_format_bc.assert_called_once_with(bc_fixture)
        mock_format_ilr.assert_called_once_with(ilr_fixture)
        mock_printed.assert_called_once()

        _stages_progress_mbe(
            number_of_batches=2,
            batch_list=bl_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )
        mock_format_batch_lists.assert_called_once()


def test_stages_progress_me(bc_fixture, ilr_fixture, bl_fixture):
    """Test the _stages_progress_me function"""

    with patch(
        "BatchMonitor.lib_app._init_maxEarnings",
        return_value=["Continuous", 0, 10000000, 1, 0, 0, 0, None],
    ) as mock_init, patch(
        "BatchMonitor.lib_app._maxEarnings_resolution"
    ) as mock_resolution, patch(
        "BatchMonitor.lib_app.format_batch_collection",
        return_value="batch_collection",
    ) as mock_format_bc, patch(
        "BatchMonitor.lib_app.format_itemlistRequest", return_value="ilr"
    ) as mock_format_ilr, patch(
        "BatchMonitor.lib_app._printed_me", return_value="result"
    ) as mock_printed, patch(
        "BatchMonitor.lib_app.format_batch_lists", return_value="batch_lists"
    ) as mock_format_batch_lists:

        _stages_progress_me(
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init.assert_called_once()
        mock_resolution.assert_called_once()
        mock_format_bc.assert_called_once_with(bc_fixture)
        mock_format_ilr.assert_called_once_with(ilr_fixture)
        mock_printed.assert_called_once()

        _stages_progress_me(
            number_of_batches=2,
            batch_list=bl_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )
        mock_format_batch_lists.assert_called_once()


def test_stages_progress_both(bc_fixture, ilr_fixture, bl_fixture):
    """Test the _stages_progress_both function"""

    with patch(
        "BatchMonitor.lib_app._init_minBatchExpense",
        return_value=["Continuous", 0, 10000000, 1, 0, 0, 0, None],
    ) as mock_init_mbe, patch(
        "BatchMonitor.lib_app._init_maxEarnings",
        return_value=["Continuous", 0, 10000000, 1, 0, 0, 0, None],
    ) as mock_init_me, patch(
        "BatchMonitor.lib_app._minBatchExpense_resolution"
    ) as mock_mbe_resolution, patch(
        "BatchMonitor.lib_app._maxEarnings_resolution"
    ) as mock_me_resolution, patch(
        "BatchMonitor.lib_app.format_batch_collection",
        return_value="batch_collection",
    ) as mock_format_bc, patch(
        "BatchMonitor.lib_app.format_itemlistRequest", return_value="ilr"
    ) as mock_format_ilr, patch(
        "BatchMonitor.lib_app._printed_both", return_value="result"
    ) as mock_printed, patch(
        "BatchMonitor.lib_app.format_batch_lists", return_value="batch_lists"
    ) as mock_format_batch_lists:

        _stages_progress_both(
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init_mbe.assert_called_once()
        mock_init_me.assert_called_once()
        mock_mbe_resolution.assert_called_once()
        mock_me_resolution.assert_called_once()
        mock_format_bc.assert_called_once_with(bc_fixture)
        mock_format_ilr.assert_called_once_with(ilr_fixture)
        mock_printed.assert_called_once()

        _stages_progress_both(
            number_of_batches=2,
            batch_list=bl_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )
        mock_format_batch_lists.assert_called_once()


def test_maxEarnings_resolution(bc_fixture, ilr_fixture):
    """Test the _maxEarnings_resolution function"""

    with patch("BatchMonitor.lib_app.maxEarnings") as mock_maxEarnings, patch(
        "BatchMonitor.lib_app.format_maxEarnings", return_value="result"
    ) as mock_format_maxEarnings:

        _maxEarnings_resolution(
            bc=bc_fixture,
            ilr=ilr_fixture,
            cat_of_variables=False,
            min_benefit=None,
            max_benefit=None,
            exchange_rate=1,
            tax_rate=0,
            custom_duties=0,
            transport_fee=0,
            item_prices_constraints=None,
        )

        mock_maxEarnings.assert_called_once()
        mock_format_maxEarnings.assert_called_once()


def test_minBatchExpense_resolution(bc_fixture, ilr_fixture):
    """Test the _minBatchExpense_resolution function"""

    with patch("BatchMonitor.lib_app.minBatchExpense") as mock_minBatchExpense, patch(
        "BatchMonitor.lib_app.format_minBatchExpense", return_value="result"
    ) as mock_format_minBatchExpense:

        _minBatchExpense_resolution(
            bc=bc_fixture,
            ilr=ilr_fixture,
            cat_of_variables=False,
            min_expense=None,
            max_expense=None,
            exchange_rate=1,
            tax_rate=0,
            custom_duties=0,
            transport_fee=0,
            batches_constraints=None,
        )

        mock_minBatchExpense.assert_called_once()
        mock_format_minBatchExpense.assert_called_once()


def test_solve_mbe(bc_fixture, ilr_fixture):
    """Test the solve function"""

    with patch(
        "BatchMonitor.__main__._init_solve",
        return_value=("BatchCollection", "minBatchExpense"),
    ) as mock_init_solve, patch(
        "BatchMonitor.__main__._create_object_from_json",
        return_value=(bc_fixture, ilr_fixture, 2),
    ) as mock_create_object_from_json, patch(
        "BatchMonitor.__main__._solving_problem_choice"
    ) as mock_solving_problem_choice:

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init_solve.assert_called_once()
        mock_create_object_from_json.assert_called_once()
        mock_solving_problem_choice.assert_called_once()

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )

        mock_solving_problem_choice.assert_called_with(
            problem_type="minBatchExpense",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )


def test_solve_me(bc_fixture, ilr_fixture):
    """Test the solve function"""

    with patch(
        "BatchMonitor.__main__._init_solve",
        return_value=("BatchCollection", "maxEarnings"),
    ) as mock_init_solve, patch(
        "BatchMonitor.__main__._create_object_from_json",
        return_value=(bc_fixture, ilr_fixture, 2),
    ) as mock_create_object_from_json, patch(
        "BatchMonitor.__main__._solving_problem_choice"
    ) as mock_solving_problem_choice:

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init_solve.assert_called_once()
        mock_create_object_from_json.assert_called_once()
        mock_solving_problem_choice.assert_called_once()

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )

        mock_solving_problem_choice.assert_called_with(
            problem_type="maxEarnings",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )


def test_solve_both(bc_fixture, ilr_fixture):
    """Test the solve function"""

    with patch(
        "BatchMonitor.__main__._init_solve",
        return_value=("BatchCollection", "both"),
    ) as mock_init_solve, patch(
        "BatchMonitor.__main__._create_object_from_json",
        return_value=(bc_fixture, ilr_fixture, 2),
    ) as mock_create_object_from_json, patch(
        "BatchMonitor.__main__._solving_problem_choice"
    ) as mock_solving_problem_choice:

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=False,
            function_constraints=False,
            rates=False,
            variable_constraints=False,
        )

        mock_init_solve.assert_called_once()
        mock_create_object_from_json.assert_called_once()
        mock_solving_problem_choice.assert_called_once()

        solve(
            batches_path="batches_path",
            itemlist_path="itemlist_path",
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )

        mock_solving_problem_choice.assert_called_with(
            problem_type="both",
            number_of_batches=2,
            batch_list=bc_fixture,
            ilr=ilr_fixture,
            category_of_variables=True,
            function_constraints=True,
            rates=True,
            variable_constraints=True,
        )


def test_init_and_run_me_bc(bc_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="maxEarnings"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bc_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_me"
    ) as mock_stages_progress_me, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_me.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_mbe_bc(bc_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="minBatchExpense"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bc_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_mbe"
    ) as mock_stages_progress_mbe, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_mbe.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_both_bc(bc_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="both"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bc_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_both"
    ) as mock_stages_progress_both, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_both.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_mbe_bl(bl_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="minBatchExpense"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bl_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_mbe"
    ) as mock_stages_progress_mbe, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_mbe.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_both_bl(bl_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="both"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bl_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_both"
    ) as mock_stages_progress_both, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_both.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_me_bl(bl_fixture, ilr_fixture):
    """Test the init_and_run function"""

    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="maxEarnings"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bl_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation", return_value=ilr_fixture
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", return_value=True
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._stages_progress_me"
    ) as mock_stages_progress_me, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.__main__._thanks"
    ) as mock_thanks, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.assert_called_once()
        mock_verify_valid_ilr.assert_called_once()
        mock_stages_progress_me.assert_called_once()
        mock_styled_prompt.assert_called()
        mock_thanks.assert_called_once()
        mock_style_h2.call_count == 4


def test_init_and_run_mbe_bc_invalid_ilr(bc_fixture, ilr_fixture):
    """Test the init_and_run function"""

    bad_ilr = ItemListRequest.from_str("1-3 of apple", "4-5 of orange")
    with patch("BatchMonitor.__main__._init_app") as mock_init_app, patch(
        "BatchMonitor.__main__._init_problem", return_value="minBatchExpense"
    ) as mock_init_problem, patch(
        "BatchMonitor.__main__._init_batchtype", return_value=(2, bc_fixture)
    ) as mock_init_batchtype, patch(
        "BatchMonitor.__main__._item_request_creation",
        side_effect=[bad_ilr, ilr_fixture],
    ) as mock_item_request_creation, patch(
        "BatchMonitor.__main__._verify_valid_ilr", side_effect=[False, True]
    ) as mock_verify_valid_ilr, patch(
        "BatchMonitor.__main__._styled_prompt", side_effect=["no", "no"]
    ) as mock_styled_prompt, patch(
        "BatchMonitor.lib_app._style_h2"
    ) as mock_style_h2:

        with pytest.raises(SystemExit):
            init_and_run()

        mock_init_app.assert_called_once()
        mock_init_problem.assert_called_once()
        mock_init_batchtype.assert_called_once()
        mock_item_request_creation.call_count == 2
        mock_verify_valid_ilr.call_count == 2
        mock_styled_prompt.assert_called()
        mock_style_h2.call_count == 5
