"""Description:

Library containing the creation of dataclasses Item_in_batch, Batch, BatchCollection, BatchLists

- Item_in_batch : class representing the different items and their respective quantity in the considered batch.
- Batch : class representing the proposed batches of items.
- BatchCollection : class representing the list of batches sold by one seller.
- BatchLists : class representing the list of batches sold by each seller.

- This library is useful to resolve the batches_optimization problem.

You can import this library with the following command :
    import lib_batches as lb

Developed by :
    - [Hugo Cochereau](https://github.com/hugocoche)
    - [Gregory Jaillet](https://github.com/Greg-jllt)
"""

import json
import warnings
from dataclasses import dataclass, field

import numpy as np
from beartype.typing import Iterator
from prettytable import PrettyTable
from serde import serde


class Incompatible_negative_value(ValueError):
    """Error returned if the price of a batch or a quantity is negative."""

    pass


@serde
@dataclass
class Item_in_batch:
    """Class illustrating the different items
    and their respective quantity in the considered batch.

    Args :
        name: str -> name of the item
        quantity_in_batch: float -> quantity of the item in the batch

    Returns :
        Item_in_batch : item and its quantity in the batch

    Raises :
        Incompatible_negative_value : if the quantity of the item is negative

    Example :

    >>> Item_in_batch(name = "apple",quantity_in_batch = 5)
    Item_in_batch(name='apple', quantity_in_batch=5)

    It is also possible to create an item from a string:

    >>> Item_in_batch.from_str("2xapple")
    Item_in_batch(name='apple', quantity_in_batch=2)

    Attention, the quantity of items cannot be negative :

    >>> Item_in_batch(name = "apple",quantity_in_batch = -5)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    lib_init.Incompatible_negative_value: The quantity of the entered item :
    '-5' is negative, however, it must be positive or zero.
    """

    name: str
    quantity_in_batch: float | int

    def __post_init__(self):
        """Checks if the item is valid."""

        if self.quantity_in_batch < 0:
            raise Incompatible_negative_value(
                f"The specific quantity of the entered item : \n '{self.quantity_in_batch}' is negative, however, it must be positive or zero."
            )

    def __str__(self) -> str:
        """Prints the item in a readable way with print()."""

        table = PrettyTable()
        table.field_names = ["Item name", "Quantity in batch"]
        table.add_row([self.name, self.quantity_in_batch])
        return f"{table}"

    def __hash__(self) -> int:
        """Returns the hash of the item."""

        return hash((self.name, self.quantity_in_batch))

    def __getitem__(self, index: int | str) -> str | float | int:
        """Returns the name or the quantity of the item at the specified index.

        Args :
        - index : int | str : index of the item

        Returns :
        - str | float : name or quantity of the item

        Raises :
        - IndexError : if the index is not valid

        Example :

        >>> item = Item_in_batch("apple", 5)
        >>> item[0]
        'apple'
        >>> item[1]
        5
        """

        if index == 0 or index == "name":
            return self.name
        elif index == 1 or index == "quantity_in_batch":
            return self.quantity_in_batch
        elif isinstance(index, int):
            raise IndexError("You must provide a valid index.")
        else:
            raise KeyError("You must provide a valid key.")

    def __iter__(self) -> Iterator[str | float | int]:
        """Returns an iterator over the item.

        Example :

        >>> item = Item_in_batch("apple", 5)
        >>> for i in item:
        ...     i
        apple
        5
        """

        yield self.name
        yield self.quantity_in_batch

    def __eq__(self, other: object) -> bool:
        """Returns True if the two Item_in_batch objects are equal, False otherwise.

        Args :
        - other : Item_in_batch : other item

        Returns :
        - bool : True if the two Item_in_batch objects are equal, False otherwise

        Example :

        >>> Item_in_batch("apple", 5) == Item_in_batch("apple", 5)
        True

        >>> Item_in_batch("apple", 5) == Item_in_batch("orange", 5)
        False
        """

        if not isinstance(other, Item_in_batch):
            return NotImplemented

        return (
            self.name == other.name
            and self.quantity_in_batch == other.quantity_in_batch
        )

    def __ne__(self, other: object) -> bool:
        """Returns True if the two Item_in_batch objects are different, False otherwise.

        Args :
        - other : Item_in_batch : other item

        Returns :
        - bool : True if the two Item_in_batch objects are different, False otherwise

        Example :

        >>> Item_in_batch("apple", 5) != Item_in_batch("apple", 5)
        False

        >>> Item_in_batch("apple", 5) != Item_in_batch("orange", 5)
        True
        """

        if not isinstance(other, Item_in_batch):
            return NotImplemented

        return (
            self.name != other.name or self.quantity_in_batch != other.quantity_in_batch
        )

    @classmethod
    def from_str(cls, string: str) -> "Item_in_batch":
        """Creates an item from a string.

        Args :
        - string : str : string representing the item

        Returns :
        - Item_in_batch : item

        Example :

        >>> Item_in_batch.from_str("2xapple")
        Item_in_batch(name='apple', quantity_in_batch=2.0)
        """

        quantity_in_batch, name = string.split("x")

        return cls(name, float(quantity_in_batch))


