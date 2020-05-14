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
from dogebuild_c.c_plugin import CPlugin, BinaryType
from dogebuild.dogefile_internals.dependencies import dependencies, folder

dependencies(
    folder('../dependency')
)

CPlugin(
    type=BinaryType.EXECUTABLE,
    out='hello',
    src_dir='.',
    src=[
        'main.c',
    ],
)
```

To run task simply pass task name as argument to doge script.
`doge build` will run `build` task and all dependencies.
You can also run multiple tasks: `doge clean build`.
