"""Description:

Library contains the ItemRequest and the ItemListRequest dataclasses.

- The ItemRequest dataclass represents an item requested by the requester.
- The ItemListRequest dataclass represents the list of all items requested by the requester.

- This library is useful to resolve the batches_optimization problem.

You can import this library with the following command :
    import lib_item_request as lir

Developed by :
    - [Hugo Cochereau](https://github.com/hugocoche)
    - [Gregory Jaillet](https://github.com/Greg-jllt)
"""

import json
import math
from dataclasses import dataclass, field
from beartype.typing import Iterator
from prettytable import PrettyTable
from serde import serde


class Incompatible_negative_value(ValueError):
    """Error returned if the price of a batch or a quantity is negative."""

    pass


@serde
@dataclass
class ItemRequest:
    """Represents an item requested by the requester.

    An ItemRequest is identified by its name and the minimum quantity of this item that the requester needs.

    Args:

    name: str -> name of the item
    minimum_quantity: float | int -> minimum quantity of the item requested by the requester
    maximum_quantity: float | int -> maximum quantity of the item requested by the requester

    Returns:

    ItemRequest: ItemRequest -> item requested by the requester

    Raises:
    - Incompatible_negative_value: if the quantity of the item is negative
    - ValueError: if the minimum quantity is greater than the maximum quantity

    Examples:

    >>> request = ItemRequest("apple", 1, 2)
    >>> request
    ItemRequest(name='apple', minimum_quantity=1, maximum_quantity=2)


    The quantity of items cannot be negative :

    >>> ItemRequest("apple", -1, 2)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    lib_init.Incompatible_negative_value: The quantity of the item '-1' is negative, however, it must be positive or zero.

    The minimum quantity of the item must be less than the maximum quantity :

    >>> ItemRequest("apple", 2, 1)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    ValueError: The minimum quantity '2' is greater than the maximum quantity '1'.

    It is also possible to create an item from a string :

    >>> ItemRequest.from_str("1-2 of apple")
    ItemRequest(name='apple', minimum_quantity=2)

    If the maximum quantity is not specified, it is considered infinite, you must precise the maximum is the infinite :
    >>> ItemRequest.from_str("1-inf of apple")
    ItemRequest(name='apple', minimum_quantity=1, maximum_quantity=inf)

    if you don't specify the maximum quantity, it will raise an error :
    >>> ItemRequest.from_str("1 of apple")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in from_str
    ValueError: not enough values to unpack (expected 2, got 1)
    """

    name: str
    minimum_quantity: float | int
    maximum_quantity: float | int | None = None

    def __post_init__(self):
        """Checks if the item is valid."""

        if self.minimum_quantity < 0:
            raise Incompatible_negative_value(
                f"The quantity of the item '{self.minimum_quantity}' is negative, however, it must be positive or zero."
            )
        if self.maximum_quantity == float("inf"):
            self.maximum_quantity = None

        if self.maximum_quantity is not None:
            if self.maximum_quantity < 0:
                raise Incompatible_negative_value(
                    f"The quantity of the item '{self.maximum_quantity}' is negative, however, it must be positive or zero."
                )
            if self.minimum_quantity > self.maximum_quantity:
                raise ValueError(
                    f"The minimum quantity '{self.minimum_quantity}' is greater than the maximum quantity '{self.maximum_quantity}'."
                )

    def __hash__(self) -> int:
        """Returns the hash of the item."""

        return hash((self.name, self.minimum_quantity, self.maximum_quantity))

    def __getitem__(self, key: str | int) -> str | float | int | None:
        """Returns the item at the index key.

        Args:
        - key: str | int -> index of the item

        Returns:
        - str: str -> name of the item
        - float: float -> minimum quantity of the item requested by the requester

        Examples:

        >>> request = ItemRequest("apple", 1, 2)
        >>> request[0]
        'apple'
        >>> request[1]
        1
        >>> request[2]
        2
        >>> request["name"]
        'apple'
        >>> request["minimum_quantity"]
        1
        >>> request["maximum_quantity"]
        2
        """

        if key == 0 or key == "name":
            return self.name
        elif key == 1 or key == "minimum_quantity":
            return self.minimum_quantity
        elif key == 2 or key == "maximum_quantity":
            return self.maximum_quantity
        else:
            if isinstance(key, int):
                raise IndexError("The index is out of range.")
            else:
                raise ValueError(f"The key '{key}' is invalid.")

    def __str__(self) -> str:
        """Returns a string representation of the item."""

        table = PrettyTable()
        table.field_names = [
            "Item name",
            "Minimum Quantity requested",
            "Maximum Quantity requested",
        ]
        table.add_row([self.name, self.minimum_quantity, self.maximum_quantity])
        return f"{table}"

    def __iter__(self) -> Iterator[str | float | int | None]:
        """Returns an iterator on the item.

        Examples:

        >>> request = ItemRequest("apple", 1, 2)
        >>> for item in request:
        ...     item
        'apple'
        1
        2
        """

        yield self.name
        yield self.minimum_quantity
        yield self.maximum_quantity

    def __eq__(self, other: object) -> bool:
        """Checks if the item is equal to another item.

        Args:
        - other: ItemRequest -> another item

        Returns:
        - bool: bool -> True if the item is equal to the other item, False otherwise

        Examples:

        >>> request = ItemRequest("apple", 1, 2)
        >>> request == ItemRequest("apple", 1, 2)
        True
        """
        if not isinstance(other, ItemRequest):
            return NotImplemented

        return (
            self.name == other.name
            and self.minimum_quantity == other.minimum_quantity
            and self.maximum_quantity == other.maximum_quantity
        )

    def __ne__(self, other: object) -> bool:
        """Checks if the item is different from another item.

        Args:
        - other: ItemRequest -> another item

        Returns:
        - bool: bool -> True if the item is different from the other item, False otherwise

        Examples:

        >>> request = ItemRequest("apple", 1, 2)
        >>> request != ItemRequest("apple", 1, 2)
        False
        """

        if not isinstance(other, ItemRequest):
            return NotImplemented

        return not self.__eq__(other)

    @classmethod
    def from_str(cls, string: str) -> "ItemRequest":
        """Creates an item from a string.

        Args:
        - string: str -> string representation of the item

        Returns:
        - ItemRequest: ItemRequest -> item requested by the requester

        Raises:
        - ValueError: if the maximum quantity is not specified

        Examples:

        >>> ItemRequest.from_str("1-2 of apple")
        ItemRequest(name='apple', minimum_quantity=1, maximum_quantity=2)

        Attention, if the maximum quantity is not specified, it is considered infinite, you must precise the maximum is the infinite :
        >>> ItemRequest.from_str("1-inf of apple")
        ItemRequest(name='apple', minimum_quantity=1, maximum_quantity=inf)

        if you don't specify the maximum quantity, it will raise an error :
        >>> ItemRequest.from_str("1 of apple")
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<string>", line 5, in from_str
        ValueError: not enough values to unpack (expected 2, got 1)
        """

        quantities, name = string.split(" of ")
        minimum_quantity, maximum_quantity = quantities.split("-")
        return cls(name, float(minimum_quantity), float(maximum_quantity))