@serde
@dataclass
class Batch:
    """Class representing the proposed batches of items.

    Args :
    - name : str -> name of the batch
    - price: float | int -> price of the batch
    - items: list[Item_in_batch] -> list of items contained in the batch

    Returns :
    - Batch : proposed batch of items

    Raises :
    - Incompatible_negative_value : if the price of the batch or the quantity of items is negative
    - ValueError : if the names of the items are not unique

    Example :

    >>> Batch(
            name = "batch 1"
            price = 1,
            items = [
                Item_in_batch(name = "apple", quantity_in_batch = 1),
                Item_in_batch(name = "orange", quantity_in_batch = 2
                )
            ]
        )
    Batch(name = "batch 1", price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)])

    The best way to create a batch is to use the Item_in_batch class :

    >>> item1 = Item_in_batch("apple", 1)
    >>> item2 = Item_in_batch("orange", 2)
    >>> Batch(name = "batch 1", price = 1, items = [item1, item2])
    Batch(name = "batch 1", price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)])

    It is also possible to create a batch from a string :

    >>> Batch.from_str("batch 1:1; 2xapple, 3xorange")
    Batch(name = "batch 1", price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3)])

    Thanks to print(), we can display the batches in a readable way :

    >>> print(Batch(name = "batch 1", price=1, items=[Item_in_batch("apple", 1), Item_in_batch("orange", 2)]))
    Batch : batch 1 - Price : 1
    +-----------------+----------+
    |   Item name     | Quantity |
    +-----------------+----------+
    |     apple      |    1     |
    |     orange      |    2     |
    +-----------------+----------+

    Attention, the price of the batch and the quantity of items cannot be negative :

    >>> Batch(name = "batch 1", price = -1, items = [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    lib_init.Incompatible_negative_value: The price of the batch '-1' is negative, however, it must be positive or zero.

    >>> Batch(name = "batch 1", price = 1, items = [Item_in_batch("apple", -1), Item_in_batch("orange", 2)])
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    lib_init.Incompatible_negative_value: The quantity of 'apple' is '-1', but it must be positive or zero.

    The names of the items must be unique :

    >>> Batch(name = "batch 1", price = 1, items = [Item_in_batch("apple", 1), Item_in_batch("apple", 2)])
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    ValueError: Some items have the same name in the batch !
    """

    name: str
    price: float | int
    items: list[Item_in_batch] = field(default_factory=list)

    def __post_init__(self):
        """Checks if the batch is valid."""

        if self.price < 0:
            raise Incompatible_negative_value(
                f"The price of the batch '{self.price}' is negative, however, it must be positive or zero."
            )

        if len(self) > 0:
            item_names = [item.name for item in self.items]
            if len(item_names) != len(set(item_names)):
                raise ValueError("Some items have the same name in the batch !")

    def __hash__(self):
        """Returns the hash of the batch."""

        return hash((self.name, self.price, tuple(self.items)))

    def __str__(self) -> str:
        """Prints the batch in a readable way with print()."""

        table = PrettyTable()
        table.field_names = ["Item name", "Quantity"]
        for item in self.items:
            table.add_row([item.name, item.quantity_in_batch])
        return f"Batch : {self.name} - Price : {self.price}\n{table}"

    def __getitem__(
        self, index: int | str
    ) -> str | float | int | Item_in_batch | list[Item_in_batch]:
        """Returns the name, the price or the items at the specified index.

        Args :
        - index : int | str : index of the item

        Returns :
        - str | float | list[Item_in_batch] : name, price or items of the batch

        Raises :
        - IndexError : if the index is not valid

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch['name']
        'batch 1'

        >>> batch['price']
        1

        >>> batch['items']
        [Item_in_batch(name='apple',quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]

        >>> batch[0]
        Item_in_batch(name='apple', quantity_in_batch=1)

        >>> batch[1]
        Item_in_batch(name='orange', quantity_in_batch=2)
        """

        if index == "name":
            return self.name
        elif index == "price":
            return self.price
        elif index == "items":
            return self.items
        elif isinstance(index, int):
            return self.items[index]
        elif isinstance(index, str):
            raise KeyError("You must provide a valid key.")
        else:
            raise IndexError("You must provide a valid index.")

    def __iter__(self) -> Iterator[Item_in_batch]:
        """Returns an iterator over the items.

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])

        >>> for i in batch :
        ...     i
        Item_in_batch(name='apple', quantity_in_batch=1)
        Item_in_batch(name='orange', quantity_in_batch=2)
        """

        return iter(self.items)

    def __len__(self) -> int:
        """Returns the number of items in the batch.

        Example :

        >>> batch = Batch(name = "batch 1", price = 1, items = [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])

        >>> len(batch)
        2
        """

        return len(self.items)

    def __contains__(self, item_name: str) -> bool:
        """Returns True if the item is in the batch, False otherwise.

        Args :
        - item_name : str : name of the item

        Returns :
        - bool : True if the item is in the batch, False otherwise

        Example :

        >>> batch = Batch(name = "batch 1", price = 1, items = [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])

        >>> "apple" in batch
        True

        >>> "banana" in batch
        False
        """

        for item in self:
            if item.name == item_name:
                return True
        return False

    def __add__(self, other: "Batch") -> "Batch":
        """Returns a new Batch object with the items of the two Batch objects.
        name is the concatenation of the names of the two Batch objects.
        price is the sum of the prices of the two Batch objects.
        if the two Batch objects have the same item, the quantity of the item is the sum of the quantities of the two Batch objects.

        Args :
        - other : Batch : other batch

        Returns :
        - Batch : new batch with the items of the two Batch objects, the price is the sum of the prices of the two Batch objects

        Example :

        >>> batch1 = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])

        >>> batch2 = Batch("batch 2", 2, [Item_in_batch("banana", 3), Item_in_batch("pinapple", 4)])

        >>> batch1 + batch2
        Batch(
            name='batch 1 + batch 2',
            price=3,
            items=[
                Item_in_batch(name='apple', quantity_in_batch=1),
                Item_in_batch(name='orange', quantity_in_batch=2),
                Item_in_batch(name='banana', quantity_in_batch=3),
                Item_in_batch(name='pinapple', quantity_in_batch=4)
            ]
        )
        """

        new_items_dict = {}
        for item in self.items:
            new_items_dict[item.name] = item.quantity_in_batch
        for item in other.items:
            if item.name in new_items_dict:
                new_items_dict[item.name] += item.quantity_in_batch
            else:
                new_items_dict[item.name] = item.quantity_in_batch
        new_items_list = [
            Item_in_batch(name, quantity) for name, quantity in new_items_dict.items()
        ]

        return Batch(
            f"{self.name} + {other.name}",
            self.price + other.price,
            new_items_list,
        )

    def __eq__(self, other: object) -> bool:
        """Returns True if the two Batch objects are equal, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the two Batch objects are equal, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) == Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        True

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) == Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        False
        """

        if not isinstance(other, Batch):
            return NotImplemented

        return (
            self.name == other.name
            and self.price == other.price
            and self.items == other.items
        )

    def __ne__(self, other: object) -> bool:
        """Returns True if the two Batch objects are different, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the two Batch objects are different, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) != Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        False

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) != Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        True
        """

        if not isinstance(other, Batch):
            return NotImplemented

        return (
            self.name != other.name
            or self.price != other.price
            or self.items != other.items
        )

    def __lt__(self, other: "Batch") -> bool:
        """Returns True if the first Batch object has less items than the second Batch object, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the first Batch object has less items than the second Batch object, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) < Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        False

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) < Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2), Item_in_batch("banana", 3)])
        True
        """

        return len(self) < len(other)

    def __le__(self, other: "Batch") -> bool:
        """Returns True if the first Batch object has less items than or equal to the second Batch object, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the first Batch object has less items than or equal to the second Batch object, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) <= Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        True

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) <= Batch("batch 1", 1, [Item_in_batch("orange", 2)]
        False
        """

        return len(self) <= len(other)

    def __gt__(self, other: "Batch") -> bool:
        """Returns True if the first Batch object has more items than the second Batch object, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the first Batch object has more items than the second Batch object, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) > Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        False

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) > Batch("batch 1", 1, [Item_in_batch("orange", 2)]
        True
        """

        return len(self) > len(other)

    def __ge__(self, other: "Batch") -> bool:
        """Returns True if the first Batch object has more items than or equal to the second Batch object, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the first Batch object has more items than or equal to the second Batch object, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]) >= Batch("batch 2", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        True

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1)]) >= Batch("batch 1", 1, [Item_in_batch("orange", 2), Item_in_batch("banana", 3)])
        False
        """

        return len(self) >= len(other)

    @classmethod
    def from_str(cls, string: str) -> "Batch":
        """Creates a batch from a string.

        Args :
        - string : str : string representing the batch

        Returns :
        - Batch : batch

        Example :

        >>> Batch.from_str("batch 1:1; 2xapple, 3xorange")
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3)])
        """

        batch_caracteristics, items = string.split(";")
        batch_name, batch_price = batch_caracteristics.split(":")
        item_list = items.split(",")
        batch_price_float = float(batch_price)
        item_in_batch_list = [Item_in_batch.from_str(item) for item in item_list]

        return cls(batch_name, batch_price_float, item_in_batch_list)

    def add_item(self, *items: Item_in_batch, add_quantities: bool = False) -> "Batch":
        """Adds an item or a list of items to the list of items in the batch.

        Args :
        - item : Item_in_batch | list[Item_in_batch] : item or item list to add to the list of items in the batch

        Returns :
        - Batch : batch with the added item

        Raises :
        - TypeError : if the item is not of type Item_in_batch
        - ValueError : if the name of the item is not unique

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.add_item(Item_in_batch("banana", 3))
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2), Item_in_batch(name='banana', quantity_in_batch=3)])

        a list of items can also be added :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.add_item([Item_in_batch("banana", 3), Item_in_batch("pinapple", 4)])
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2), Item_in_batch(name='banana', quantity_in_batch=3), Item_in_batch(name='pinapple', quantity_in_batch=4)])

        More simply,

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.add_item(Item_in_batch("apple", 3), Item_in_batch("orange", 4))
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=4), Item_in_batch(name='orange', quantity_in_batch=6)])

        if the item is already in the batch, the quantity of the item is the sum of the quantities of the two items if add_quantities is True, otherwise an error is raised:

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.add_item(Item_in_batch("apple", 3), add_quantities=True)
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=4), Item_in_batch(name='orange', quantity_in_batch=2)])
        """

        existing_items = {item.name: item for item in self.items}

        for item in items:
            if item.name in existing_items:
                if add_quantities:
                    existing_items[
                        item.name
                    ].quantity_in_batch += item.quantity_in_batch
                else:
                    raise ValueError("Some items have the same name in the batch !")
            else:
                existing_items[item.name] = item

        self.items = list(existing_items.values())
        self.__post_init__()
        return self

    def remove_item(self, *index: int, **item_names: str) -> "Batch":
        """Removes an item or a list of items from the list of items in the batch.

        Args :
        - index : int | list[int] : index or list of indexes of the items to remove from the list of items in the batch
        - item_names : str : name of the item to remove from the list of items in the batch

        Returns :
        - Batch : batch with the removed item

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.remove_item(item_names="apple")
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='orange', quantity_in_batch=2)])

        a list of items can also be removed :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.remove_item(item_names="apple", "orange")

        an item can also be removed by its index :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.remove_item(index=0)
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='orange', quantity_in_batch=2)])

        a list of items can also be removed by their indexes :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.remove_item(0,1)
        Batch(name='batch 1', price=1, items=[])
        """

        if item_names:
            for item_name in item_names.values():
                self.items = [item for item in self.items if item.name != item_name]
        elif index:
            for ind in sorted(index, reverse=True):
                self.items.pop(ind)
        return self

    def find_item(
        self, item_name: str | None = None, item_quantity: float | int | None = None
    ) -> int | list[int] | None:
        """Returns the item corresponding to the item name or the item quantity in batch.

        Args :
        - item_name : str : name of the item
        - item_quantity : float | int : quantity of the item in the batch

        Returns :
        - int | None : index of the item in the batch

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
        >>> batch.find(item_name="apple")
        0
        >>> batch.find(item_quantity=2)
        1
        """

        if item_name:
            return next(
                (
                    index
                    for index, item in enumerate(self.items)
                    if item.name == item_name
                ),
                None,
            )
        elif item_quantity:
            indexes = [
                index
                for index, item in enumerate(self.items)
                if item.quantity_in_batch == item_quantity
            ]
            return indexes[0] if len(indexes) == 1 else indexes if indexes else None
        else:
            return None

    def sort(self, by: str = "name", reverse: bool = False) -> "Batch":
        """Sorts the items in the batch by name or the quantity in batch in ascending order or descending order.

        Args :
        - by : str : name or quantity
        - reverse : bool : True if the items are sorted in descending order, False otherwise

        Returns :
        - Batch : batch with the sorted items

        Example :

        >>> batch = Batch("batch 1", 1, [Item_in_batch("orange", 1), Item_in_batch("apple", 2)])
        >>> batch.sort(by="name")
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=1)])


        >>> batch = Batch("batch 1", 1, [Item_in_batch("orange", 1), Item_in_batch("apple", 2)])
        >>> batch.sort(by="quantity", reverse=False)
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='orange', quantity_in_batch=1), Item_in_batch(name='apple', quantity_in_batch=2)])


        >>> batch = Batch("batch 1", 1, [Item_in_batch("orange", 1), Item_in_batch("apple", 2)])
        >>> batch.sort(by="quantity", reverse=True)
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=1)])
        """

        if by == "name":
            self.items.sort(key=lambda x: x.name, reverse=reverse)
            return self
        elif by == "quantity":
            self.items.sort(key=lambda x: x.quantity_in_batch, reverse=reverse)
            return self
        else:
            raise KeyError("You must provide a valid key.")

    def are_equal(self, other: "Batch") -> bool:
        """Returns True if the two Batch objects have the same items, False otherwise.

        Args :
        - other : Batch : other batch

        Returns :
        - bool : True if the two Batch objects have the same items, False otherwise

        Example :

        >>> Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]).are_equal(Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]))
        True
        """

        return set(self) == set(other)


