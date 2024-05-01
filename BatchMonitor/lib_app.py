"""Description.

This module contains the different functiions used for the app"""

import copy
import os
import sys
import time

import numpy as np
import rich
import rich.table
from rich.console import Console
from rich.layout import Layout
from rich.markdown import Markdown
from rich.progress import Progress
from rich.prompt import Prompt

from BatchMonitor import (
    Batch,
    BatchCollection,
    BatchLists,
    ItemListRequest,
    ItemRequest,
    format_batch_collection,
    format_batch_lists,
    format_itemlistRequest,
    format_maxEarnings,
    format_minBatchExpense,
    maxEarnings,
    minBatchExpense,
)

from .lib_optimization import _transform_batch_list

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

- python -m BatchMonitor solve path_to_batches path_to_items
"""


console = Console()

_jaune = "rgb(255,255,0)"


def _animate_progress_bar(object: str, total: int):
    """Animate a progress bar for the creation of batches or items."""

    console.print("\n \n")
    with Progress(console=console) as progress:
        task_id = progress.add_task(f"[red]{object}...", total=total)
        for _ in range(total):
            progress.update(task_id, advance=1)
            time.sleep(0.1)


def _resolution_progress_bar(object: str):
    """Animate a progress bar for the resolution of the optimization problem."""

    total = 20
    sleep_time = 0.1

    console.print("\n \n")
    with Progress() as progress:
        task_id = progress.add_task(f"[red]{object}...", total=total)
        for _ in range(total):
            progress.update(task_id, advance=1)
            time.sleep(sleep_time)


def _styled_prompt(text: str) -> str:
    """Prompt the user with a styled message."""

    return Prompt.ask(f"[cyan]{text}[/cyan]")


def _styled_echo(text: str):
    """Echo a styled message."""

    return console.print(f"[{_jaune}]{text}")


def _style_h2(text: str):
    """Echo a styled message with a h2 title."""

    return console.print(
        "\n", Markdown(f"## {text}"), "\n", style="magenta", justify="center"
    )


def _style_invalid_choice(text: str):
    """Echo a styled message with an invalid choice."""

    return console.print(text, ":angry: !", "\n", style="red")


def _thanks():
    console.print(
        r"""
_________________________________________________________
|     _____  _   _    _    _   _  _  _  _____            |
|       |    |   |  (   )  |\  |  |  /  |        | | |   |
|       |    |___|  |___|  | \ |  | /   |___     | | |   |
|       |    |   |  |   |  |  \|  |/\       |    | | |   |
|       |    |   |  |   |  |   |  |  \  ____|    . . .   |
|________________________________________________________|
""",
        style="white",
        justify="center",
    )
    console.print(
        r"""
