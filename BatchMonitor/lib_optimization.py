"""Description:

This file contains the optimization functions of the package
Use the pulp library to optimize the batches problem

You can resolve the Batch expenditure minimization problem with the minBatchExpense function
You can resolve the Earnings maximization problem with the maxEarnings function.
You can fix the minimum and maximum expense with the minBatchExpense function
You can fix the minimum and maximum benefit with the maxEarnings function
You can fix the category of the variables with the minBatchExpense and maxEarnings functions
You can fix the constraints of the batches with the minBatchExpense function
You can fix the constraints of the prices with the maxEarnings function
You can fix the exchange rate, tax rate, customs duty, and transport fee with the minBatchExpense or maxEarnings functions

Limits :
- We suppose that we have a unique requester for the minBatchExpense function
- The rates are applied to the price of the batch

You can import this module with the following command:
    import lib_optimization as opt

Developed by :
    - [Hugo Cochereau](https://github.com/hugocoche)
    - Gregory Jaillet
"""

import copy
import os
import sys

import numpy as np
import pulp as pulp

from .lib_batches import Batch, BatchCollection, BatchLists
from .lib_item_request import ItemListRequest, ItemRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def _transform_batch_list(liste_of_batches: BatchLists) -> BatchCollection:
    """Transform a BatchLists object into a BatchCollection object.
    We also add the name of the seller to the name of the batch."""

    for batches in liste_of_batches:
        for batch in batches:
            batch.name = f"{batches.seller}_{batch.name}"

    batch_collection = [batch for batches in liste_of_batches for batch in batches]

    return BatchCollection(batch_list=batch_collection)