@serde
@dataclass
class ItemListRequest:
    """Represents the list of all items requested by the requester.

    Args:

    ItemListRequest: list[ItemRequest] -> list of items requested by the requester

    Returns:

    ItemListRequest: ItemListRequest -> list of items requested by the requester

    Raises:
    - TypeError: if the item is not an instance of the class 'ItemRequest'
    - ValueError: if the name of the item is not unique

    Examples:

    >>> ItemListRequest({ItemRequest("apple", 1, 3), ItemRequest("banana", 2, 3)})
    ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=1, maximum_quantity = 3), ItemRequest(name='banana', minimum_quantity=2, maximum_quantity = 3)])

    Attention, the item must be an instance of the class 'ItemRequest' :
    >>> ItemListRequest(
    ...             [
    ...                 ItemRequest("apple", 5),
    ...                 ItemRequest("banana", 7),
    ...                 ItemRequest("orange", 9),
    ...                 "cherries",
    ...             ]
    ...         )
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<@beartype(batches_optimization.lib_item_request.ItemListRequest.__init__) at 0x219e22916c0>", line 44, in __init__
    File "<string>", line 4, in __init__
    line 166, in __post_init__
        raise TypeError(
    TypeError: The item 'cherries' is not an instance of the class 'ItemRequest'.


    An item cannot be requested several times in different quantities in an ItemListRequest:

    >>> ItemListRequest({ItemRequest("apple", 1), ItemRequest("apple", 2)})
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    ValueError: The name of the item 'apple' is not unique.


    It is also possible to create a list of items from a string :

    >>> ItemListRequest.from_str("1-2 of apple, 2-3 of banana")
    ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=1.0, maximum_quantity = 3.0), ItemRequest(name='banana', minimum_quantity=2.0, maximum_quantity = 3.0)])

    Thanks to print, we can display the items in a readable way :

    >>> print(ItemListRequest({ItemRequest("apple", 1, 2), ItemRequest("banana", 2, 3)}))
    The requested items are :
    +-----------------+----------------------------+------------------------------+
    | Item name       | Minimum Quantity requested |   Maximum Quantity requested |
    +-----------------+----------------------------+------------------------------+
    |     apple      |              1             |                2             |
    |     banana      |              2             |                3             |
    +-----------------+----------------------------+------------------------------+

    """

    items: list[ItemRequest] = field(default_factory=list)

    def __post_init__(self):
        """Checks if the list of items is valid."""

        if len(self.items) > 0:
            item_already_seen = set()
            for item in self.items:
                if item.name not in item_already_seen:
                    item_already_seen.add(item.name)
                else:
                    raise ValueError(
                        f"The name of the item '{item.name}' is not unique."
                    )

    def __contains__(self, item: ItemRequest) -> bool:
        """Checks if the item is in the list of items requested.

        Args:
        - item: ItemRequest -> item to check if it is in the list of items requested

        Returns:
        - bool: bool -> True if the item is in the list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> ItemRequest("apple", 5, 6) in item_list_request
        True
        >>> ItemRequest("orange", 9, 10) in item_list_request
        False
        """

        return item in self.items

    def __str__(self) -> str:
        """Prints the items in a readable way with print()."""

        table = PrettyTable()
        table.field_names = [
            "Item name",
            "Minimum Quantity requested",
            "Maximum Quantity requested",
        ]
        for item in self.items:
            table.add_row([item.name, item.minimum_quantity, item.maximum_quantity])
        return f"The requested items are : \n{table}"

    def __getitem__(self, key: str | int) -> ItemRequest | list[ItemRequest]:
        """Returns the item at the index key.

        Args:
        - key: str | int -> index of the item

        Returns:
        - ItemRequest: ItemRequest -> item requested by the requester

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...             ItemRequest("orange", 9, 10),
                ...         ]
                ...     )
        >>> item_list_request[0]
        ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6)
        >>> item_list_request["items"]
        [ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8), ItemRequest(name='orange', minimum_quantity=9, maximum_quantity=10)]
        """

        if key == "items":
            return self.items
        elif isinstance(key, int):
            return self.items[key]
        else:
            raise KeyError(f"The key '{key}' is invalid.")

    def __len__(self) -> int:
        """Returns the number of items requested.

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...             ItemRequest("orange", 9, 10),
                ...         ]
                ...     )
        >>> len(item_list_request)
        3
        """

        return len(self.items)

    def __iter__(self) -> Iterator[ItemRequest]:
        """Returns an iterator on the items requested.

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...             ItemRequest("orange", 9, 10),
                ...         ]
                ...     )
        >>> for item in item_list_request:
        ...     item
        ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6)
        ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8)
        ItemRequest(name='orange', minimum_quantity=9, maximum_quantity=10)
        """

        return iter(self.items)

    def __hash__(self) -> int:
        """Returns the hash of the items requested."""

        return hash(tuple(self.items))

    def __eq__(self, other: object) -> bool:
        """Checks if the items requested are equal to another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are equal to the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...             ItemRequest("orange", 9, 10),
                ...         ]
                ...     )
        >>> item_list_request == ItemListRequest(
            ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        True
        """

        if not isinstance(other, ItemListRequest):
            return NotImplemented

        return self.items == other.items

    def __ne__(self, other: object) -> bool:
        """Checks if the items requested are different from another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are different from the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...             ItemRequest("orange", 9, 10),
                ...         ]
                ...     )
        >>> item_list_request != ItemListRequest(

                ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        False
        """

        if not isinstance(other, ItemListRequest):
            return NotImplemented

        return not self.__eq__(other)

    def __le__(self, other: "ItemListRequest") -> bool:
        """Checks if the items requested are less than or equal to another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are less than or equal to the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request <= ItemListRequest(
            ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        True
        """

        return len(self.items) <= len(other.items)

    def __lt__(self, other: "ItemListRequest") -> bool:
        """Checks if the items requested are less than another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are less than the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request < ItemListRequest(
            ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        True
        """

        return len(self.items) < len(other.items)

    def __ge__(self, other: "ItemListRequest") -> bool:
        """Checks if the items requested are greater than or equal to another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are greater than or equal to the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request >= ItemListRequest(
            ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        False
        """

        return len(self.items) >= len(other.items)

    def __gt__(self, other: "ItemListRequest") -> bool:
        """Checks if the items requested are greater than another list of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - bool: bool -> True if the items requested are greater than the other list of items requested, False otherwise

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request > ItemListRequest(
            ...         [
                ...             ItemRequest(name="apple", minimum_quantity=5, maximum_quantity=6),
                ...             ItemRequest(name="banana", minimum_quantity=7, maximum_quantity=8),
                ...             ItemRequest(name="orange", minimum_quantity=9, maximum_quantity=10),
                ...         ]
                ...     )
        False
        """

        return len(self.items) > len(other.items)

    def __add__(self, other: "ItemListRequest") -> "ItemListRequest":
        """Adds two lists of items requested.

        Args:
        - other: ItemListRequest -> another list of items requested

        Returns:
        - ItemListRequest: ItemListRequest -> list of items requested by the requester

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
            ...         ]
            ...     )
        >>> item_list_request + ItemListRequest(
            ...         [
                ...             ItemRequest("orange", 9, 10),
                ...             ItemRequest("cherries", 9, 10),
            ...         ]
            ...     )
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8), ItemRequest(name='orange', minimum_quantity=9, maximum_quantity=10), ItemRequest(name='cherries', minimum_quantity=9, maximum_quantity=10)])
        """
        item = ItemListRequest(self.items + other.items)
        item.__post_init__()
        return item

    @classmethod
    def from_str(cls, *string: str) -> "ItemListRequest":
        """Creates a list of items from a string.

        Args:
        - string: str -> string representation of the list of items requested

        Returns:
        - ItemListRequest: ItemListRequest -> list of items requested by the requester

        Raises:
        - ValueError: if the maximum quantity is not specified

        Examples:

        >>> ItemListRequest.from_str("1-2 of apple", "2-3 of banana")
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=1.0, maximum_quantity = 3.0), ItemRequest(name='banana', minimum_quantity=2.0, maximum_quantity = 3.0])

        Attention, if the maximum quantity is not specified, it is considered infinite, you must precise the maximum is the infinite :
        >>> ItemListRequest.from_str("1-inf of apple", "2-3 of banana")
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=1.0, maximum_quantity = inf), ItemRequest(name='banana', minimum_quantity=2.0, maximum_quantity = 3.0)

        if you don't specify the maximum quantity, it will raise an error :
        >>> ItemListRequest.from_str("1 of apple", "2 of banana")
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<string>", line 5, in from_str
        ValueError: not enough values to unpack (expected 2, got 1)
        """

        return cls([ItemRequest.from_str(s) for s in string])

    def add_item(self, *items: ItemRequest) -> "ItemListRequest":
        """Adds an item or a list of item to the list of items requested.

        Args:
        - item: ItemRequest -> item to add to the list of items requested

        Returns:
        - ItemListRequest: ItemListRequest -> list of items requested by the requester

        Raises:
        - ValueError: if the item is already in the list

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.add_item(ItemRequest("orange", 9, 10))
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8), ItemRequest(name='orange', minimum_quantity=9, maximum_quantity=10)])

        You can also add several items at the same time :

        >>> item_list_request.add_item(ItemRequest("orange", 9, 10), ItemRequest("cherries", 9, 10))
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8), ItemRequest(name='orange', minimum_quantity=9, maximum_quantity=10), ItemRequest(name='cherries', minimum_quantity=9, maximum_quantity=10)])

        You cannot add an item that is already in the list :

        >>> item_list_request.add_item(ItemRequest("apple", 5, 6))
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<string>", line 5, in add_item
        ValueError: The item 'ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6)' is already in the list.
        """

        for item in items:
            if item in self.items:
                raise ValueError(f"The item '{item}' is already in the list.")
            self.items.append(item)
        self.__post_init__()
        return self

    def remove_item(self, *index: int, **item_name: str) -> "ItemListRequest":
        """Removes an item from the list of items requested.

        Args:
        - index: int -> index of the item to remove from the list of items requested
        - item_name: str -> name of the item to remove from the list of items requested

        Returns:
        - ItemListRequest: ItemListRequest -> list of items requested by the requester

        Raises:
        - ValueError: if the item is not in the list

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.remove_item(0)
        ItemListRequest(items=[ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8)])

        You can also remove several items at the same time :

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.remove_item(0, 1)
        ItemListRequest(items=[])

        You can also remove an item by its name :

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.remove_item(item_name="banana")
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6)])

        You cannot remove several items at the same time by their name :

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.remove_item(item_name="banana", apple = "apple")
        ItemListRequest(items=[])
        """

        if index:
            for i in sorted(index, reverse=True):
                if i < len(self.items):
                    self.items.pop(i)
                else:
                    raise ValueError(f"The index '{i}' is out of range.")
        if item_name:
            for name in item_name.values():
                indice = self.find(name)
                if indice is not None:
                    self.items.pop(indice)
                else:
                    raise ValueError(f"The item '{name}' is not in the list.")
        return self

    def find(self, item_name: str) -> int | None:
        """Finds an item in the list of items requested.

        Args:
        - item_name: str -> name of the item to find

        Returns:
        - int: int -> index of the item found
        - None: None -> if the item is not found

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.find("apple")
        0
        """

        for index, item in enumerate(self):
            if item.name == item_name:
                return index
        return None

    def sort(self, by="name", reverse: bool = False) -> "ItemListRequest":
        """Sorts the list of items requested.

        Args:
        - by: str -> the criterion to sort the items requested (name, minimum_quantity, maximum_quantity)
        - reverse: bool -> if the list of items requested is sorted in ascending or descending order

        Returns:
        - ItemListRequest: ItemListRequest -> list of items requested by the requester

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.sort("name")
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8)])

        >>> item_list_request.sort("minimum_quantity", reverse=True)
        ItemListRequest(items=[ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8), ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6)])

        >>> item_list_request.sort("maximum_quantity")
        ItemListRequest(items=[ItemRequest(name='apple', minimum_quantity=5, maximum_quantity=6), ItemRequest(name='banana', minimum_quantity=7, maximum_quantity=8)])
        """

        if by == "name":
            self.items.sort(
                key=lambda x: x.name if x.name is not None else "", reverse=reverse
            )
        elif by == "minimum_quantity":
            self.items.sort(
                key=lambda x: (
                    x.minimum_quantity if x.minimum_quantity is not None else -math.inf
                ),
                reverse=reverse,
            )
        elif by == "maximum_quantity":
            self.items.sort(
                key=lambda x: (
                    x.maximum_quantity if x.maximum_quantity is not None else math.inf
                ),
                reverse=reverse,
            )
        return self

    def to_json(self, path: str = "ItemlistRequest.json"):
        """Saves the list of items requested in a json file.

        Args:
        - path: str -> path to save the list of items requested

        Examples:

        >>> item_list_request = ItemListRequest(
            ...         [
                ...             ItemRequest("apple", 5, 6),
                ...             ItemRequest("banana", 7, 8),
                ...         ]
                ...     )
        >>> item_list_request.to_json("items.json")
        """
        try:
            with open(path, "w") as file:
                json.dump(self, file, default=lambda o: o.__dict__, indent=4)
        except Exception as error:
            raise error

    @classmethod
    def from_json(cls, path: str = "ItemlistRequest.json") -> "ItemListRequest":
        """Loads the list of items requested from a json file.

        Args:
        - path: str -> path to load the list of items requested

        Examples:

        >>> ItemListRequest.from_json("items.json")
        """
        try:
            with open(path, "r") as file:
                json_ilr = json.load(file)

            ilr = ItemListRequest()
            for item in json_ilr["items"]:
                item_name = item["name"]
                item_min_quantity = item["minimum_quantity"]
                item_max_quantity = item["maximum_quantity"]
                ilr.add_item(
                    ItemRequest(item_name, item_min_quantity, item_max_quantity)
                )
            ilr.__post_init__()
            return ilr
        except Exception as error:
            raise error