|                                          /\             /\             /\                                        |
|                                         /  \           /  \           /  \                                       |
|                                        /    \         /    \         /    \                                      |
|                                       /______\       /______\       /______\                                     |
|                                       |      |       |      |       |      |                                     |
|                                       |      |       |      |       |      |                                     |
|                                       |  /\  |       |  /\  |       |  /\  |                                     |
|                                       | /  \ |       | /  \ |       | /  \ |                                     |
|                                       |/____\|       |/____\|       |/____\|                                     |
|                                      /|      |\     /|      |\     /|      |\                                    |
|                                     /_|______|_\   /_|______|_\   /_|______|_\                                   |
|                                    |  |      |  | |  |      |  | |  |      |  |                                  |
|                                    |__|______|__| |__|______|__| |__|______|__|                                  |
|                                       |      |       |      |       |      |                                     |
|                                       |      |       |      |       |      |                                     |
""",
        style="white",
        justify="center",
    )


def _init_app():
    """Show the title and the description of the app."""

    console.print(Markdown(MARKDOWN_TITLE), justify="center")
    console.print(5 * ":rocket:", justify="center")
    console.print(Markdown(MARKDOWN_DESCRIPTION), "\n")


def _init_problem():
    """Prompt the user to choose the problem he wants to resolve."""

    _style_h2("PROBLEM SELECTION")
    console.print("\n")
    problem = ""
    while problem not in ["minBatchExpense", "maxEarnings", "both"]:
        problem = _styled_prompt(
            f"Which problem do you want to resolve ? [{_jaune}](minBatchExpense/maxEarnings/both)"
        )
    return problem


def _init_batchtype():
    """Prompt the user to choose the type of batch he wants to create."""

    while True:
        batchtype = _styled_prompt(
            f"Do you have one seller or multiple sellers ? [{_jaune}](one/multiple)"
        )
        if batchtype == "one":
            number_of_batches, batch_list = _bc_creation()
            return number_of_batches, batch_list
        elif batchtype == "multiple":
            number_of_batches, batch_list = _bl_creation()
            return number_of_batches, batch_list


def _number_creation(object: str):
    """Prompt the user to enter the number of batches/items he wants to create."""

    while True:
        try:
            number = int(_styled_prompt(f"\nHow many {object} do you want to create ?"))
            if number <= 0:
                raise ValueError(f"The number of {object} must be greater than 0")
            break
        except ValueError:
            _style_invalid_choice(
                f"The number of {object} must be an integer greater than 0"
            )
    return number


def _bc_creation():
    """Create a BatchCollection object."""

    _style_h2("BATCHES CREATION : BATCH COLLECTION")
    number_of_batches = _number_creation(object="batches")

    str_seller = _styled_prompt("Enter the name of the seller")
    _styled_echo(
        '\nYou can create a batch like this : "Batch name:price; quantity1xitem1, quantity2xitem2, ..."'
    )
    _styled_echo("Example : Batchname:10; 1xapple, 2xbanana")
    bc = BatchCollection(seller=str_seller)
    for numero in range(1, number_of_batches + 1):
        while True:
            try:
                str_batch = _styled_prompt(
                    f"\n[red]⠹ {round(100 * (numero) / number_of_batches, 2)}% : [/red]Enter the Batch n°{numero}"
                )
                console.print(str_batch)
                bc.add_batch(Batch.from_str(str_batch))
                break
            except ValueError:
                _style_invalid_choice(
                    "Invalid format.\nHave you entered two batches with the same name for the same seller?\nIf so, please change the name of one of the batches"
                )
                _styled_echo(
                    'You can create a batch like this : "Batch name:price; quantity1xitem1, quantity2xitem2, ..."'
                )
                _styled_echo("Example : Batchname:10; 1xapple, 2xbanana")
    _animate_progress_bar("Initialization of the problems", number_of_batches)
    return number_of_batches, bc


def _bl_creation():
    """Create a BatchLists object."""

    _style_h2("BATCHES CREATION : BATCH LISTS")
    number_of_batches = _number_creation(object="batches")
    _styled_echo(
        "\nYou can create a batch list like this : 'Seller1_BatchName:price; quantity1xitem1, quantity2xitem2, ...'"
    )
    _styled_echo("Example : Seller1_batchname:10; 1xapple, 2xbanana")

    bl = BatchLists()
    for numero in range(1, number_of_batches + 1):
        while True:
            try:
                str_batch = _styled_prompt(
                    f"\n[red]⠹ {round(100 * (numero) / number_of_batches, 2)}% : [/red]Enter the Batch n°{numero}"
                )
                seller, str_batch = str_batch.split("_")
                bl.add_BatchCollection(
                    BatchCollection.from_str(str_batch, seller=seller)
                )
                break
            except ValueError:
                _style_invalid_choice(
                    "Invalid format.\nHave you entered two batches with the same name for the same seller?\nIf so, please change the name of one of the batches"
                )
                _styled_echo(
                    "You can create a batch list like this : 'Seller1_BatchName:price; quantity1xitem1, quantity2xitem2, ...'"
                )
                _styled_echo(
                    "Example : Seller1_batchname:10; 1xapple, 2xbanana",
                )
    _animate_progress_bar("Initialization of the problems", number_of_batches)
    return number_of_batches, bl


def _item_request_creation():
    """Create an ItemListRequest object."""

    _style_h2("ITEM REQUEST CREATION")
    number_of_items = _number_creation(object="items")
    _styled_echo(
        "\nYou can create an item request like this : 'minimum quantity-maximum quantity of item name, ...'"
    )
    _styled_echo("Example : 1-10 of apple")
    ilr = ItemListRequest()
    for numero in range(1, number_of_items + 1):
        while True:
            try:
                str_items = _styled_prompt(
                    f"\n[red]⠹ {round(100 * (numero) / number_of_items, 2)}% : [/red]Enter the item n°{numero} you want to request"
                )
                ilr.add_item(ItemRequest.from_str(str_items))
                break
            except (AttributeError, ValueError):
                _style_invalid_choice(
                    "Invalid format. Please enter the items in the correct format.\nDo you enter several times the same item ?\nIf yes, please enter the item only once."
                )
                _styled_echo(
                    "You can create an item request like this : 'minimum quantity-maximum quantity of item name, ...'"
                )
                _styled_echo("Example : 1-10 of apple")
    _animate_progress_bar("Initialization of the problems", number_of_items)
    return ilr


def _transform_string_category(category: str) -> str:
    """Transform the category into a correct string form if needed."""

    if category in ["Continuous", "continuous"]:
        category = "Continuous"
    if category in ["Integer", "integer"]:
        category = "Integer"
    return category


def _init_category_of_batch_quantities(
    batch_list: BatchCollection | BatchLists,
) -> str | dict[str, str]:
    """Prompt the user to choose the category of the variables which represents the quantities of the batches."""

    batch_list_copy = _batch_transformation(batch_list)
    while True:
        choice = _styled_prompt(
            f"\nDo you want to add one category for all quantity's variables or one category for each quantity's variable ? [{_jaune}](one/all)"
        )
        if choice == "one":
            while True:
                category = _styled_prompt(
                    f"Enter the category of batch quantity's variable [{_jaune}](Continuous, Integer)"
                )
                if category not in ["Continuous", "continuous", "Integer", "integer"]:
                    _style_invalid_choice(
                        "Invalid category. Please choose between Continuous and Integer."
                    )
                else:
                    category = _transform_string_category(category)
                    return category
        elif choice == "all":
            batches_constraints = dict()
            for batch in batch_list_copy:
                while True:
                    category = _styled_prompt(
                        f"Enter the category of batch quantity's variable : {batch.name}. [{_jaune}](Continuous, Integer)"
                    )
                    if category not in [
                        "Continuous",
                        "continuous",
                        "Integer",
                        "integer",
                    ]:
                        _style_invalid_choice(
                            "Invalid category. Please choose between Continuous and Integer."
                        )
                    else:
                        category = _transform_string_category(category)
                        batches_constraints[batch.name] = category
                        break
            return batches_constraints


def _init_objective_function_constraints_prompt(
    min: str, max: str
) -> tuple[str, str, str, str]:
    """Prompt messages for the constraints of the objective function of the optimization problem."""

    if (min, max) == ("minimum expense", "maximum expense"):
        choice_prompt = "Do you have minimum expenses constraints, maximum expenses constraints or both ?"
        min_prompt = "Enter the minimum expense the customer has to spend."
        max_prompt = "Enter the maximum expense the customer can spend."
        error_prompt = "The expenses must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
    elif (min, max) == ("minimum benefit", "maximum benefit"):
        choice_prompt = "Do you have minimum benefits constraints, maximum benefits constraints or both ?"
        min_prompt = "Enter the minimum benefit the seller has to earn."
        max_prompt = "Enter the maximum benefit the seller can earn."
        error_prompt = "The benefits must be numbers.\nFurthermore, the minimum value must be less than the maximum value."

    return choice_prompt, min_prompt, max_prompt, error_prompt


def _init_objective_function_constraints(
    min: str, max: str
) -> tuple[float | None, float | None]:
    """Prompt the user to choose the expenses constraints or the benefits constraints.
    In fact, this is constraints for the objective function of the optimization problem
    """
    (
        choice_prompt,
        min_prompt,
        max_prompt,
        error_prompt,
    ) = _init_objective_function_constraints_prompt(min, max)

    while True:
        choice = _styled_prompt(f"\n{choice_prompt} [{_jaune}](min/max/both)")
        if choice in ["min", "max", "both"]:
            while True:
                try:
                    minimum = (
                        float(_styled_prompt(f"{min_prompt}"))
                        if choice in ["min", "both"]
                        else None
                    )
                    maximum = (
                        float(_styled_prompt(f"{max_prompt}"))
                        if choice in ["max", "both"]
                        else None
                    )
                    if isinstance(minimum, float) and isinstance(maximum, float):
                        if minimum > maximum:
                            raise ValueError
                    return minimum, maximum
                except ValueError:
                    _style_invalid_choice(f"{error_prompt}")
        else:
            _style_invalid_choice(
                "Invalid choice. Please choose between min, max or both"
            )


def _init_rates(rate_choice: str, number_of_batches: int) -> np.ndarray:
    """Prompt the user to enter the rates he has for the batches.
    The rates are the exchange rate, the tax rate, the custom duties and the transport fee.
    and they are applied on the prices of the batches."""

    if rate_choice == "exchange rate":
        Default = f"(Default: 1,1,....,1 or 1 for all batches) => (batch_cost x {rate_choice})"
    else:
        Default = f"(Default: 0,0,....,0 or 0 for all batches) => (batch_cost x (1+{rate_choice})"
    while True:
        invalid_choice = False
        try:
            rates = np.array(
                [
                    float(rate)
                    for rate in _styled_prompt(
                        f"\nTake the requester's point of view.\n[{_jaune}]{Default}[/{_jaune}]\nEnter the [red]{rate_choice}[/red] you have for the [red]{number_of_batches}[/red] batches"
                    ).split(",")
                ]
            )
            if not _verify_rates(rates, number_of_batches):
                raise ValueError
            rates = rates if len(rates) == number_of_batches else rates[0]

        except ValueError:
            _style_invalid_choice(
                "The rates must be numbers.\nFurthermore, the number of rates must be equal to the number of batches or equal to 1."
            )
            invalid_choice = True

        if not invalid_choice:
            return rates


def _verify_rates(rates: np.ndarray, number_of_batches: int) -> bool:
    """This function verifies if the rates entered by the user are correct."""

    if len(rates) != number_of_batches and len(rates) != 1:
        _style_invalid_choice(
            "The number of rates must be equal to the number of batches."
        )
        return False

    return True


def _batch_transformation(batch_list: BatchCollection | BatchLists):
    """Copy the batch list to avoid modifying the original one.
    Furthermore, transform the copy of the BatchLists object into a BatchCollection object.
    """

    if isinstance(batch_list, BatchLists):
        batch_list_copy = copy.deepcopy(batch_list)
        batch_list_copy_transform = _transform_batch_list(batch_list_copy)
    else:
        batch_list_copy_transform = batch_list
    return batch_list_copy_transform


def _init_batch_constraints(
    batch_list: BatchCollection | BatchLists,
) -> dict[str, tuple[float | None, float | None]] | None:
    """Prompt the user to enter the constraints he has for the quantities of the batches."""

    batch_list_copy = _batch_transformation(batch_list)
    while True:
        choice = _styled_prompt(
            f"\nDo you have minimum quantities constraints, maximum quantities constraints or both ? [{_jaune}](min/max/both)"
        )
        if choice in ["min", "max", "both"]:
            batches_constraints = dict()
            for batch in batch_list_copy:
                while True:
                    try:
                        minimum_quantity = (
                            float(
                                _styled_prompt(
                                    f"Enter the minimum quantity of the batch [red]{batch.name}"
                                )
                            )
                            if choice in ["min", "both"]
                            else None
                        )
                        maximum_quantity = (
                            float(
                                _styled_prompt(
                                    f"Enter the maximum quantity of the batch [red]{batch.name}"
                                )
                            )
                            if choice in ["max", "both"]
                            else None
                        )
                        if isinstance(minimum_quantity, float) and isinstance(
                            maximum_quantity, float
                        ):
                            if minimum_quantity > maximum_quantity:
                                raise ValueError
                        batches_constraints[batch.name] = (
                            minimum_quantity,
                            maximum_quantity,
                        )
                        break
                    except ValueError:
                        _style_invalid_choice(
                            "The quantities must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
                        )
            return batches_constraints


def _init_minBatchExpense(
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    category_of_variables: bool,
    function_constraints: bool,
    rates: bool,
    variable_constraints: bool,
):
    """Initialize the minBatchExpense function with the different parameters if needed."""

    if category_of_variables:
        _style_h2("CATEGORY OF VARIABLES")
        cat = _init_category_of_batch_quantities(batch_list)
    else:
        cat = "Continuous"

    if function_constraints:
        _style_h2("EXPENSES CONSTRAINTS")
        minimum_expense, maximum_expense = _init_objective_function_constraints(
            min="minimum expense", max="maximum expense"
        )
    else:
        minimum_expense, maximum_expense = None, None

    exchange_rate: int | float | np.ndarray = 1
    tax_rate: int | float | np.ndarray = 0
    custom_duties: int | float | np.ndarray = 0
    transport_fee: int | float | np.ndarray = 0
    if rates:
        _style_h2("RATES")
        exchange_rate, tax_rate, custom_duties, transport_fee = [
            _init_rates(rate, number_of_batches)
            for rate in ["exchange rate", "tax rate", "custom duties", "transport fee"]
        ]

    if variable_constraints:
        _style_h2("VARIABLE CONSTRAINTS")
        batch_constraints = _init_batch_constraints(batch_list)
    else:
        batch_constraints = None

    return (
        cat,
        minimum_expense,
        maximum_expense,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        batch_constraints,
    )


def _minBatchExpense_resolution(
    bc: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    cat_of_variables: str | dict[str, str] = "Continuous",
    min_expense: float | None = None,
    max_expense: float | None = None,
    exchange_rate: float | np.ndarray | int = 1,
    tax_rate: float | np.ndarray | int = 0,
    custom_duties: float | np.ndarray | int = 0,
    transport_fee: float | np.ndarray | int = 0,
    batches_constraints: dict[str, tuple[float, float | None]] | None = None,
):
    """Resolve the minBatchExpense problem."""

    result = minBatchExpense(
        batches=bc,
        demand_list=ilr,
        category_of_variables=cat_of_variables,
        minimum_expense=min_expense,
        maximum_expense=max_expense,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        customs_duty=custom_duties,
        transport_fee=transport_fee,
        batch_constraints=batches_constraints,
    )
    return format_minBatchExpense(result)


def _printed_mbe(
    lay_batch: rich.table.Table, lay_ilr: rich.table.Table, lay_mbe: rich.table.Table
):
    """Print the initialization and the resolution of the minBatchExpense problem."""

    _style_h2("INITIALIZATION OF THE BATCH EXPENDITURE MINIMIZATION PROBLEM")
    _animate_progress_bar("Initialization of the problem", total=2)
    console.print("\n", "\n")
    console.print(lay_batch, justify="center")
    console.print("\n", "\n")
    console.print(lay_ilr, justify="center")
    console.print("\n", "\n")
    _style_h2("RESOLUTION OF THE BATCH EXPENDITURE MINIMIZATION PROBLEM")
    _resolution_progress_bar("Resolution of the problem")
    console.print("\n", "\n")
    console.print(lay_mbe, justify="center")


def _init_category_of_item_prices(batch_list: BatchCollection | BatchLists):
    """Prompt the user to choose the category of the variables which represents the prices of the items."""

    batch_list_copy = _batch_transformation(batch_list)
    while True:
        choice = _styled_prompt(
            f"\nDo you want to add one category for all item price's variables or one category for each item price's variables ? [{_jaune}](one/all)"
        )
        if choice == "one":
            while True:
                category = _styled_prompt(
                    f"Enter the category of item price's variables [{_jaune}](Continuous, Integer)"
                )
                if category not in ["Continuous", "continuous", "Integer", "integer"]:
                    _style_invalid_choice(
                        "Invalid category. Please choose between Continuous and Integer."
                    )
                else:
                    category = _transform_string_category(category)
                    return category
        elif choice == "all":
            items_constraints = dict()
            all_item_already_asked = []
            for batch in batch_list_copy:
                for item in batch:
                    if item.name not in all_item_already_asked:
                        all_item_already_asked.append(item.name)
                        while True:
                            category = _styled_prompt(
                                f"Enter the category of item price's variable : [red]{item.name}[/red]. [{_jaune}](Continuous, Integer)"
                            )
                            if category not in [
                                "Continuous",
                                "continuous",
                                "Integer",
                                "integer",
                            ]:
                                _style_invalid_choice(
                                    "Invalid category. Please choose between Continuous and Integer."
                                )
                            else:
                                category = _transform_string_category(category)
                                items_constraints[item.name] = category
                                break
                    else:
                        continue
                return items_constraints


def _init_item_prices_constraints(batch_list: BatchCollection | BatchLists):
    """Prompt the user to enter the constraints he has for the prices of the items."""

    batch_list_copy = _batch_transformation(batch_list)
    seen = set()
    all_batches_item_name = []
    for batch in batch_list_copy:
        for item in batch:
            if item.name not in seen:
                seen.add(item.name)
                all_batches_item_name.append(item.name)
    while True:
        choice = _styled_prompt(
            f"\nDo you have minimum prices constraints, maximum prices constraints or both ? [{_jaune}](min/max/both)"
        )
        if choice in ["min", "max", "both"]:
            item_prices_constraints = dict()
            for item_name in all_batches_item_name:
                while True:
                    try:
                        minimum_price = (
                            float(
                                _styled_prompt(
                                    f"Enter the minimum price of the item [red]{item_name}"
                                )
                            )
                            if choice in ["min", "both"]
                            else None
                        )
                        maximum_price = (
                            float(
                                _styled_prompt(
                                    f"Enter the maximum price of the item [red]{item_name}"
                                )
                            )
                            if choice in ["max", "both"]
                            else None
                        )
                        if isinstance(minimum_price, float) and isinstance(
                            maximum_price, float
                        ):
                            if minimum_price > maximum_price:
                                raise ValueError
                        item_prices_constraints[item_name] = (
                            minimum_price,
                            maximum_price,
                        )
                        break
                    except ValueError:
                        _style_invalid_choice(
                            "The prices must be numbers.\nFurthermore, the minimum value must be less than the maximum value."
                        )
            return item_prices_constraints


def _init_maxEarnings(
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    category_of_variables: bool,
    function_constraints: bool,
    rates: bool,
    variable_constraints: bool,
):
    """Initialize the maxEarnings function with the different parameters if needed."""

    if category_of_variables:
        _style_h2("CATEGORY OF VARIABLES")
        cat = _init_category_of_item_prices(batch_list)
    else:
        cat = "Continuous"
    if function_constraints:
        _style_h2("BENEFITS CONSTRAINTS")
        minimum_benefit, maximum_benefit = _init_objective_function_constraints(
            min="minimum benefit", max="maximum benefit"
        )
    else:
        minimum_benefit, maximum_benefit = None, None

    exchange_rate: int | float | np.ndarray = 1
    tax_rate: int | float | np.ndarray = 0
    custom_duties: int | float | np.ndarray = 0
    transport_fee: int | float | np.ndarray = 0
    if rates:
        _style_h2("RATES")
        exchange_rate, tax_rate, custom_duties, transport_fee = [
            _init_rates(rate, number_of_batches)
            for rate in ["exchange rate", "tax rate", "custom duties", "transport fee"]
        ]

    if variable_constraints:
        _style_h2("VARIABLES CONSTRAINTS")
        item_prices_constraints = _init_item_prices_constraints(batch_list)
    else:
        item_prices_constraints = None

    return (
        cat,
        minimum_benefit,
        maximum_benefit,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        item_prices_constraints,
    )


def _maxEarnings_resolution(
    bc: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    cat_of_variables: str | dict[str, str] = "Continuous",
    min_benefit: float | None = None,
    max_benefit: float | None = None,
    exchange_rate: float | np.ndarray | int = 1,
    tax_rate: float | np.ndarray | int = 0,
    custom_duties: float | np.ndarray | int = 0,
    transport_fee: float | np.ndarray | int = 0,
    item_prices_constraints: dict[str, tuple[float, float | None]] | None = None,
):
    """Resolve the maxEarnings problem."""

    result = maxEarnings(
        batches=bc,
        demand_list=ilr,
        category_of_variables=cat_of_variables,
        minimum_benefit=min_benefit,
        maximum_benefit=max_benefit,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        customs_duty=custom_duties,
        transport_fee=transport_fee,
        price_constraints=item_prices_constraints,
    )
    return format_maxEarnings(result)


def _printed_me(
    lay_batch: rich.table.Table, lay_ilr: rich.table.Table, lay_me: rich.table.Table
):
    """Print the initialization and the resolution of the maxEarnings problem."""

    _style_h2("INITIALIZATION OF THE MAX EARNINGS PROBLEM")
    _animate_progress_bar("Initialization of the problem", total=2)
    console.print("\n", "\n")
    console.print(lay_batch, justify="center")
    console.print("\n", "\n")
    console.print(lay_ilr, justify="center")
    console.print("\n", "\n")
    _style_h2("RESOLUTION OF THE MAX EARNINGS PROBLEM")
    _resolution_progress_bar("Resolution of the problem")
    console.print("\n", "\n")
    console.print(lay_me, justify="center")


def _stages_progress_mbe(
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    category_of_variables: bool,
    function_constraints: bool,
    rates=bool,
    variable_constraints=bool,
):
    """Show the different stages of the minBatchExpense problem"""

    (
        cat,
        minimum_expense,
        maximum_expense,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        batches_constraints,
    ) = _init_minBatchExpense(
        number_of_batches=number_of_batches,
        batch_list=batch_list,
        category_of_variables=category_of_variables,
        function_constraints=function_constraints,
        rates=rates,
        variable_constraints=variable_constraints,
    )
    print_mbe = _minBatchExpense_resolution(
        bc=batch_list,
        ilr=ilr,
        cat_of_variables=cat,
        min_expense=minimum_expense,
        max_expense=maximum_expense,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        custom_duties=custom_duties,
        transport_fee=transport_fee,
        batches_constraints=batches_constraints,
    )

    if isinstance(batch_list, BatchCollection):
        print_batch = format_batch_collection(batch_list)
    elif isinstance(batch_list, BatchLists):
        print_batch = format_batch_lists(batch_list)

    print_ilr = format_itemlistRequest(ilr)

    return _printed_mbe(lay_batch=print_batch, lay_ilr=print_ilr, lay_mbe=print_mbe)


def _stages_progress_me(
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    category_of_variables: bool,
    function_constraints: bool,
    rates=bool,
    variable_constraints=bool,
):
    """Show the different stages of the maxEarnings problem"""

    (
        cat,
        minimum_benefit,
        maximum_benefit,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        item_prices_constraints,
    ) = _init_maxEarnings(
        number_of_batches=number_of_batches,
        batch_list=batch_list,
        category_of_variables=category_of_variables,
        function_constraints=function_constraints,
        rates=rates,
        variable_constraints=variable_constraints,
    )
    print_me = _maxEarnings_resolution(
        bc=batch_list,
        ilr=ilr,
        cat_of_variables=cat,
        min_benefit=minimum_benefit,
        max_benefit=maximum_benefit,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        custom_duties=custom_duties,
        transport_fee=transport_fee,
        item_prices_constraints=item_prices_constraints,
    )

    if isinstance(batch_list, BatchCollection):
        print_batch = format_batch_collection(batch_list)
    elif isinstance(batch_list, BatchLists):
        print_batch = format_batch_lists(batch_list)

    print_ilr = format_itemlistRequest(ilr)

    return _printed_me(lay_batch=print_batch, lay_ilr=print_ilr, lay_me=print_me)


def _printed_both(
    lay_batch: rich.table.Table,
    lay_ilr: rich.table.Table,
    lay_mbe: rich.table.Table,
    lay_me: rich.table.Table,
):
    """Print the initialization and the resolution of both problems."""

    _style_h2("INITIALIZATION OF THE MIN BATCH EXPENSE AND MAX EARNINGS PROBLEMS")
    _animate_progress_bar("Initialization of the problems", total=4)
    console.print("\n", "\n")
    console.print(lay_batch, justify="center")
    console.print("\n", "\n")
    console.print(lay_ilr, justify="center")
    console.print("\n", "\n")
    _style_h2("RESOLUTION OF THE MIN BATCH EXPENSE AND MAX EARNINGS PROBLEMS")
    _resolution_progress_bar("Resolution of the problems")
    console.print("\n", "\n")
    layout_object = Layout()
    layout_object.split_row(
        Layout(lay_mbe),
        Layout(lay_me),
    )
    console.print(layout_object)


def _stages_progress_both(
    number_of_batches: int,
    batch_list: BatchCollection | BatchLists,
    ilr: ItemListRequest,
    category_of_variables: bool,
    function_constraints: bool,
    rates=bool,
    variable_constraints=bool,
):
    """Show the different stages of the minBatchExpense and maxEarnings problems"""

    (
        cat,
        minimum_expense,
        maximum_expense,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        batches_constraints,
    ) = _init_minBatchExpense(
        number_of_batches=number_of_batches,
        batch_list=batch_list,
        category_of_variables=category_of_variables,
        function_constraints=function_constraints,
        rates=rates,
        variable_constraints=variable_constraints,
    )
    print_mbe = _minBatchExpense_resolution(
        bc=batch_list,
        ilr=ilr,
        cat_of_variables=cat,
        min_expense=minimum_expense,
        max_expense=maximum_expense,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        custom_duties=custom_duties,
        transport_fee=transport_fee,
        batches_constraints=batches_constraints,
    )

    (
        cat,
        minimum_benefit,
        maximum_benefit,
        exchange_rate,
        tax_rate,
        custom_duties,
        transport_fee,
        item_prices_constraints,
    ) = _init_maxEarnings(
        number_of_batches=number_of_batches,
        batch_list=batch_list,
        category_of_variables=category_of_variables,
        function_constraints=function_constraints,
        rates=False,
        variable_constraints=variable_constraints,
    )

    print_me = _maxEarnings_resolution(
        bc=batch_list,
        ilr=ilr,
        cat_of_variables=cat,
        min_benefit=minimum_benefit,
        max_benefit=maximum_benefit,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        custom_duties=custom_duties,
        transport_fee=transport_fee,
        item_prices_constraints=item_prices_constraints,
    )

    if isinstance(batch_list, BatchCollection):
        print_batch = format_batch_collection(batch_list)
    elif isinstance(batch_list, BatchLists):
        print_batch = format_batch_lists(batch_list)

    print_ilr = format_itemlistRequest(ilr)

    return _printed_both(
        lay_batch=print_batch, lay_ilr=print_ilr, lay_mbe=print_mbe, lay_me=print_me
    )


def _verify_valid_ilr(
    ilr: ItemListRequest, batch_list: BatchCollection | BatchLists
) -> bool:
    """This function verifies if the items requested by the user are available in the batches."""

    batch_list_copy = _batch_transformation(batch_list)
    all_batches_item_name = {item.name for batch in batch_list_copy for item in batch}
    all_ilr_item_name = {item.name for item in ilr}
    if not all_ilr_item_name.issubset(all_batches_item_name):
        return False
    return True