@serde
@dataclass
class BatchCollection:
    """Class representing the list of batches sold by the seller.

    Args :
    - batch_list : list[Batch] : list of batches sold by the seller.
    - seller : str : name of the seller.

    Returns :
    - BatchCollection : list of batches sold by the seller.

    Raises :
    - ValueError : if the names of the batches are not unique.
    - TypeError : if the elements of the list are not of type Batch.

    Warning :
    - Some batches contain weapons not present in other batches. They have been added with a quantity of 0.

    Example :

    >>> BatchCollection(
            seller = "seller1",
            batch_list = [
                Batch(
                    name = "batch 1",
                    price = 1,
                    items = [
                        Item_in_batch(name = "apple", quantity_in_batch = 1),
                        Item_in_batch(name = "orange", quantity_in_batch = 2
                        )
                    ]
                ),
                Batch(
                    name = "batch 2",
                    price = 2,
                    items = [
                        Item_in_batch(name = "apple", quantity_in_batch = 3),
                        Item_in_batch(name = "orange", quantity_in_batch = 4)
                    ]
                )
            ]
        )
    BatchCollection(seller = "seller1", batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, elements=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)])])

    The best way to create a batchCollection is to use the Batch class :

    >>> batch1 = Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])
    >>> batch2 = Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])
    >>> BatchCollection(batch_list = [batch1, batch2], seller = "seller1")

    It is also possible to create a list of batches from a string :

    >>> BatchCollection(
            seller = "seller1",
            batch_list = [
                Batch.from_str("batch 1:1; 2xapple, 3xorange, 5xbanana"),
                Batch.from_str("batch 2:2; 3xpinapple, 4xcherry")
            ]
        )
    BatchCollection(seller = "seller1", batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3), Item_in_batch(name='banana', quantity_in_batch=5)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='pinapple', quantity_in_batch=3), Item_in_batch(name='cherry', quantity_in_batch=4)])])

    Or,

    >>> BatchCollection.from_str(
        "batch 1:1; 2xapple, 3xorange, 5xbanana",
        "batch 2:2; 3xpinapple, 4xcherry",
        seller = "seller1"
    )
    BatchCollection(seller = "seller1", batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3), Item_in_batch(name='banana', quantity_in_batch=5)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='pinapple', quantity_in_batch=3), Item_in_batch(name='cherry', quantity_in_batch=4)])])

    Thanks to print, we can display the batches in a readable way

    >>> batch =  BatchCollection(
            seller = "seller1",
            batch_list = [
                Batch(
                    name = "batch 1",
                    price = 1,
                    items = [
                        Item_in_batch("apple", 1),
                        Item_in_batch("orange", 2)
                    ]
                ),
                Batch(
                    name = "batch 2",
                    price = 2,
                    items = [
                        Item_in_batch("apple", 3),
                        Item_in_batch("orange", 4)
                    ]
                )
            ]
        )
    >>> print(batch)
    Batch : batch 1 - Price : 1
    +-----------------+----------+
    |   Item name     | Quantity |
    +-----------------+----------+
    |     apple      |    1     |
    |     orange      |    2     |
    +-----------------+----------+
    Lot : batch 2 - Prix : 2
    +-----------------+----------+
    |   Item name     | Quantity |
    +-----------------+----------+
    |     apple      |    3     |
    |     orange      |    4     |
    +-----------------+----------+

    If the batches contain weapons not present in other batches, they are added with a quantity of 0 :

    >>> BatchCollection.from_str(
        "batch 1:1; 2xapple, 3xorange, 5xbanana",
        "batch 2:2; 3xpinapple, 4xcherry",
        seller = "seller1"
    )
    BatchCollection(seller = "seller1", batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3), Item_in_batch(name='banana', quantity_in_batch=5)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='pinapple', quantity_in_batch=3), Item_in_batch(name='cherry', quantity_in_batch=4)])])

    The names of the batches must be unique :

    >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 1", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])])
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
    ValueError: The name of the batch 'batch 1' is not unique.

    Attention, all the batch_list elements must be of type Batch :

    >>> BatchCollection(seller = "seller1", batch_list = ["batch 1", "batch 2"])
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<@beartype(batches_optimization.lib_batches.BatchCollection.__init__) at 0x20d788662a0>", line 63, in __init__
    File "<string>", line 5, in __init__
    in __post_init__
        raise TypeError(f"Expected all elements in 'batch_list' to be of type 'Batch', but got '{type(batch).__name__}'.")
    TypeError: Expected all elements in 'batch_list' to be of type 'Batch', but got 'str'.
    """

    batch_list: list[Batch] = field(default_factory=list)
    seller: str = "Default seller"

    def __post_init__(self):
        """Checks if the list of batches is valid."""

        if len(self) > 0:
            batch_name_already_seen = set()
            for batch in self.batch_list:
                if batch.name not in batch_name_already_seen:
                    batch_name_already_seen.add(batch.name)
                else:
                    raise ValueError(
                        f"The name of the batch '{batch.name}' is not unique."
                    )

            all_items_name = [
                item.name for batch in self.batch_list for item in batch.items
            ]

            counter = 0
            for batch in self.batch_list:
                for item_name in all_items_name:
                    if item_name not in [item.name for item in batch.items]:
                        batch.items.append(Item_in_batch(item_name, 0.0))
                        counter += 1

            if counter > 0:
                warnings.warn(
                    "Some batches contain weapons not present in other batches. They have been added with a quantity of 0."
                )

            for item_name in all_items_name:
                item_list_name = np.array(
                    [
                        item.quantity_in_batch == 0
                        for batch in self
                        for item in batch
                        if item.name == item_name
                    ]
                )
                if all(item_list_name):
                    for batch in self:
                        batch.remove_item(item_name=item_name)

    def __str__(self) -> str:
        """Prints the batch collection in a readable way with print()."""

        str_seller = f"Seller : {self.seller}\n"
        return str_seller + "\n".join([str(batch) for batch in self.batch_list])

    def __getitem__(self, index: int | str) -> str | Batch | list[Batch]:
        """Returns the seller or the batch at the specified index.

        Args :
        - index : int | str : index of the batch

        Returns :
        - str | Batch : seller or batch

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection["seller"]
        'seller1'

        >>> batch_collection["batch_list"]
        [Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)])]

        >>> batch_collection[0]
        Batch(name='batch 1', price=1, items= [Item_in_batch(name='apple',quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)])

        >>> batch_collection[1]
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)])
        """

        if index == "seller":
            return self.seller
        elif index == "batch_list":
            return self.batch_list
        elif isinstance(index, int):
            return self.batch_list[index]
        elif isinstance(index, str):
            raise KeyError(f"Key '{index}' not found.")
        else:
            raise IndexError("Index is out of range.")

    def __iter__(self) -> Iterator[Batch]:
        """Returns an iterator over the batches.

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> for batch in batch_collection:
        ...    batch
        Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)])
        Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)])
        """

        return iter(self.batch_list)

    def __len__(self) -> int:
        """Returns the number of batches in the BatchCollection.

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> len(batch_collection)
        2
        """

        return len(self.batch_list)

    def __contains__(self, batch_name: str) -> bool:
        """Returns True if the batch is in the BatchCollection, False otherwise.

        Args :
        - batch_name : str : name of the batch

        Returns :
        - bool : True if the batch is in the BatchCollection, False otherwise

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> "batch 1" in batch_collection
        True

        >>> "batch 3" in batch_collection
        False
        """

        for batch in self.batch_list:
            if batch.name == batch_name:
                return True
        return False

    def __hash__(self):
        """Returns the hash of the BatchCollection object."""

        return hash((self.seller, tuple(self.batch_list)))

    def __add__(self, other: "BatchCollection") -> "BatchCollection":
        """Returns a new BatchCollection object with the batches of the two BatchCollection objects.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - BatchCollection : new BatchCollection object with the batches of the two BatchCollection objects

        Example :

        >>> batch_collection1 = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection2 = BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")

        >>> batch_collection1 + batch_collection2
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), Batch(name='batch 4', price=4, items=[Item_in_batch(name='apple', quantity_in_batch=7), Item_in_batch(name='orange', quantity_in_batch=8)])], seller='seller1')

        if the two BatchCollection objects have different sellers, the seller of the new BatchCollection object is the concatenation of the two sellers :

        if the two BatchCollection have a same name for one of their batches, the name of the batch in the new BatchCollection object is renamed with the name of its seller :

        >>> batch_collection1 = BatchCollection(seller = "seller1", batch_list = [Batch(name = "batch 1", price = 1, items = [Item_in_batch(name = "apple", quantity_in_batch = 1), Item_in_batch(name = "orange", quantity_in_batch = 2)])])
        >>> batch_collection2 = BatchCollection(seller = "seller2", batch_list = [Batch(name = "batch 1", price = 1, items = [Item_in_batch(name = "apple", quantity_in_batch = 3), Item_in_batch(name = "orange", quantity_in_batch = 4)])])
        >>> batch_collection1 + batch_collection2
        """

        new_collection = BatchCollection(
            batch_list=self.batch_list.copy(), seller=self.seller
        )

        if self.seller != other.seller:
            new_collection.seller = f"{self.seller} + {other.seller}"

        for other_batch in other.batch_list:
            for new_batch in new_collection.batch_list:
                if new_batch.name == other_batch.name:
                    other_batch.name += f" from {other.seller}"
                    break
            new_collection.batch_list.append(other_batch)
        new_collection.__post_init__()
        return new_collection

    def __eq__(self, other: object) -> bool:
        """Returns True if the two BatchCollection objects are the same.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the two BatchCollection objects are the same

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") == BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        True

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") == BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")
        False
        """

        if not isinstance(other, BatchCollection):
            return NotImplemented

        return self.batch_list == other.batch_list and self.seller == other.seller

    def __ne__(self, other: object):
        """Returns True if the two BatchCollection objects are different, False otherwise.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the two BatchCollection objects are different, False otherwise

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") != BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        False

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") != BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")
        True
        """

        if not isinstance(other, BatchCollection):
            return NotImplemented

        return self.batch_list != other.batch_list or self.seller != other.seller

    def __lt__(self, other: "BatchCollection"):
        """Returns True if the first BatchCollection have less batches than the second BatchCollection, False otherwise.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the first BatchCollection have less batches than the second BatchCollection, False otherwise

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") < BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        False

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") < BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")
        True
        """

        return len(self) < len(other)

    def __le__(self, other: "BatchCollection"):
        """Returns True if the first BatchCollection object have less batches than or equal to the second BatchCollection object, False otherwise.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the first BatchCollection object have less batches than or equal to the second BatchCollection object, False otherwise

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") <= BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        True
        """

        return len(self) <= len(other)

    def __gt__(self, other: "BatchCollection"):
        """Returns True if the first BatchCollection object have more batches than the second BatchCollection object, False otherwise.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the first BatchCollection object have more batches than the second BatchCollection object, False otherwise

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") > BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        False
        """

        return len(self) > len(other)

    def __ge__(self, other: "BatchCollection"):
        """Returns True if the first BatchCollection object have more batches than or equal to the second BatchCollection object, False otherwise.

        Args :
        - other : BatchCollection : other BatchCollection object

        Returns :
        - bool : True if the first BatchCollection object have more batches than or equal to the second BatchCollection object, False otherwise

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1") >= BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")
        True
        """

        return len(self) >= len(other)

    @classmethod
    def from_str(
        cls,
        *strings: str,
        seller: str = "Default seller",
    ) -> "BatchCollection":
        """Creates a batch collection from a string.

        Args :
        - strings : str : strings representing the batches
        - seller : str : name of the seller

        Returns :
        - BatchCollection : BatchCollection object

        Example :

        >>> BatchCollection.from_str(
            "batch 1:1; 2xapple, 3xorange, 5xbanana",
            "batch 2:2; 3xpinapple, 4xcherry",
            seller = "seller1"
        )
        BatchCollection(seller = "seller1", batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2), Item_in_batch(name='orange', quantity_in_batch=3), Item_in_batch(name='banana', quantity_in_batch=5)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='pinapple', quantity_in_batch=3), Item_in_batch(name='cherry', quantity_in_batch=4)])])
        """

        batch_list = [Batch.from_str(string) for string in strings]
        return cls(batch_list, seller)

    def are_equal(self, other: "BatchCollection") -> bool:
        """Returns True if the two BatchCollection objects have the same batch but in different order.

        Args :
        - other : BatchCollection : other BatchCollection object
        - bool : True if the two BatchCollection objects have the same batch but in different order

        Example :

        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1").are_equal(BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"))
        True


        >>> BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1").are_equal(BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller2"))
        False
        """

        return set(self.batch_list) == set(other.batch_list)

    def add_batch(self, *batch: Batch) -> "BatchCollection":
        """Adds a batch or a list of batches to the list of batches in the BatchCollection.

        Args :
        - batch : Batch : batch to add, it can be a list of batches

        Returns :
        - BatchCollection : BatchCollection with the added batch

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection.add_batch(Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]))
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), seller='seller1')

        You can also add several batches at the same time :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection.add_batch(Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)]))
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), Batch(name='batch 4', price=4, items=[Item_in_batch(name='apple', quantity_in_batch=7), Item_in_batch(name='orange', quantity_in_batch=8)]), seller='seller1')

        Attention, if the name of the batch is not unique, the function will raise an error :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection.add_batch(Batch("batch 1", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]))
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<string>", line 5, in __init__
        ValueError: The name of the batch 'batch 1' is not unique.
        """

        for b in batch:
            if b.name in [batch.name for batch in self.batch_list]:
                raise ValueError(f"The name of the batch '{b.name}' is not unique.")
            self.batch_list.append(b)
        self.__post_init__()
        return self

    def remove_batch(self, *index: int, **batch_name: str) -> "BatchCollection":
        """Removes a batch from the list of batches in the BatchCollection.

        Args :
        - index : int : index of the batch to remove
        - batch_name : str : name of the batch to remove

        Returns :
        - BatchCollection : BatchCollection with the removed batch

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 3", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.remove_batch(0)
        BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), Batch(name='batch 3', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1')

        You can also remove several batches at the same time :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 3", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.remove_batch(0, 2)
        BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')

        You can also remove a batch by its name :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 3", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.remove_batch(batch_name="batch 1")
        BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), Batch(name='batch 3', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1')

        You can also remove several batches by their name :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 3", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.remove_batch(batch_name="batch 1", batch3 = "batch 3"})
        BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')
        """

        if index:
            indices = sorted(index, reverse=True)
            for i in indices:
                self.batch_list.pop(i)
            self.__post_init__()

        if batch_name:
            names = (
                batch_name.values() if isinstance(batch_name, dict) else [batch_name]
            )
            for name in names:
                self.batch_list = [
                    batch for batch in self.batch_list if batch.name != name
                ]
            self.__post_init__()

        return self

    def find(
        self, batch_name: str | None = None, batch_price: float | int | None = None
    ) -> int | list[int] | None:
        """Returns the batch corresponding to the batch name or to the batch_price.

        Args :
        - batch_name : str : name of the batch
        - batch_price : float | int : price of the batch

        Returns :
        - int | list[int] | None : index of the batch

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 3", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.find(batch_name="batch 1")
        0

        >>> batch_collection.find(batch_price=2)
        1

        if there are several batches with the same price, the function returns a list of indexes :
        >>> batch_collection.find(batch_price=1)
        [0, 2]
        """

        if batch_name:
            for index, batch in enumerate(self):
                if batch.name == batch_name:
                    return index
            return None
        elif batch_price:
            liste_of_index_with_same_price = [
                index for index, batch in enumerate(self) if batch.price == batch_price
            ]
            if len(liste_of_index_with_same_price) == 1:
                return liste_of_index_with_same_price[0]
            else:
                return liste_of_index_with_same_price
        else:
            raise ValueError("You must specify a valid batch name or a batch price.")

    def sort(self, by: str = "name", reverse: bool = False) -> "BatchCollection":
        """Sorts the batches in the BatchCollection by name or by price.

        Args :
        - by : str : "name" or "price"

        Returns :
        - BatchCollection : BatchCollection with the sorted batches

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.sort(by="name")
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')

        >>> batch_collection = BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)]), Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")

        >>> batch_collection.sort(by="price")
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')
        """

        if by == "name":
            self.batch_list.sort(
                key=lambda x: x.name if x.name else "", reverse=reverse
            )
        elif by == "price":
            self.batch_list.sort(
                key=lambda x: x.price if x.price else 0, reverse=reverse
            )
        return self

    def to_json(self, path: str = "batch_collection.json"):
        """Returns the BatchCollection object in json format.

        Returns :
        - str : BatchCollection object in json format

        Example :

        >>> batch_collection = BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")

        >>> batch_collection.to_json()
        """
        try:
            with open(path, "w") as file:
                json.dump(self, file, default=lambda o: o.__dict__, indent=4)
        except Exception as error:
            raise error

    @classmethod
    def from_json(cls, path: str) -> "BatchCollection":
        """Creates a BatchCollection object from a json file.

        Args :
        - path : str : path of the json file

        Returns :
        - BatchCollection : BatchCollection object

        Example :

        >>> batch_collection = BatchCollection.from_json("batch_collection.json")
        >>> batch_collection
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')
        """
        try:
            with open(path, "r") as file:
                json_bc = json.load(file)

            bc = BatchCollection()
            bc.seller = json_bc["seller"]
            for batch in json_bc["batch_list"]:
                item = []
                batch_name = batch["name"]
                batch_price = batch["price"]
                for batch_item in batch["items"]:
                    item.append(
                        Item_in_batch(
                            batch_item["name"], batch_item["quantity_in_batch"]
                        )
                    )
                batch = Batch(name=batch_name, price=batch_price, items=item)
                bc.add_batch(batch)
            bc.__post_init__()
            return bc
        except Exception as error:
            raise error


