This Guide is here to help you understand how to use the BatchMonitor library. It will guide you through the different steps to follow to use the library in your project.

## Class objects

BatchMonitor is a library that allows you to solve optimization problems us. It is a simple and easy-to-use library that can be used to solve a wide range of optimization problems.

The chore of the library is made by the `Batch` class. It contains the following objects:

- **name**: the name of the batch
- **price** : the price of the batch
- and **items** which is a list that contains the subclass `Item_in_batch` with the following objects:
  - **name** the name of the item
  - **quantity_in_batch**: the quantity of the item in the batch

A Batch can contain as many items as you want.


Those batches are regrouped in a `BatchCollection` object. This object is used to create a collection of Batches, and to solve optimization problems on them. This object is defined by a **seller** which is a string that can be a name or a code.


Finally those `BatchCollection` objects are used to create a `BatchLists` object. Which is used to cover all your possibility


On the other side of the library, there is the `ItemRequest` class. This class is used to create item requests, as the name suggests. Specifically, an ItemRequest object contains :
 - name : the name of the item
 - a minimum and a maximum value (which can be None for the last one).


those ItemRequest are regrouped in a `ItemListRequest` class.

### Intern functions

*from_str* : function that allows you to create an object from string, all the objects of the library have this function

*add_items* : function that allows you to add items to a `batch` or to a `ItemListRequest`

*remove_items* : function that allows you to remove items from a `batch` or to a `ItemListRequest`

*find_item* : function that allows you to find an item in a `batch`

*find* : function that allows you to find a specific  `ItemListRequest`, `BatchCollection` or `BatchLists` object by a specific object (item, Batch Name, etc. it depend on the object you are looking for)

*sort* : function that allows you to sort a `batch`, a `ItemListRequest`, a `BatchCollection` or a `BatchLists` object by a specific object (item, Batch Name, etc. it depend on the object you are looking for)

*are_equal* : function that allow you to compare some `Batch` , some `BatchCollection` or even some `BatchLists` objects to see if they have the same items

*to_json* : function that allows you to convert a `ItemListRequest`,  `BatchCollection` and a `BatchLists` to a json file

*from_json* : function that allows you to appel a `ItemListRequest`,  `BatchCollection` and a `BatchLists` from a json file

*add_batch* : function that allows you to add a `Batch` to a `BatchCollection`

*remove_batch* : function that allows you to remove a `Batch` from a `BatchCollection`

*add_batchCollection* : function that allows you to add a `BatchCollection` to a `BatchLists`

*remove_batchCollection* : function that allows you to remove a `BatchCollection` from a `BatchLists`

## Functions

The two mains fonction of the library are `minBatchExpense`, which can be interpreted as a Primal, and `MaxEarnings`, which is the Dual of your problem. The engine for the resolution of the optimization problem is based on the PulP library.

You can specify quite a few parameters to the function apart from the batches and the demand list :
 - *category_of_variables* : which can be 'continuous' or 'integer'
 - *exchange_rate* : the exchange rate to apply to the price of the batch
 - *tax_rate* : the tax rate to apply to the price of the batch
 - *customs_duty* : the customs duty to apply to the price of the batch
 - *transport_fee* : the transport fee to apply to the price of the batch
 - *minimum_expense* (only for minBatchExpense) : The minimum expense the requester is willing to pay.
 - *maximum_expense* (only for minBatchExpense) : The maximum expense the requester is willing to pay.
 - *minimum_benefit* (only for MaxEarnings) : The minimum benefit the seller is willing to earn.
 - *maximum_benefit* (only for MaxEarnings) : The maximum benefit the seller is willing to earn.
 - *batch constraints* (only for minBatchExpense) : The constraints of the batches. You can specify a different constraint for each batch in the form of a dict('batch_name' = (minimum_quantity, maximum_quantity)).
 - *price constraints* (only for MaxEarnings): The constraints of the price. You can specify a different constraint for each item in the form of a dict('item_name' = (minimum_price, maximum_price)).


The package also contains a format library that allows you to print in your console the results of the optimization problem or the different object such as `BatchCollection` or `ItemListRequest` except for `Item_in_Batch` and `ItemRequest`.


## Quick exemple

The country of HEALTHYLAND wishes to increase its potential for healthy eating, it wants to acquire at least:

- 100,000 apples,
- 200,000 oranges,
- 100 watermelons,
- 400 bunches of bananas and as many pineapples.

To do this, they turn to a merchant of All_requested_items named FRUITVENDOR. This merchant collects the produce, used or not, from all the fields and farms.

These merchants offer 3 types of Batch_list (M$ = million dollars).

|                | Batch 1 | Batch 2 | Batch 3 |
| -------------- | ------- | ------- | ------- |
| Apples         | 500     | 300     | 800     |
| Oranges        | 1000    | 2000    | 1500    |
| Watermelons    | 10      | 20      | 15      |
| Bananas | 100 | 80      | 15      |
| Pineapples     | 80      | 120     | 200     |
| Costs of Batch_list | 10M$ | 12M$   | 15M$    |

- First, we have to create the `BatchCollection` object and the `ItemListRequest` object

```{python, include=FALSE}
from BatchMonitor import (
    BatchCollection,
    ItemListRequest,
    format_batch_collection,
    format_itemlistRequest,
    minBatchExpense,
    maxEarnings,
    format_maxEarnings,
    format_minBatchExpense,
    BatchLists,
    format_batch_lists
)
import numpy as np
```

```python
FRUITVENDOR_Batches = BatchCollection.from_str(
    "Batch 1:10000000; 500xApples, 1000xOranges, 10xWatermelons, 100xBananas, 80xPineapples",
    "Batch 2:12000000; 300xApples, 2000xOranges, 20xWatermelons, 80xBananas, 120xPineapples",
    "Batch 3:15000000; 800xApples, 1500xOranges, 15xWatermelons, 15xBananas, 200xPineapples",
    seller="FRUITVENDOR"
)
```
You can view the batches by printing the collection

```python
format_batch_collection(FRUITVENDOR_Batches)
```

Don't forget to create the demand list

```python
HEALTHYLAND_Request = ItemListRequest.from_str(
    "100000-inf of Apples",
    "200000-inf of Oranges",
    "100-inf of Watermelons",
    "400-inf of Bananas",
    "400-inf of Pineapples",
)
```
You can view the requested items by printing the demand list with format library that comes with the packages

```python
format_itemlistRequest(HEALTHYLAND_Request)
```

Now we can optimize the batch expenses for the HEALTHYLAND request

```python
result = minBatchExpense(
    batches=FRUITVENDOR_Batches,
    demand_list=HEALTHYLAND_Request,
)
```

You can use the following function to format the result

```python
format_minBatchExpense(result)
```