def _generate_variables_primal(
    batches: BatchCollection,
    cat: dict[str, str] | str = "Continuous",
    batch_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> dict[str, pulp.LpVariable]:
    """Generate the variables of the primal problem."""

    if batch_constraints is None:
        batch_constraints = {}

    variables = {
        batch.name: pulp.LpVariable(
            batch.name,
            lowBound=batch_constraints.get(batch.name, (0, None))[0],
            upBound=batch_constraints.get(batch.name, (0, None))[1],
            cat=cat.get(batch.name, cat) if isinstance(cat, dict) else cat,
        )
        for batch in batches
    }

    return variables


def _generate_primal_objective_function(
    variables: dict[str, pulp.LpVariable], batches: BatchCollection
) -> pulp.LpProblem:
    """Generate the objective function of the primal problem."""

    prob = pulp.LpProblem("Primal problem", pulp.LpMinimize)
    prob += pulp.lpSum([batch.price * variables[batch.name] for batch in batches])

    return prob.objective


def _missing_ItemRequest(
    batches: BatchCollection, demand_list: ItemListRequest
) -> bool:
    """Check if an item in the demand list is not in the Batch_list."""

    return any(
        all(
            request_item.name not in [item.name for item in batch.items]
            for batch in batches
        )
        for request_item in demand_list
    )


def _addition_of_unrequested_item(
    batches: BatchCollection, demand_list: ItemListRequest
) -> ItemListRequest:
    """Add the items not requested in the demand list."""

    All_items_in_batch = {item.name for batch in batches for item in batch}
    items_requested = {item.name for item in demand_list}
    for item in All_items_in_batch:
        if item not in items_requested:
            demand_list.items.append(ItemRequest(item, 0))
    return demand_list


def _exchange_rate(
    batches: BatchCollection, rate: float | np.ndarray
) -> BatchCollection:
    """Apply an exchange rate to the prices of the batches."""

    if isinstance(rate, np.ndarray):
        for i, batch in enumerate(batches):
            batch.price *= rate[i]
    else:
        for batch in batches:
            batch.price *= rate

    return batches


def _taxe_rate(batches: BatchCollection, rate: float | np.ndarray) -> BatchCollection:
    """Apply a tax rate to the prices of the batches."""

    if isinstance(rate, np.ndarray):
        for i, batch in enumerate(batches):
            batch.price *= 1 + rate[i]
    else:
        for batch in batches:
            batch.price *= 1 + rate

    return batches


def _customs_duty(
    batches: BatchCollection, rate: float | np.ndarray
) -> BatchCollection:
    """Apply customs duties to the prices of the batches."""

    if isinstance(rate, np.ndarray):
        for i, batch in enumerate(batches):
            batch.price *= 1 + rate[i]
    else:
        for batch in batches:
            batch.price *= 1 + rate

    return batches


def _transport_fee(
    batches: BatchCollection, rate: float | np.ndarray
) -> BatchCollection:
    """Apply transport fees to the prices of the batches."""

    if isinstance(rate, np.ndarray):
        for i, batch in enumerate(batches):
            batch.price *= 1 + rate[i]
    else:
        for batch in batches:
            batch.price *= 1 + rate

    return batches


def _apply_rates(
    batches: BatchCollection,
    exchange_rate: float | np.ndarray,
    tax_rate: float | np.ndarray,
    customs_duty: float | np.ndarray,
    transport_fee: float | np.ndarray,
) -> BatchCollection:
    """Apply the rates to the prices of the batches."""

    batches = _transport_fee(batches, transport_fee)
    batches = _exchange_rate(batches, exchange_rate)
    batches = _taxe_rate(batches, tax_rate)
    batches = _customs_duty(batches, customs_duty)

    return batches


def _prepare_the_problem(
    batches: BatchCollection | BatchLists,
    demand_list: ItemListRequest,
    exchange_rate: float | np.ndarray = 1,
    tax_rate: float | np.ndarray = 0,
    customs_duty: float | np.ndarray = 0,
    transport_fee: float | np.ndarray = 0,
) -> BatchCollection:
    """Prepare the batch list for the optimization."""

    if isinstance(batches, BatchLists):
        batches = _transform_batch_list(batches)
    demand_list = _addition_of_unrequested_item(batches, demand_list)
    if _missing_ItemRequest(batches, demand_list):
        raise ValueError("An item requested is not contained in any batch.")
    batches = _apply_rates(
        batches, exchange_rate, tax_rate, customs_duty, transport_fee
    )

    return batches


def _minimum_expense(
    batches: BatchCollection,
    variables: dict[str, pulp.LpVariable],
    minimum_expense: float,
) -> pulp.LpProblem:
    """Add a constraint to the primal problem to set a minimum expense."""

    return (
        pulp.lpSum([batch.price * variables[batch.name] for batch in batches])
        >= minimum_expense
    )


def _maximum_expense(
    batches: BatchCollection,
    variables: dict[str, pulp.LpVariable],
    maximum_expense: float,
) -> pulp.LpProblem:
    """Add a constraint to the primal problem to set a maximum expense."""

    return (
        pulp.lpSum([batch.price * variables[batch.name] for batch in batches])
        <= maximum_expense
    )


def _apply_expense_constraints(
    batches: BatchCollection,
    variables: dict[str, pulp.LpVariable],
    constraints: pulp.LpProblem,
    minimum_expense: float | None,
    maximum_expense: float | None,
) -> pulp.LpProblem:
    """Apply the expense constraints to the primal problem."""

    if minimum_expense is not None and maximum_expense is not None:
        if maximum_expense < minimum_expense:
            raise ValueError("maximum_expense cannot be less than minimum_expense")

    if minimum_expense is not None:
        constraints += _minimum_expense(batches, variables, minimum_expense)
    if maximum_expense is not None:
        constraints += _maximum_expense(batches, variables, maximum_expense)

    return constraints


def _generate_primal_constraints(
    variables: dict[str, pulp.LpVariable],
    batches: BatchCollection,
    demand_list: ItemListRequest,
    maximum_expense: float | None = None,
    minimum_expense: float | None = None,
) -> pulp.LpProblem:
    """Generate the constraints of the primal problem."""

    prob = pulp.LpProblem("Primal problem", pulp.LpMinimize)
    for item_request in demand_list:
        prob += (
            pulp.lpSum(
                [
                    item.quantity_in_batch * variables[batch.name]
                    for batch in batches
                    for item in batch
                    if item.name == item_request.name
                ]
            )
            >= item_request.minimum_quantity
        )
        if item_request.maximum_quantity:
            prob += (
                pulp.lpSum(
                    [
                        item.quantity_in_batch * variables[batch.name]
                        for batch in batches
                        for item in batch
                        if item.name == item_request.name
                    ]
                )
                <= item_request.maximum_quantity
            )
    prob = _apply_expense_constraints(
        batches=batches,
        variables=variables,
        constraints=prob,
        minimum_expense=minimum_expense,
        maximum_expense=maximum_expense,
    )

    return prob.constraints


def _collecte_data_primal(
    batches: BatchCollection,
    demand_list: ItemListRequest,
    cat: dict[str, str] | str = "Continuous",
    maximum_expense: float | None = None,
    minimum_expense: float | None = None,
    batch_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> tuple:
    """Collect the data for the primal problem."""

    variables = _generate_variables_primal(
        batches=batches, cat=cat, batch_constraints=batch_constraints
    )
    objective = _generate_primal_objective_function(variables, batches)
    constraints = _generate_primal_constraints(
        variables=variables,
        batches=batches,
        demand_list=demand_list,
        minimum_expense=minimum_expense,
        maximum_expense=maximum_expense,
    )

    return variables, objective, constraints


def _expense_per_each_seller(
    batches: BatchCollection,
    x: dict[str, float],
) -> dict[str, float]:
    """Calculate the expense per each seller"""

    expense_per_seller: dict[str, float] = {}
    for key, value, price in zip(
        x.keys(), x.values(), [batch.price for batch in batches]
    ):
        seller = key.split("_")[0]
        if seller in expense_per_seller:
            expense_per_seller[seller] += price * value
        else:
            expense_per_seller[seller] = price * value

    return expense_per_seller


def minBatchExpense(
    batches: BatchCollection | BatchLists,
    demand_list: ItemListRequest,
    category_of_variables: dict[str, str] | str = "Continuous",
    exchange_rate: float | np.ndarray | int = 1,
    tax_rate: float | np.ndarray | int = 0,
    customs_duty: float | np.ndarray | int = 0,
    transport_fee: float | np.ndarray | int = 0,
    minimum_expense: float | None = None,
    maximum_expense: float | None = None,
    batch_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> dict:
    """Generate the primal problem to minimize the expense of the requester of the batches.
    The objective function is the sum of the price of each batch multiplied by the quantity of the batch.
    The constraints are the quantities of the items requested.
    The variables are the quantities of the batches.

    Args:
    - batches: BatchCollection | BatchLists: The list of batches to optimize.

    You can specify the list of batches in the form of a BatchCollection or a BatchLists.


    - demand_list: ItemListRequest: The list of items requested.

    You can specify the list of items requested in the form of an ItemListRequest.

    - category_of_variables: dict[str, str] | str: The category of the variables.

    You can specify a category (Contnuous or Integer) for each bach.

    - exchange_rate: float | np.ndarray: The exchange rate.

    You can specify a different exchange rate for each batch in the form of an np.array([]).

    Attention: The exchange rate is applied to the price of the batch. So the final money will be in the currency of the requester.


    - tax_rate: float | np.ndarray: The tax rate.

    You can specify a different tax rate for each batch in the form of an np.array([]).

    - customs_duty: float | np.ndarray: The customs duty.

    You can specify a different customs duty for each batch in the form of an np.array([]).


    - transport_fee: float | np.ndarray: The transport fee.

    You can specify a different transport fee for each batch in the form of an np.array([]).

    The different rates are applied to the price of the batch in the following order:
    - transport_fee
    - exchange_rate
    - tax_rate
    - customs_duty

    - minimum_expense: float: The minimum expense the requester is willing to pay.

    - maximum_expense: float: The maximum expense the requester is willing to pay.

    - batch_constraints: dict: The constraints of the batches.

    You can specify a different constraint for each batch in the form of a dict('batch_name' = (minimum_quantity, maximum_quantity)).


    Returns:

    dict: The result of the optimization.


    Examples:

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> item_request = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...         ]
    ...     )
    The variable will be the quantity of each batch.
    batch1, batch2, batch3

    The objective function will be :
    10 * batch1 + 12 * batch2 + 15 * batch3

    The constraints will be :
    500 * batch1 + 300 * batch2 + 800 * batch3 >= 100000
    1000 * batch1 + 2000 * batch2 + 1500 * batch3 >= 200000
    10 * batch1 + 20 * batch2 + 15 * batch3 >= 100
    100 * batch1 + 80 * batch2 + 15 * batch3 >= 400
    80 * batch1 + 120 * batch2 + 200 * batch3 >= 400



    Examples:

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> item_request = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...         ]
    ...     )
    >>> minBatchExpense(batch, item_request)
    {'Status': 'Optimal', 'Total cost': 1930.4347764000001, 'Batch quantities': {'batch1': 0.0, 'batch2': 8.6956522, 'batch3': 121.73913}}

    an ultimate example:

    >>> batches = BatchCollection(
    ...     seller="type",
    ...     batch_list=[
    ...         Batch.from_str("lot1:10; 1xarme 1, 2xarme 2, 3xarme 3"),
    ...         Batch.from_str("lot2:20; 2xarme 1, 3xarme 2")
    ...     ]
    ... )
    >>>
    >>> items = ItemListRequest([ItemRequest("arme 1", 3,6), ItemRequest("arme 2", 6,9)])
    >>> result = minBatchExpense(
    ...     batches,
    ...     items,
    ...     category_of_variables="Continuous",
    ...     exchange_rate=0.9,
    ...     transport_fee=np.array([0.3, 0.1, 0.4]),
    ...     tax_rate=np.array([0.2, 0.1, 0.3]),
    ...     customs_duty=0.2,
    ...     batch_constraints=dict(
    ...         lot1= (0, 50),
    ...         lot2= (0, 1000),
    ...         lot3= (0, 100)),
    ...     minimum_expense=60,
    ...     maximum_expense = 100
    ...     )
    >>> result
    {'Status': 'Optimal', 'Total cost': 59.9999996376, 'Batch quantities': {'lot1': 0.0, 'lot2': 2.2956841}}

    Attention: The function will raise a ValueError if an item requested is not contained in any batch.

    Example :

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> item_request = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...             ItemRequest("cherries", 100),
    ...         ]
    ...     )
    >>> minBatchExpense(batch, item_request)
    Traceback (most recent call last):
    ...
    ValueError: An item requested is not contained in any batch.

    Attention: The function will raise a ValueError if the maximum_expense is less than the minimum_expense.

    Example :

    >>> minBatchExpense(
    ...     batch,
    ...     item_request,
    ...     category_of_variables="Continuous",
    ...     exchange_rate=0.9,
    ...     transport_fee=np.array([0.3, 0.1, 0.4]),
    ...     tax_rate=np.array([0.2, 0.1, 0.3]),
    ...     customs_duty=0.5,
    ...     batch_constraints=dict(
    ...         lot1= (0, 50),
    ...         lot2= (0, 1000),
    ...         lot3= (0, 100)),
    ...     maximum_expense=1000,
    ...     minimum_expense=100000
    ...     )
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
            variables, objective, constraints = _collecte_data_primal(
                                                ^^^^^^^^^^^^^^^^^^^^^^
            constraints = _generate_primal_constraints(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            prob = _apply_expense_constraints(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
            raise ValueError("maximum_expense cannot be less than minimum_expense")
        ValueError: maximum_expense cannot be less than minimum_expense

    Attention: The function is not able to solve the problem if it is infeasible.

    >>> minBatchExpense(
        batch,
        ItemListRequest([ItemRequest("apple", 1000000), ItemRequest("banana", 2000000)]),
        maximum_expense=1000
    )
    {'Status': 'Infeasible'}
    """

    batches_copy = copy.deepcopy(batches)
    demand_list_copy = copy.deepcopy(demand_list)

    batches_copy = _prepare_the_problem(
        batches=batches_copy,
        demand_list=demand_list_copy,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        customs_duty=customs_duty,
        transport_fee=transport_fee,
    )

    variables, objective, constraints = _collecte_data_primal(
        batches=batches_copy,
        demand_list=demand_list_copy,
        cat=category_of_variables,
        maximum_expense=maximum_expense,
        minimum_expense=minimum_expense,
        batch_constraints=batch_constraints,
    )

    prob = pulp.LpProblem("Primal problem", pulp.LpMinimize)
    prob += objective
    for constraint in constraints.values():
        prob += constraint
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    return _return_minBatchExpense(
        batches=batches, batches_copy=batches_copy, variables=variables, prob=prob
    )


def _return_minBatchExpense(
    batches: BatchCollection | BatchLists,
    batches_copy: BatchCollection,
    variables: pulp.LpVariable,
    prob: pulp.LpProblem,
) -> dict[str, str | float | int | dict[str, float | int]] | dict[str, str]:
    """Returns of the minBatchExpense function"""

    x = {
        batch.name: pulp.value(variables[batch.name])
        for batch in batches_copy
        if isinstance(batch, Batch)
    }
    if pulp.LpStatus[prob.status] == "Infeasible":
        return {"Status": pulp.LpStatus[prob.status]}
    elif isinstance(batches, BatchLists) and isinstance(batches_copy, BatchCollection):
        return {
            "Status": pulp.LpStatus[prob.status],
            "Total cost": pulp.value(prob.objective),
            "Batch quantities": x,
            "Expense per seller": _expense_per_each_seller(batches_copy, x),
        }
    else:
        # raise ValueError(f"batches is the type {type(batches_copy)}")
        return {
            "Status": pulp.LpStatus[prob.status],
            "Total cost": pulp.value(prob.objective),
            "Batch quantities": x,
        }


def _generate_variable_dual(
    demand_list: ItemListRequest,
    cat: dict[str, str] | str = "Continuous",
    price_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> dict[str, pulp.LpVariable]:
    """Generate the variables of the dual problem."""

    if price_constraints is None:
        price_constraints = {}

    variables = {
        item_request.name: pulp.LpVariable(
            item_request.name,
            lowBound=price_constraints.get(item_request.name, (0, None))[0],
            upBound=price_constraints.get(item_request.name, (0, None))[1],
            cat=cat,
        )
        for item_request in demand_list.items
    }

    return variables


def _generate_dual_objective_function(
    variables: dict[str, pulp.LpVariable], demand_list: ItemListRequest
) -> pulp.LpProblem:
    """Generate the objective function of the dual problem."""

    prob = pulp.LpProblem("Dual problem", pulp.LpMaximize)
    prob += pulp.lpSum(
        [
            item_request.minimum_quantity * variables[item_request.name]
            for item_request in demand_list
        ]
    )

    return prob.objective


def _maximum_benefit(
    demand_list: ItemListRequest,
    variables: dict[str, pulp.LpVariable],
    maximum_benefit: float | None,
) -> pulp.LpProblem:
    """Add a constraint to the dual problem to set a maximum benefit."""

    return (
        pulp.lpSum(
            [
                item_request.minimum_quantity * variables[item_request.name]
                for item_request in demand_list
            ]
        )
        <= maximum_benefit
    )


def _minimum_benefit(
    demand_list: ItemListRequest,
    variables: dict[str, pulp.LpVariable],
    minimum_benefit: float | None,
) -> pulp.LpProblem:
    """Add a constraint to the dual problem to set a minimum benefit."""

    return (
        pulp.lpSum(
            [
                item_request.minimum_quantity * variables[item_request.name]
                for item_request in demand_list
            ]
        )
        >= minimum_benefit
    )


def _apply_benefit_constraints(
    demand_list: ItemListRequest,
    variables: dict[str, pulp.LpVariable],
    constraints: pulp.LpProblem,
    minimum_benefit: float | None,
    maximum_benefit: float | None,
) -> pulp.LpProblem:
    """Apply the benefit constraints to the dual problem."""

    if minimum_benefit is not None and maximum_benefit is not None:
        if maximum_benefit < minimum_benefit:
            raise ValueError("maximum_benefit cannot be less than minimum_benefit")

    if minimum_benefit is not None:
        constraints += _minimum_benefit(demand_list, variables, minimum_benefit)
    if maximum_benefit is not None:
        constraints += _maximum_benefit(demand_list, variables, maximum_benefit)

    return constraints


def _generate_dual_constraints(
    variables: dict[str, pulp.LpVariable],
    batch_list: BatchCollection,
    demand_list: ItemListRequest,
    minimum_benefit: float | None = None,
    maximum_benefit: float | None = None,
) -> pulp.LpProblem:
    """Generate the constraints of the dual problem."""

    prob = pulp.LpProblem("Dual problem", pulp.LpMaximize)
    for batch in batch_list:
        prob += (
            pulp.lpSum(
                [item.quantity_in_batch * variables[item.name] for item in batch]
            )
            <= batch.price
        )
    prob = _apply_benefit_constraints(
        demand_list=demand_list,
        variables=variables,
        constraints=prob,
        minimum_benefit=minimum_benefit,
        maximum_benefit=maximum_benefit,
    )

    return prob.constraints


def _collecte_data_dual(
    batches: BatchCollection,
    demand_list: ItemListRequest,
    cat: dict[str, str] | str = "Continuous",
    maximum_benefit: float | None = None,
    minimum_benefit: float | None = None,
    price_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> tuple:
    variables = _generate_variable_dual(
        demand_list=demand_list,
        cat=cat,
        price_constraints=price_constraints,
    )

    objective = _generate_dual_objective_function(variables, demand_list)
    constraints = _generate_dual_constraints(
        variables=variables,
        batch_list=batches,
        demand_list=demand_list,
        minimum_benefit=minimum_benefit,
        maximum_benefit=maximum_benefit,
    )

    return variables, objective, constraints


def maxEarnings(
    batches: BatchCollection | BatchLists,
    demand_list: ItemListRequest,
    category_of_variables: dict[str, str] | str = "Continuous",
    exchange_rate: float | np.ndarray | int = 1,
    tax_rate: float | np.ndarray | int = 0,
    customs_duty: float | np.ndarray | int = 0,
    transport_fee: float | np.ndarray | int = 0,
    minimum_benefit: float | None = None,
    maximum_benefit: float | None = None,
    price_constraints: dict[str, tuple[float, float | None]] | None = None,
) -> dict:
    """Generate the dual problem to maximize the earnings of the seller.
    The objective function is the sum of the minimum quantity of each item multiplied by the price of the item.
    The constraints are the prices of the batches.
    The variables are the prices of the items.

    Args:

    - batches: BatchCollection | BatchLists: The list of batches to optimize.

    You can specify the list of batches in the form of a BatchCollection or a BatchLists.


    - demand_list: ItemListRequest: The list of items requested.

    You can specify the list of items requested in the form of an ItemListRequest.


    - category_of_variables: dict[str, str] | str: The category of the variables.

    You can specify a category (Contnuous or Integer) for each bach.

    - exchange_rate: float | np.ndarray: The exchange rate.

    You can specify a different exchange rate for each batch in the form of an np.array([]).

    Attention , the final money will be in the currency of the requester.


    - tax_rate: float | np.ndarray: The tax rate.

    You can specify a different tax rate for each batch in the form of an np.array([]).


    - customs_duty: float | np.ndarray: The customs duty.

    You can specify a different customs duty for each batch in the form of an np.array([]).


    - transport_fee: float | np.ndarray: The transport fee.

    You can specify a different transport fee for each batch in the form of an np.array([]).

    the different rates are applied to the price of the batch in the following order:
    - transport_fee
    - exchange_rate
    - tax_rate
    - customs_duty

    - minimum_benefit: float: The minimum benefit the seller is willing to earn.

    - maximum_benefit: float: The maximum benefit the seller is willing to earn.


    - price_constraints: dict: The constraints of the prices.

    You can specify a different constraint for each item in the form of a dict('item_name' = (minimum_price, maximum_price)).


    Returns:

    dict: The result of the optimization.

    Examples:

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> items = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...         ]
    ...     )

    The variable will be the price of each item.
    apple, banana, orange, date, strawberry

    The objective function will be :
    100000 * apple + 200000 * banana + 100 * orange + 400 * date + 400 * strawberry

    The constraints will be :
    500 * apple + 1000 * banana + 10 * orange + 100 * date + 80 * strawberry <= 10
    300 * apple + 2000 * banana + 20 * orange + 80 * date + 120 * strawberry <= 12
    800 * apple + 1500 * banana + 15 * orange + 15 * date + 200 * strawberry <= 15


    Examples:

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> items = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...         ]
    ...     )
    >>> result = maxEarnings(batch, items)
    >>> result
    {'Status': 'Optimal', 'Total benefit': 1930.43482, 'Item prices': {'apple': 0.010434783, 'banana': 0.0044347826, 'orange': 0.0, 'date': 0.0, 'strawberry': 0.0}}

    an ultimate example:

    >>> batch = BatchCollection(
    ...         [
    ...             Batch.from_str(
    ...                 "batch1:10000000; 500xapple, 1000xbanana, 10xorange, 100xdate, 80xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch2:12000000; 300xapple, 2000xbanana, 20xorange, 80xdate, 120xstrawberry"
    ...             ),
    ...             Batch.from_str(
    ...                 "batch3:15000000; 800xapple, 1500xbanana, 15xorange, 15xdate, 200xstrawberry"
    ...             ),
    ...         ]
    ...     )
    >>> items = ItemListRequest(
    ...         [
    ...             ItemRequest("apple", 100000),
    ...             ItemRequest("banana", 200000),
    ...             ItemRequest("orange", 100),
    ...             ItemRequest("date", 400),
    ...             ItemRequest("strawberry", 400),
    ...         ]
    ...     )
    >>> result = maxEarnings(
    ...         batches=batch,
    ...         demand_list=items,
    ...         minimum_benefit=10405200,
    ...         maximum_benefit=1330405200,
    ...         price_constraints={
    ...             "apple": (100, 300),
    ...             "banana": (50, 100),
    ...             "orange": (10000, 20000),
    ...             "date": (5000, 10000),
    ...             "strawberry": (100, 300),
    ...         },
    ...         category_of_variables="Integer",
    ...         exchange_rate=1.2,
    ...         transport_fee=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
    ...         tax_rate=0.1,
    ...         customs_duty=0.2,
    ...     )
    >>> result
    {'Status': 'Optimal', 'Total benefit': 56120000.0, 'Item prices': {'apple': 300.0, 'banana': 100.0, 'orange': 20000.0, 'date': 10000.0, 'strawberry': 300.0}}

    Attention: The function is not able to solve the problem if it is infeasible.

    >>> maxEarnings(
    ...         batches=batch,
    ...         demand_list=items,
    ...         maximum_benefit=1,
    ...         price_constraints={
    ...             "apple": (10000, None),
    ...             "banana": (5000, None),
    ...             "orange": (0, None),
    ...             "date": (0, None),
    ...             "strawberry": (0, None),
    ...         },
    ...     )
    {'Status': 'Infeasible'}

    Attention: The function will raise a ValueError if an item requested is not contained in any batch.

    >>> result = maxEarnings(
    ...         batches=batch,
    ...         demand_list=items,
    ...         minimum_benefit=10405200,
    ...         maximum_benefit=1330405200,
    ...         price_constraints={
    ...             "apple": (100, 300),
    ...             "banana": (50, 100),
    ...             "orange": (10000, 20000),
    ...             "date": (5000, 10000),
    ...             "strawberry": (100, 300),
    ...         },
    ...         category_of_variables="Integer",
    ...         exchange_rate=1.2,
    ...         transport_fee=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
    ...         tax_rate=0.1,
    ...         customs_duty=0.2,
    ...     )
    >>> result
    {'Status': 'Optimal', 'Total benefit': 56120000.0, 'Item prices': {'apple': 300.0, 'banana': 100.0, 'orange': 20000.0, 'date': 10000.0, 'strawberry': 300.0}}
    >>> maxEarnings(
    ...             batches=batch,
    ...             demand_list=ItemListRequest(items=[ItemRequest("abcd", 100000)]),
    ...             maximum_benefit=1,
    ...             minimum_benefit=2,
    ...             price_constraints={
    ...                 "apple": (10000, None),
    ...                 "banana": (5000, None),
    ...                 "orange": (0, None),
    ...                 "date": (0, None),
    ...                 "strawberry": (0, None),
    ...             },
    ...             category_of_variables="Continuous",
    ...         )
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
        ...             Batch.from_str(
                    ^^^^^^^^^^^^^^^^
    ValueError: An item requested is not contained in any batch.

    Attention: The function will raise a ValueError if the maximum_benefit is less than the minimum_benefit.

    Example :

    >>> maxEarnings(
    ...     batch,
    ...     item_request,
    ...     maximum_benefit=1000,
    ...     minimum_benefit=100000
    ...     )
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
            variables, objective, constraints = _collecte_data_primal(
                                                ^^^^^^^^^^^^^^^^^^^^^^
            constraints = _generate_primal_constraints(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            prob = _apply_expense_constraints(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
            raise ValueError("maximum_benefit cannot be less than minimum_benefit")
        ValueError: maximum_benefit cannot be less than minimum_benefit
    """

    batches = _prepare_the_problem(
        batches=batches,
        demand_list=demand_list,
        exchange_rate=exchange_rate,
        tax_rate=tax_rate,
        customs_duty=customs_duty,
        transport_fee=transport_fee,
    )

    variables, objective, constraints = _collecte_data_dual(
        batches=batches,
        demand_list=demand_list,
        cat=category_of_variables,
        maximum_benefit=maximum_benefit,
        minimum_benefit=minimum_benefit,
        price_constraints=price_constraints,
    )

    prob = pulp.LpProblem("Dual problem", pulp.LpMaximize)
    prob += objective
    for constraint in constraints.values():
        prob += constraint
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    return _return_maxEarnings(variables=variables, demand_list=demand_list, prob=prob)


def _return_maxEarnings(
    variables: pulp.LpVariable, demand_list: ItemListRequest, prob: pulp.LpProblem
) -> dict[str, str | float | int | dict[str, float | int]]:
    """Returns of the maxEarnings function"""

    x = {
        item_request.name: pulp.value(variables[item_request.name])
        for item_request in demand_list
    }

    if pulp.LpStatus[prob.status] == "Infeasible":
        return {"Status": pulp.LpStatus[prob.status]}
    else:
        return {
            "Status": pulp.LpStatus[prob.status],
            "Total benefit": pulp.value(prob.objective),
            "Item prices": x,
        }
