# dogebuild

[![Build Status](https://travis-ci.org/dogebuild/dogebuild.svg?branch=master)](https://travis-ci.org/dogebuild/dogebuild)
[![PyPI version](https://badge.fury.io/py/dogebuild.svg)](https://badge.fury.io/py/dogebuild)
[![Documentation Status](https://readthedocs.org/projects/dogebuild/badge/?version=latest)](https://dogebuild.readthedocs.io/en/latest/?badge=latest)

General purpose build manager mainly designed to build C++ projects which
uses directed acyclic graph (DAG) to manage tasks dependencies.

## Install

```sh
pip install dogebuild
```

## How to use

Dogebuild uses `dogefile.py` to describe project structure and task DAG.
An example of `dogefile.py`:

```python
from dogebuild import make_mode, task

make_mode()


@task
def task1():
    print("task1")


@task()
def task2():
    print("task2")


@task(
    aliases=["Task 3 verbose name"], depends=["task1", "task2"],
)
def task3():
    print("task3")


@task(depends=["Task 3 verbose name"], aliases=["build"])
def task4():
    print("task4")

```

To run task simply pass task name as argument to doge script.
`doge build` will run `build` task and all dependencies.
You can also run multiple tasks: `doge task1 task2`.

For more advanced use see plugins section.

## Plugins

Plugins allow to hide low-level mechanics of build from user. 
See how to use plugins in plugin documentation.

### Language plugins:

#### C/C++

- [dogebuild-c](https://github.com/dogebuild/dogebuild-c) - a C/C++ build plugin
