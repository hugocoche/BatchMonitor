<p align="center">
  <img src="presentation\Batch_Monitor.png" alt="Logo de mon projet" width="200" height="200">
</p>

# BatchMonitor

The `BatchMonitor` module aims to solve the following problem ([link to the subject](resolution/Sujet.md)) and to extend this problem to as many situations as possible.

BatchMonitor is a library that allows you to solve problems related to linear programming. It's designed to be easy to use and to provide a simple interface. You can use it to solve problems in a variety of domains, such as logistics, and manufacturing.

This library come with a streamlined API that allows you to quickly build and solve optimization problems and a CLI Typer. It also provides a set of tools and options to help you analyze and visualize the results of your optimization problems.

This module enables the resolution of various types of problems. We refer to one as `MinBatchExpense`, which aims to minimize the consumer's expenditure on different batches supplied by one or more batch sellers. The other is `MaxEarnings`, designed to maximize the profit of a unitary arms merchant.

# Installation

```bash
pip install BatchMonitor
```
# Utilisation guide

The basis of the library is the `Batch` class. This class is used to create batches, as the name suggests. Specifically, a Batch object contains its name, a value, and a list of items, each of which has a name and a value (such as quantity, price, etc.).

Those Batches are regrouped in a `BatchCollection` object. This object is used to create a collection of Batches, and to solve optimization problems on them. This object is defined by a string such as a name or a code.

Finally those `BatchCollection` objects are used to create a `BatchLists` object. Which is used to cover all your possibility

On the other side, there is also the `ItemRequest` class. This class is used to create item requests, as the name suggests. Specifically, an ItemRequest object contains its name, a minimum and a maximum value (which can be None for the last one).

Those ItemRequest are regrouped in a `ItemListRequest` class.


# CLI

## Call the CLI

- If you've already installed the package, you will not need to initialize a virtual environnment to use the package
- In the other case
- Clone the package
```python
git clone https://github.com/hugocoche/BatchMonitor.git
```
- Open a terminal au dossier racine du package
```python
cd ./BatchMonitor
```
- Initialize a virtual environment
```
py -m poetry shell
```
- Install the depedencies
```python
py -m poetry install
```





- You can see the possible command :
```python
python -m BatchMonitor --help
```

![](presentation/help_typer.png)

- You have 2 options:
  - `init-and-run` is a function that will create all batch objects through prompts it will address to you;
  - `solve` assumes that you already have the objects in your possession.

### Init-and-run

```python
python -m BatchMonitor init-and-run --help
```
![](presentation/init-and-run_help.png)


### View

- `view` commands allows to visualize the object you provide with json file :

#### Best way to create the json object

![](presentation/create_json_files.png)

I recommend opening a terminal in the directory where your JSON files are located.

Now, we can view these objects.

```python
cd repertory/of/your/json/files
python -m BatchMonitor view-batches batch.json
python -m BatchMonitor view-ilr ilr.json
```

![](presentation/view_ex.gif)

### Solve

```python
python -m BatchMonitor solve --help
```
![](presentation/solve_help.png)


Now, you are able to resolve your problem.

```python
python -m BatchMonitor solve batch.json ilr.json
```

![](presentation/solve_ex.gif)



# API appel

```python
python -m BatchMonitor api
python -m streamlit run BatchMonitor\Welcome.py
```

![](presentation/presentation-gif.gif)

# Resolution

We have prepared an example of problem-solving using the package located [here](resolution/resolution_with_library.ipynb).

# Features


- Fully documented module for both public and private interfaces
- Code formatting by Black to adhere to PEP 8 standards
- Dependency management with Poetry
- Type checking with Mypy
- Creation of a command-line interface with Typer
- Development of a graphical user interface with Streamlit
- Unit and integration testing with Pytest, and test coverage with Pytest-cov

# Contributors

- [Gregory Jaillet](https://github.com/Greg-jllt)
- [Hugo Cochereau](https://github.com/hugocoche)
