# Sorting Algorithm Visualizer

## Purpose

This has been a fun project of mine to help visualize the inner workings of sorting algorithms. It is a fun mental exercise to write these algorithms in an iterable fashion version a 'method' implementation.

## Description



The BubbleSort, HeapSort, and QuickSort have been added to show the number of compare operations as well as time-to-completion relative to each algorithm.

## Installation

Use a virtual environment if you like. Just need to enter the folling items in the command line:

```
> git clone https://github.com/ctimmins96/Sorting-Algorithm-Visualizer.git
> cd ./Sorting-Algorithm-Visualizer
> pip install -e .
```

Package is now available on PyPi! In can be installed doing the following:

```
> pip install timmins_sort
```

## Use

Once installed, enter the following in the command line:

```
> timmins-sorter
```

Alternatively, the project and be imported and run via the following:

```python
import timmins_sort

timmins_sort.run()
```