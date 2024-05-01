"""Description of the app.
Module contains the user interface of the batches_optimization package.

- This app work much with some prompt functions to get the user's choices.
- The user can choose the problem he wants to resolve, the type of batches he wants to create, the number of batches he wants to create, the number of items he wants to create, the category of the variables, the constraints he wants to set on the variables, the rates he wants to apply on the prices of the batches, the constraints he wants to set on the expenses of the customer, the constraints he wants to set on the prices of the items, the constraints he wants to set on the benefits of the retailer, the constraints he wants to set on the quantities of the batches.

Developed by :
    - [Hugo Cochereau](https://github.com/hugocoche)
    - Gregory Jaillet

"""

import os
import sys

import typer
from rich.console import Console
from subprocess import run

from BatchMonitor import (
    BatchCollection,
    BatchLists,
    ItemListRequest,
    format_batch_collection,
    format_batch_lists,
    format_itemlistRequest,
)

from .lib_app import (
    _batch_transformation,
    _init_app,
    _init_batchtype,
    _init_problem,
    _item_request_creation,
    _jaune,
    _stages_progress_both,
    _stages_progress_mbe,
    _stages_progress_me,
    _style_invalid_choice,
    _styled_prompt,
    _thanks,
    _verify_valid_ilr,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

MARKDOWN_TITLE = """
# *WELCOME TO THE BATCHES OPTIMIZATION APP !*
"""
MARKDOWN_DESCRIPTION = """
## Overview
> This app allows you to optimize the expenses of a customer who wants to buy items from different sellers or to maximize the benefits of a retailer who wants to sell items to different customers.

> First of all, you have to type app.py --help to see the different options you can choose.

> If you want to stop the app, you can type CTRL + C.

1. You can create a BatchCollection or a BatchLists object.
2. You can create an ItemListRequest object.
3. You can choose the type of variables for the quantities of the batches and the prices of the items.
4. You can apply different rates on the prices of the batches.
5. You can set constraints on the quantities of the batches.
6. You can set constraints on the expenses of the customer.
7. You can set constraints on the prices of the items.
8. You can set constraints on the benefits of the retailer.
9. You can resolve the optimization problem with the minBatchExpense function, the maxEarnings function or both.

> If you have already created a BatchCollection, BatchLists, and an ItemListRequest object, you can solve the optimization problem with the following command:

- python3 -m batches_optimization solve --batches-path path_to_batches --items-path path_to_items
"""
app = typer.Typer()

console = Console()


def _restart_app(
    category_of_variables: bool = False,
    function_constraints: bool = False,
    rates: bool = False,
    variable_constraints: bool = False,
):
    """Restart the app with the same problem or with a new problem."""

    while True:
        restart = _styled_prompt(f"Do you want to restart the app ? [{_jaune}](yes/no)")
        if restart == "yes":
            init_and_run(
                category_of_variables=category_of_variables,
                function_constraints=function_constraints,
                rates=rates,
                variable_constraints=variable_constraints,
            )
        elif restart == "no":
            _thanks()
            sys.exit()
        else:
            _style_invalid_choice("Invalid choice. Please choose between yes or no.")


@app.command()
def init_and_run(
    category_of_variables: bool = False,
    function_constraints: bool = False,
    rates: bool = False,
    variable_constraints: bool = False,
):
    """
    Run the app with the different options the user can choose. Use this when you didn't create a json file with the batches and the items requested.\n\n

    Args:\n
    - category_of_variables (bool): if True, the user will be prompted to choose the category of the variables which represents the quantities of the batches and the prices of the items.\n\n
    - function_constraints (bool): if True, the user will be prompted to choose the constraints for the objective function of the minBatchExpense problem and the benefits of the maxEarnings problem.\n\n
    - rates (bool): if True, the user will be prompted to choose the rates he has for the batches.\n\n
    - variable_constraints (bool): if True, the user will be prompted to choose the constraints he has for the quantities of the batches and the prices of the items.\n\n

    Returns:
    - The resolution of the minBatchExpense problem.\n
    - The resolution of the maxEarnings problem.\n
    - The resolution of both problems.\n
    """

    _init_app()
    problem = _init_problem()
    number_of_batches, batch_list = _init_batchtype()
    ilr = _item_request_creation()
    while not _verify_valid_ilr(ilr, batch_list):
        _style_invalid_choice(
            "The items requested are not available in the batches. Please enter the items again."
        )
        ilr = _item_request_creation()

    if problem == "minBatchExpense":
        _stages_progress_mbe(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )
        while True:
            response = _styled_prompt(
                f"Do you want to resolve the maxEarnings problem ? [{_jaune}](yes/no)"
            )
            if response == "yes":
                rates_other_problem = False
                _stages_progress_me(
                    number_of_batches=number_of_batches,
                    batch_list=batch_list,
                    ilr=ilr,
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates_other_problem,
                    variable_constraints=variable_constraints,
                )
                _restart_app(
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates,
                    variable_constraints=variable_constraints,
                )
            elif response == "no":
                _restart_app(
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates,
                    variable_constraints=variable_constraints,
                )
            else:
                _style_invalid_choice(
                    "Invalid choice. Please choose between yes or no."
                )

    elif problem == "maxEarnings":
        _stages_progress_me(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )
        while True:
            response = _styled_prompt(
                f"Do you want to resolve the minBatchExpense problem ? [{_jaune}](yes/no)"
            )
            if response == "yes":
                rates_other_problem = False
                _stages_progress_mbe(
                    number_of_batches=number_of_batches,
                    batch_list=batch_list,
                    ilr=ilr,
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates_other_problem,
                    variable_constraints=variable_constraints,
                )
                _restart_app(
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates,
                    variable_constraints=variable_constraints,
                )
            elif response == "no":
                _restart_app(
                    category_of_variables=category_of_variables,
                    function_constraints=function_constraints,
                    rates=rates,
                    variable_constraints=variable_constraints,
                )
            else:
                _style_invalid_choice(
                    "Invalid choice. Please choose between yes or no."
                )

    elif problem == "both":
        _stages_progress_both(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )
        _restart_app(
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )


@app.command()
def demo_batchCollection():
    """Create an example of a BatchCollection object and save it in a json file"""
    bc = BatchCollection.from_str(
        "batch 1: 1; 2xapple, 5xbanana, 6xorange",
        "batch 2: 2; 3xapple, 4xbanana, 5xorange",
        "batch 3: 3; 4xapple, 3xbanana, 4xorange",
        seller="seller 1",
    )
    bc.to_json("demo_batchcollection.json")


@app.command()
def demo_batchLists():
    """Create an example of a BatchLists object and save it in a json file"""
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


@app.command()
def demo_itemListRequest():
    """Create an example of an ItemListRequest object and save it in a json file"""
    ilr = ItemListRequest.from_str(
        "1-3 of apple",
        "2-5 of banana",
        "3-4 of orange",
    )
    ilr.to_json("demo_itemlistrequest.json")


@app.command()
def view_batches(path: str):
    """View the content of a BatchCollection or BatchLists object from a json file

    Args:
    - path (str): path to the json file

    Returns:
    - None

    Raises:
    - Exception: if the json file does not contain a BatchCollection or BatchLists object
    """

    try:
        bc = BatchCollection.from_json(path)
        console.print(format_batch_collection(bc))
    except Exception:
        try:
            bl = BatchLists.from_json(path)
            console.print(format_batch_lists(bl))
        except Exception as error:
            print(error)
            sys.exit(1)


@app.command()
def view_ilr(path: str):
    """View the content of an ItemListRequest object from a json file

    Args:
    - path (str): path to the json file

    Returns:
    - None

    Raises:
    - Exception: if the json file does not contain an ItemListRequest object
    """

    try:
        ilr = ItemListRequest.from_json(path)
        console.print(format_itemlistRequest(ilr))
    except Exception as error:
        print(error)
        sys.exit(1)


def _init_solve() -> tuple[str, str]:
    """Prompt the user to choose the type of the batch object and the type of the problem."""

    while True:
        batch_type = _styled_prompt(
            f"Enter the type of the batch object [{_jaune}](BatchCollection or BatchLists)"
        )
        problem_type = _styled_prompt(
            f"Enter the type of the problem [{_jaune}](minBatchExpense, maxEarnings or both)"
        )
        if batch_type in ["BatchCollection", "BatchLists"]:
            break
        else:
            _style_invalid_choice(
                "Invalid choice. Please choose between BatchCollection and BatchLists"
            )
        if problem_type in ["minBatchExpense", "maxEarnings", "both"]:
            break

    return batch_type, problem_type


def _create_object_from_json(
    batch_type: str, batches_path: str, itemlist_path: str
) -> tuple[BatchCollection | BatchLists, ItemListRequest, int]:
    """Create the BatchCollection or BatchLists object and the ItemListRequest object from the json files."""

    batch_object: BatchCollection | BatchLists
    try:
        if batch_type == "BatchCollection":
            batch_object = BatchCollection.from_json(batches_path)
        elif batch_type == "BatchLists":
            batch_object = BatchLists.from_json(batches_path)
        ilr_object = ItemListRequest.from_json(itemlist_path)
    except Exception as error:
        print(error)
        sys.exit(1)

    batch_transform = _batch_transformation(batch_object)
    if not _verify_valid_ilr(ilr_object, batch_transform):
        _style_invalid_choice("The items requested are not available in the batches")
        sys.exit(1)

    number_of_batches = (
        len(batch_object)
        if isinstance(batch_object, BatchCollection)
        else len(batch_transform)
    )

    return batch_object, ilr_object, number_of_batches


def _solving_problem_choice(
    problem_type: str,
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    category_of_variables: bool,
    function_constraints: bool,
    rates: bool,
    variable_constraints: bool,
):
    """Solve the optimization problem according to the user's choice"""

    if problem_type == "minBatchExpense":
        _stages_progress_mbe(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )

    elif problem_type == "maxEarnings":
        _stages_progress_me(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )

    elif problem_type == "both":
        _stages_progress_both(
            number_of_batches=number_of_batches,
            batch_list=batch_list,
            ilr=ilr,
            category_of_variables=category_of_variables,
            function_constraints=function_constraints,
            rates=rates,
            variable_constraints=variable_constraints,
        )


@app.command()
def solve(
    batches_path: str,
    itemlist_path: str,
    category_of_variables: bool = False,
    function_constraints: bool = False,
    rates: bool = False,
    variable_constraints: bool = False,
):
    """Solve the optimization problem with the BatchCollection or BatchLists object and the ItemListRequest object from the json files.

    Args:
    - batches_path (str): path to the json file containing the BatchCollection or BatchLists object\n
    - itemlist_path (str): path to the json file containing the ItemListRequest object\n
    - category_of_variables (bool): if True, the user will be prompted to choose the category of the variables which represents the quantities of the batches and the prices of the items.\n
    - function_constraints (bool): if True, the user will be prompted to choose the constraints for the objective function of the minBatchExpense problem and the benefits of the maxEarnings problem.\n
    - rates (bool): if True, the user will be prompted to choose the rates he has for the batches.\n
    - variable_constraints (bool): if True, the user will be prompted to choose the constraints he has for the quantities of the batches and the prices of the items.\n

    Returns:
    - None

    Raises:
    - Exception: if the json files do not contain the required objects
    """

    batch_type, problem_type = _init_solve()

    batch_object, ilr_object, number_of_batches = _create_object_from_json(
        batch_type=batch_type, batches_path=batches_path, itemlist_path=itemlist_path
    )

    _solving_problem_choice(
        problem_type=problem_type,
        number_of_batches=number_of_batches,
        batch_list=batch_object,
        ilr=ilr_object,
        category_of_variables=category_of_variables,
        function_constraints=function_constraints,
        rates=rates,
        variable_constraints=variable_constraints,
    )


@app.command()
def API():
    """Run the streamlit app"""
    run(["python", "-m", "streamlit", "run", "BatchMonitor/Welcome.py"])


if __name__ == "__main__":
    app()
