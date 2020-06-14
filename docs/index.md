# Quick start

## What is dogebuild

Dogebuild is general purpose build manager designed to build C++ applications which uses
directed acyclic graph (DAG) to manage tasks dependencies.

## Install

You can install dogebuild with pip:
```sh
pip install dogebuild
```

## Start project

Project generation process was been excluded from dogebuild to [tapas scaffold tool]().
If tapas is not installed install it with:

```sh
pip install tapas
```

To create project template run

```sh
tapas <template-name>
```

and follow tapas instructions.

Selected template names:
- `dogebuild-c` - for C and C++ projects

## Simple manual solution

In case you didn't want to use any plugins, you can write `dogefile.py` from scratch.


## Build existing project

To build existing project run `doge` script with build task name (usually `build`):
```sh
doge build
```

## Add dependency

To add dependency to folder use `folder` function from `dogebuild.dependencies`

```python
from dogebuild.dogefile_internals.dependencies import dependencies, directory

dependencies(
    directory('../module')
)
```

To add dependency to external git repository use `git` function from `dogebuild.dependencies`

```python
from dogebuild.dogefile_internals.dependencies import dependencies, git

dependencies(
    git('git@github.com:dogebuild/test.git')
)
```
