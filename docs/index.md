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

## Build existing project

To build existing project run `doge` script with build task name (usually `build`):
```sh
doge build
```

## Add dependency

To add dependency to folder use `folder` function from `dogebuild.dependencies`

```python
from dogebuild.dependencies import dependencies, folder

dependencies(
    folder('../module')
)
```

To add dependency to external git repository use `git` function from `dogebuild.dependencies`

```python
from dogebuild.dependencies import dependencies, git

dependencies(
    git('git@github.com:dogebuild/test.git')
)
```
