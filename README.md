<p align="center">
  <img src="presentation\Batch_Monitor.png" alt="Logo de mon projet" width="200" height="200">
</p>

# BatchMonitor 

BatchMonitor is a library that allows you to solve problems related to linear programming. It's designed to be easy to use and to provide a simple interface. You can use it to solve problems in a variety of domains, such as logistics, and manufacturing.   

This library come with a streamlined API that allows you to quickly build and solve optimization problems. It also provides a set of tools and options to help you analyze and visualize the results of your optimization problems.

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

# API appel

```python
python -m streamlit run BatchMonitor.py
```

![](presentation/presentation-gif.gif)