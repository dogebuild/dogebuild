# Make mode

Make mode is a simple usage of dogebuild used to create python analog to [Makefile](https://en.wikipedia.org/wiki/Makefile).

## Simple example

```python
from dogebuild import make_mode, task

make_mode()

@task
def task1():
    print('task1')

@task()
def task2():
    print('task2')

@task(
    name='Task 3 verbose name',
    depends=['task1', 'task2'],
)
def task3():
    print('task3')

@task(depends=['Task 3 verbose name'])
def task4():
    print('task4')

```

`make_mode()` marks that dogefile should be run in make mode. 
All tasks must be marked with `@task` decorator to be added to build graph.
All dependencies must be enumerated as list in depends variable of `@task` decorator.

## More complex example

As far as dogefile is just a python script you can use all python power to run tasks:

```python

```
