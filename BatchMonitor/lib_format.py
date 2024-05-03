"""Description.

lib_format have to be used with lib_batches, lib_item_request or lib_optimization modules.

- He allows to format the objects of the batches_optimization project to be printed in the console.
- You can format a BatchCollection object, a BatchLists object, an ItemListRequest object, the result of the minBatchExpense function or the result of the maxEarnings function.

You can import with the following command:

    import lib_format as lf

Developed by :
    - [Hugo Cochereau](https://github.com/hugocoche)
    - [Gregory Jaillet](https://github.com/Greg-jllt)
"""

import os
import sys
import warnings
from rich.table import Table
from rich.text import Text
from .lib_batches import BatchCollection, BatchLists
from .lib_item_request import ItemListRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

warnings.filterwarnings(
    "ignore",
    "Some batches contain weapons not present in other batches. They have been added with a quantity of 0.",
)
warnings.filterwarnings(
    "ignore", "Spaces are not permitted in the name. Converted to '_'"
)
warnings.filterwarnings(
    "ignore", "The name .* has illegal characters that will be replaced by _"
)


def format_batch_collection(bc: BatchCollection) -> Table:
    """Format a BatchCollection object to be printed in the console.

    Args:
        bc (BatchCollection): the BatchCollection object to be formatted.

    Returns:
        str: the formatted string.
    """
    table = Table(
        title=f"The batches sold by {bc.seller}\n",
        expand=True,
        highlight=True,
        header_style="magenta",
    )
    table.add_column(
        "Batch",
        justify="center",
        style="black",
    )
    table.add_column("Price", justify="center")
    table.add_column("Items")
    for batch in bc:
        items_str = "\n".join(
            f"{int(item.quantity_in_batch)} {item.name}"
            for item in batch.items
            if item.quantity_in_batch > 0
        )
        table.add_row(
            Text(batch.name, style="on white"),
            str((batch.price)),
            items_str,
            end_section=True,
        )
    return table


def format_batch_lists(bl: BatchLists) -> Table:
    """Format a BatchLists object to be printed in the console.

    Args:
        bl (BatchLists): the BatchLists object to be formatted.

    Returns:
        str: the formatted string.
    """
    table = Table(
        title="The batches sold by each seller\n",
        header_style="magenta",
        expand=True,
        highlight=True,
    )
    table.add_column("Seller", justify="center")
    table.add_column("Batch", justify="center", style="black")
    table.add_column("Price", justify="center")
    table.add_column("Items")
    for bc in bl:
        table.add_row(
            Text(bc.seller, style="red"),
        )
        batches = list(bc)
        for i, batch in enumerate(batches):
            items_str = "\n".join(
                f"{int(item.quantity_in_batch)} {item.name}"
                for item in batch.items
                if item.quantity_in_batch > 0
            )
            end_section = i == len(batches) - 1
            table.add_row(
                "",
                Text(batch.name, style="on white"),
                str((batch.price)),
                f"{items_str}\n\n",
                end_section=end_section,
            )
    return table


def format_itemlistRequest(ilr: ItemListRequest) -> Table:
    """Format an ItemListRequest object to be printed in the console.

    Args:
        ilr (ItemListRequest): the ItemListRequest object to be formatted.

    Returns:
        str: the formatted string.
    """
    table = Table(
        title="The items requested by the customer\n",
        expand=True,
        highlight=True,
        header_style="magenta",
    )
    table.add_column("Item", justify="center", style="on white")
    table.add_column("Minimum Quantity", justify="center")
    table.add_column("Maximum Quantity", justify="center")
    for item in ilr:
        table.add_row(
            Text(item.name, style="black"),
            str(item.minimum_quantity),
            Text(str(item.maximum_quantity), style="white"),
            end_section=True,
        )
    return table


def format_minBatchExpense(minBatchExpense: dict) -> Table | str:
    """Format the result of the minBatchExpense function to be printed in the console.

    Args:
        minBatchExpense (dict): the result of the minBatchExpense function.

    Returns:
        str: the formatted string.
    """

    if minBatchExpense["Status"] == "Infeasible":
        return "The problem is infeasible."
    else:
        str_batch_quantities = "\n".join(
            f"[red]{batch[0]} :[/red] {batch[1]}"
            for batch in minBatchExpense["Batch quantities"].items()
        )
        if "Expense per seller" in minBatchExpense.keys():
            str_expense_per_seller = "\n".join(
                f"[red]{seller[0]} :[/red] {seller[1]}"
                for seller in minBatchExpense["Expense per seller"].items()
            )
        table = Table(
            title="Results of the batch expenditure minimization problem",
            show_header=False,
            expand=True,
            highlight=True,
        )
        table.add_column("Result of the problem", justify="center", style="magenta")
        table.add_column("Value")
        for result in minBatchExpense.items():
            if result[0] == "Batch quantities":
                table.add_row(
                    "Batch quantities", str_batch_quantities, end_section=True
                )
            elif result[0] == "Expense per seller":
                table.add_row(
                    "Expense per seller", str_expense_per_seller, end_section=True
                )
            else:
                table.add_row(result[0], str(result[1]), end_section=True)
        return table


def format_maxEarnings(maxEarnings: dict) -> Table | str:
    """Format the result of the maxEarnings function to be printed in the console.

    Args:
        maxEarnings (dict): the result of the maxEarnings function.

    Returns:
        str: the formatted string.
    """
    if maxEarnings["Status"] == "Infeasible":
        return "The problem is infeasible."
    else:
        str_item_price = "\n".join(
            f"[red]{item[0]} :[/red] {item[1]}"
            for item in maxEarnings["Item prices"].items()
        )
    table = Table(
        title="Results of the earnings maximization problem",
        show_header=False,
        expand=True,
        highlight=True,
    )
    table.add_column("Result of the problem", justify="center", style="magenta")
    table.add_column("Value")
    for result in maxEarnings.items():
        if result[0] == "Item prices":
            table.add_row("Item prices", str_item_price, end_section=True)
        else:
            table.add_row(result[0], str(result[1]), end_section=True)
    return table
