This guide is here to help you use the streamlit application. It comes with a simple and easy-to-use interface that can be used to solve optimization problems. It contains 3 main pages (4 if you count the home page) :

## Demand Creation page

the Demand Creation page is here to help you create your demand list, it use the `ItemRequest` and `ItemListRequest` classes to create the demand list.

You have three options to create your demand list :
  - Firstly by manually adding the items you want to the list
  - Secondly by importing a csv/xlsx file that contains the items you want. (Note that you have to respect a certain structure, which is defined is the streamlit page)
  - Thirdly by importing a json file that contains the items you want. Note that the `ItemlistRequest` have intern functions that allow you create a json file with the demand list you have created directly in the typer or with the library in a python script.


The maximum quantity is optionnal its default is inf

### Exemple

- Create your ItemListRequest object and convert it into a json format

```python
item_list = ItemListRequest.from_str(
  "100000-inf of rifle",
  "200000-inf of grenade",
  "100-inf of tank",
  "400-inf of machinegun",
  "400-inf of bazooka"
)
item_list.to_json("demand_list.json")
```

- Now you can use your ItemListRequest object on the API

![](../presentation/demand_creation.gif)

## Batch Creation page

the Batch Creation page is here to help you create your batch list, it use the `Batch`, `BatchCollection` and `BatchLists` classes to create the batch list.

Like the Demand Creation page, you have three options to create your batch list :
  - Firstly by manually adding the batches you want to the list
  - Secondly by importing a csv/xlsx file that contains the batches you want (Note you have to respect a certain structure, which is defined is the streamlit page)
  - Thirdly by importing a json file that contains the batches you want. Note that `BatchLists` have intern functions, like the `ItemlistRequest`, that allow you create a json file with the batch list you have created directly in the typer or with the library in a python script.

### Example :

- Create your batch object and convert it into a json format
```python
batch = Batchlists.from_str(
  strings = [
    "Detailin_LOT1:10000000; 500xrifle, 1000xgrenade, 10xtank, 100xmachinegun, 80xbazooka",
    "Detailin_LOT1:12000000; 300xrifle, 2000xgrenade, 20xtank, 80xmachinegun, 120xbazooka",
    "Detailin_LOT1:15000000; 800xrifle, 1500xgrenade, 15xtank, 15xmachinegun, 200xbazooka"
  ]
)

batch.to_json("Batch_list.json")
```

- Now you can use your batch object on our API

![](../presentation/batch_creation.gif)

## Visualization page

The Visualization page is here to help you visualize the demand list and the batch list you have created and to see the result of the optimization problem.

There is a bunch of options that you can use to simulate different scenarios and see the result of the optimization problem. those options are the same as described in the sub section "Functions" in the [UTILISATION_GUIDE_LIBRARY](docs/UTILISATION_GUIDE_LIBRARY.md) file.