@serde
@dataclass
class BatchLists:
    """Dataclass which allows to store several BatchCollection objects in a list.

    Args:
    - batchlists: list[BatchCollection] : list of BatchCollection objects.

    Returns:
    - BatchLists : list of BatchCollection objects.

    Raises:
        - ValueError: if the data is not a list of BatchCollection objects.
        - ValueError: if the name of the seller is not unique.


    Example :

    You can create a BatchLists object like this :

    >>> batch_lists = BatchLists(
            batchlists = [
                BatchCollection(
                    seller = "seller1",
                    batch_list = [
                        Batch(
                            name = "batch 1",
                            price = 1,
                            items = [
                                Item_in_batch("apple", 1),
                                Item_in_batch("orange", 2)
                            ]
                        ),
                        Batch(
                            name = "batch 2",
                            price = 2,
                            items = [
                                Item_in_batch("apple", 3),
                                Item_in_batch("orange", 4)
                            ]
                        )
                    ],
                ),
                BatchCollection(
                    seller = "seller2",
                    batch_list = [
                        Batch(
                            name = "batch 1",
                            price = 1,
                            items = [
                                Item_in_batch("apple", 1),
                                Item_in_batch("orange", 2)]),
                        Batch(
                            name = "batch 2",
                            price = 2,
                            items = [
                                Item_in_batch("apple", 3),
                                Item_in_batch("orange", 4)
                            ]
                        )
                    ],
                )
            ]
        )
    BatchLists(batchlists=[BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])

    The best way to create a BatchLists object is to use the BatchLists from_str method:
    Example :

    >>> batch_lists = BatchLists.from_str(
            strings = [
                "seller1:batch 1:1; 1xapple, 2xorange",
                "seller1:batch 2:2; 3xapple, 4xorange",
                "seller2:batch 1:1; 1xapple, 2xorange",
                "seller2:batch 2:2; 3xapple, 4xorange"
            ]
        )

    >>> batch_lists
    BatchLists(batchlists=[BatchCollection(batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1'), BatchCollection(batch_list=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])


    You can display the object with print():

    >>> print(batch_lists)
    seller1:
    Batch : batch 1 - Price : 1
    +-----------+----------+
    | Item name | Quantity |
    +-----------+----------+
    |   apple  |    1     |
    |   orange  |    2     |
    +-----------+----------+
    Batch : batch 2 - Price : 2
    +-----------+----------+
    | Item name | Quantity |
    +-----------+----------+
    |   apple  |    3     |
    |   orange  |    4     |
    +-----------+----------+
    seller2:
    Batch : batch 1 - Price : 1
    +-----------+----------+
    | Item name | Quantity |
    +-----------+----------+
    |   apple  |    1     |
    |   orange  |    2     |
    +-----------+----------+
    Batch : batch 2 - Price : 2
    +-----------+----------+
    | Item name | Quantity |
    +-----------+----------+
    |   apple  |    3     |
    |   orange  |    4     |
    +-----------+----------+

    Attention, the data must be a list of BatchCollection objects :

    >>> BatchLists([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])])

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<string>", line 5, in __init__
        raise TypeError(f"Expected all elements in 'batchlists' to be of type 'BatchCollection', but got '{type(batches).__name__}'.")
    TypeError: Expected all elements in 'batchlists' to be of type 'BatchCollection', but got 'str'.

    Attention, the name of the seller must be unique :
    if you try to create a BatchLists object with two BatchCollection objects with the same seller name, the function will merge the two BatchCollection objects into one :
    """

    batchlists: list[BatchCollection] = field(default_factory=list)

    def __post_init__(self):
        """Checks if the data is a list of BatchCollection objects and if the name of the seller is unique."""

        if len(self) > 0:
            all_items_name = {
                item.name for batches in self for batch in batches for item in batch
            }

            seller_to_batches = {}
            for batches in self:
                if batches.seller not in seller_to_batches:
                    seller_to_batches[batches.seller] = batches
                else:
                    seller_to_batches[batches.seller].add_batch(
                        [batch for batch in batches]
                    )

            self.batch_collections = list(seller_to_batches.values())

            for batches in self:
                for batch in batches:
                    for item_name in all_items_name:
                        if item_name not in [item.name for item in batch.items]:
                            batch.items.append(Item_in_batch(item_name, 0.0))

    def __str__(self) -> str:
        """Prints the batchlists in a readable way with print()."""

        return "\n".join(f"{batches.seller}:\n{batches}" for batches in self.batchlists)

    def __getitem__(
        self, index: int | str | None
    ) -> BatchCollection | list[BatchCollection] | None:
        """Returns the seller or the batchlists at the specified index.

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists["batchlists"]
        [BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')]

        >>> batch_lists[0]
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')

        >>> batch_lists[1]
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')
        """

        if index == "batchlists":
            return self.batchlists
        elif isinstance(index, int):
            return self.batchlists[index]
        elif isinstance(index, str):
            for batches in self:
                if batches.seller == index:
                    return batches
            else:
                raise KeyError(f"Key '{index}' not found.")
        else:
            return None

    def __iter__(self) -> Iterator[BatchCollection]:
        """Returns an iterator over the batchlists.

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> for batches in batch_lists:
        ...    batches
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1')
        BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')
        """

        return iter(self.batchlists)

    def __len__(self) -> int:
        """Returns the number of batch collections in the BatchLists.

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> len(batch_lists)
        2
        """

        return len(self.batchlists)

    def __contains__(self, seller: str) -> bool:
        """Returns True if the seller is in the BatchLists, False otherwise.

        Args :
        - seller : str : name of the seller

        Returns :
        - bool : True if the seller is in the BatchLists, False otherwise

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> "seller1" in batch_lists
        True
        >>> "seller3" in batch_lists
        False
        """

        for batch_collection in self:
            if batch_collection.seller == seller:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if the two BatchLists objects are the same.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the two BatchLists objects are the same, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists1 == batch_lists2
        True
        """

        if not isinstance(other, BatchLists):
            return NotImplemented

        return self.batchlists == other.batchlists

    def __ne__(self, other: object) -> bool:
        """Returns True if the two BatchLists objects are different, False otherwise.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the two BatchLists objects are different, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists1 != batch_lists2
        False
        """

        if not isinstance(other, BatchLists):
            return NotImplemented

        return self.batchlists != other.batchlists

    def __lt__(self, other: "BatchLists") -> bool:
        """Returns True if the first BatchLists object has less batch collections than the second BatchLists object, False otherwise.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the first BatchLists object has less batch collections than the second BatchLists object, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")])

        >>> batch_lists1 < batch_lists2
        False
        """

        return len(self) < len(other)

    def __le__(self, other: "BatchLists") -> bool:
        """Returns True if the first BatchLists object has less batch collections than or equal to the second BatchLists object, False otherwise.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the first BatchLists object has less batch collections than or equal to the second BatchLists object, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")])

        >>> batch_lists1 <= batch_lists2
        False
        """

        return len(self) <= len(other)

    def __gt__(self, other: "BatchLists") -> bool:
        """Returns True if the first BatchLists object has more batch collections than the second BatchLists object, False otherwise.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the first BatchLists object has more batch collections than the second BatchLists object, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")])

        >>> batch_lists1 > batch_lists2
        True
        """

        return len(self) > len(other)

    def __ge__(self, other: "BatchLists") -> bool:
        """Returns True if the first BatchLists object has more batch collections than or equal to the second BatchLists object, False otherwise.

        Args :
        - other : BatchLists : other BatchLists object

        Returns :
        - bool : True if the first BatchLists object has more batch collections than or equal to the second BatchLists object, False otherwise

        Example :

        >>> batch_lists1 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1"), BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)]), Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller2")])

        >>> batch_lists2 = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)]), Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller1")])

        >>> batch_lists1 >= batch_lists2
        True
        """

        return len(self) >= len(other)

    def __hash__(self):
        """Returns the hash of the BatchLists object."""

        return hash(tuple(self.batchlists))

    @classmethod
    def from_str(cls, strings: list[str] | str) -> "BatchLists":
        """Crée un objet BatchLists à partir d'une liste de chaînes de caractères.

        Args :
        - data : List[str] : liste de chaînes de caractères à convertir

        Returns :
        - BatchLists : objet BatchLists

        Exemple :

        >>> Batchlists.from_str(
                strings=[
                    "seller1_batch 1:1; 2xapple,
                    "seller1_batch 2:2; 3xapple, 4xorange",
                    "seller2_batch 3:3; 5xapple, 6xorange",
                    "seller2_batch 4:4; 7xapple, 8xorange"
                ]
            )
        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=2)]), Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), Batch(name='batch 4', price=4, items=[Item_in_batch(name='apple', quantity_in_batch=7), Item_in_batch(name='orange', quantity_in_batch=8)]), seller='seller2')])
        """

        seller_to_batches = {}
        strings = strings if isinstance(strings, list) else [strings]
        for string in strings:
            seller, batch = string.split("_")
            if seller not in seller_to_batches:
                seller_to_batches[seller] = BatchCollection.from_str(
                    batch, seller=seller
                )
            else:
                seller_to_batches[seller].add_batch(Batch.from_str(batch))

        return cls(list(seller_to_batches.values()))

    def add_BatchCollection(
        self, batch_collection: BatchCollection | list[BatchCollection]
    ) -> "BatchLists":
        """Adds a batch collection or a list of batch collection to the list of batch collections in the BatchLists.

        Args :
        - batch_collection : BatchCollection | list[BatchCollection] : BatchCollection or list of BatchCollection to add

        Returns :
        - BatchLists : BatchLists object with the new batch collection added

        Raises :
        - TypeError : if the data is not a BatchCollection object
        - ValueError : if the name of the seller is not unique

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.append(BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)])], "seller3"))

        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2'), BatchCollection(batches=[Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), seller='seller3')])

        You can also add a list of BatchCollection objects :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.append([BatchCollection([Batch("batch 3", 3, [Item_in_batch("apple", 5), Item_in_batch("orange", 6)])], "seller3"), BatchCollection([Batch("batch 4", 4, [Item_in_batch("apple", 7), Item_in_batch("orange", 8)])], "seller4")])
        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2'), BatchCollection(batches=[Batch(name='batch 3', price=3, items=[Item_in_batch(name='apple', quantity_in_batch=5), Item_in_batch(name='orange', quantity_in_batch=6)]), seller='seller3'), BatchCollection(batches=[Batch(name='batch 4', price=4, items=[Item_in_batch(name='apple', quantity_in_batch=7), Item_in_batch(name='orange', quantity_in_batch=8)]), seller='seller4')])
        """

        batch_collection = (
            [batch_collection]
            if not isinstance(batch_collection, list)
            else batch_collection
        )

        for bc in batch_collection:
            if bc.seller in [batches.seller for batches in self]:
                for batch in bc:
                    existing_batch_names = [
                        batch.name
                        for batches in self
                        for batch in batches
                        if batches.seller == bc.seller
                    ]
                    if batch.name in existing_batch_names:
                        raise ValueError(
                            f"The combination of the seller {bc.seller} and the batch name {batch.name} is not unique."
                        )
                    else:
                        batch_collection_to_update = self[self.find(seller=bc.seller)]
                        if isinstance(batch_collection_to_update, BatchCollection):
                            batch_collection_to_update.add_batch(batch)
            else:
                self.batchlists.append(bc)
        self.__post_init__()

        return self

    def remove_BatchCollection(
        self, index: int | list[int] | None = None, seller_name: str | None = None
    ) -> "BatchLists":
        """Removes a batch collection from the list of batch collections in the BatchLists.

        Args :
        - index : int : index of the batch collection to remove
        - seller_name : str : name of the seller of the batch collection to remove

        Returns :
        - BatchLists : BatchLists object with the batch collection removed

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.remove(index=0)
        BatchLists([BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.remove(seller_name="seller1")
        BatchLists([BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])


        You can also remove a list of BatchCollection objects :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])
        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])
        """

        if index is not None:
            index = [index] if isinstance(index, int) else sorted(index, reverse=True)
            for i in index:
                if isinstance(i, int):
                    self.batchlists.pop(i)
            return self
        elif seller_name:
            for batch_collection in self:
                if batch_collection.seller == seller_name:
                    self.batchlists.remove(batch_collection)
            return self
        else:
            return self

    def find(self, seller: str) -> int | None:
        """Returns the batch collection corresponding to the seller.

        Args :
        - seller : str : name of the seller

        Returns :
        - int | None : index of the batch collection corresponding to the seller, None if the seller is not in the BatchLists

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.find("seller1")
        0
        >>> batch_lists.find("seller3")
        None
        """

        for index, batch_collection in enumerate(self):
            if batch_collection.seller == seller:
                return index
        return None

    def sort(self, by: str = "seller", reverse: bool = False) -> "BatchLists":
        """Sorts the batch collections in the BatchLists by seller.

        Args :
        - by : str : "seller" to sort by seller, "number_of_batches" to sort by number of batches
        - reverse : bool : True to sort in descending order, False to sort in ascending order

        Returns :
        - BatchLists : BatchLists object with the batch collections sorted

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")])

        >>> batch_lists.sort(by="seller")
        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2')])

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")])

        >>> batch_lists.sort(by="number_of_batches", reverse=True)
        BatchLists([BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2'), BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1')])

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2"), BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1")])

        >>> batch_lists.sort(by="number_of_batches", reverse=False)
        BatchLists([BatchCollection(batches=[Batch(name='batch 1', price=1, items=[Item_in_batch(name='apple', quantity_in_batch=1), Item_in_batch(name='orange', quantity_in_batch=2)]), seller='seller1'), BatchCollection(batches=[Batch(name='batch 2', price=2, items=[Item_in_batch(name='apple', quantity_in_batch=3), Item_in_batch(name='orange', quantity_in_batch=4)]), seller='seller2'])
        """

        if by == "seller":
            self.batchlists.sort(
                key=lambda x: x.seller if x.seller else "", reverse=reverse
            )
            return self
        elif by == "number_of_batches":
            self.batchlists.sort(key=lambda x: len(x) if x else 0, reverse=reverse)
            return self
        else:
            raise ValueError(
                "The 'by' parameter must be 'seller' or 'number_of_batches'."
            )

    def to_json(self, path: str = "batchlists.json") -> None:
        """Saves the BatchLists object in a JSON file.

        Args :
        - path : str : path to the JSON file

        Example :

        >>> batch_lists = BatchLists([BatchCollection([Batch("batch 1", 1, [Item_in_batch("apple", 1), Item_in_batch("orange", 2)])], "seller1"), BatchCollection([Batch("batch 2", 2, [Item_in_batch("apple", 3), Item_in_batch("orange", 4)])], "seller2")])

        >>> batch_lists.to_json("batchlists.json")
        """
        try:
            with open(path, "w") as file:
                json.dump(self.batchlists, file, default=lambda o: o.__dict__, indent=4)
        except Exception as error:
            raise error

    @classmethod
    def from_json(cls, path: str = "batchlists.json") -> "BatchLists":
        """Loads the BatchLists object from a JSON file.

        Args :
        - path : str : path to the JSON file

        Returns :
        - BatchLists : BatchLists object

        Example :

        >>> batch_lists = BatchLists().from_json("batchlists.json")
        """

        try:
            with open(path, "r") as file:
                json_bl = json.load(file)

            bl = BatchLists()
            for batches in json_bl:
                bc = BatchCollection(seller=batches["seller"])
                for batch in batches["batch_list"]:
                    batch_to_add = Batch(
                        name=batch["name"], price=batch["price"], items=[]
                    )
                    items = []
                    for batch_item in batch["items"]:
                        items.append(
                            Item_in_batch(
                                batch_item["name"], batch_item["quantity_in_batch"]
                            )
                        )
                    batch_to_add.items = items
                    bc.add_batch(batch_to_add)
                if isinstance(bc, BatchCollection):
                    bl.add_BatchCollection(bc)
            bl.__post_init__()
            return bl
        except Exception as error:
            raise error
