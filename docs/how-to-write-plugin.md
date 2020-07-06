# Writing plugin

## Tapas

The easiest way to start plugin development is to use [dogebuild-plugin-tapa](https://github.com/tapas-scaffold-tool/dogebuild-plugin-tapa) 
from [tapas scaffold tool](https://github.com/tapas-scaffold-tool/tapas).

To install tapas run:

```shell script
pip install tapas
```

To generate scaffold for dogebuild plugin run:

```shell script
tapas dogebuild-plugin
```


## Creating class

First of all, create class that inherits `DogePlugin` class:

```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    pass
```

## Defining name of plugin

To distinguish tasks with the same name from different plugins each plugin must have unique name.
To define plugin name simply define `NAME` constant in plugin. 

```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'
```

Plugin name must match `[A-Za-z0-9_-]+` regexp.


## Defining tasks

Create methods, that will be represents the tasks of your plugin:

```python
from typing import Tuple, Dict
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def build_my_sources(self) -> Tuple[int, Dict]:
        # build sources
        exit_code = 0
        return exit_code, {'artifact-name': ['artifact-1-value', 'artifact-2-value']}
```

Methods may return tuple with return code and artifacts dictionary.
If no values are returned method considered successful and without any artifacts.
Keys are artifacts names and values are lists of artifacts values, usually values are path to files or directories.


## Use artifacts in task

To use artifacts from dependencies or from previous task pass artifact name as function parameter:

```python
from typing import Tuple, Dict, List
from pathlib import Path
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def generate_sources(self) -> Tuple[int, Dict[str, List[Path]]]:
        file = Path('source')
        with open(file, 'w') as f:
            # write code to source file
            pass
        return 0, {'sources': [file]}

    def compile_sources(self, sources: List[Path]) -> Tuple[int, Dict[str, List[Path]]]:
        executable = Path('out.exe')
        compile(sources, executable)
        return 0, {'executable': [executable]}
```

## Defining dependencies and phases

Dogebuild must know how to insert your tasks into build graph.
To achieve that you must define all of your tasks dependencies and phases in `__init__` method.

```python
from typing import Tuple, Dict, List
from pathlib import Path
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def generate_sources(self) -> Tuple[int, Dict[str, List[Path]]]:
        file = Path('source')
        with open(file, 'w') as f:
            # write code to source file
            pass
        return 0, {'sources': [file]}

    def compile_sources(self, sources: List[Path]) -> Tuple[int, Dict[str, List[Path]]]:
        executable = Path('out.exe')
        compile(sources, executable)
        return 0, {'executable': [executable]}

    def __init__(self):
        super(MyPlugin, self).__init__()

        self.add_task(self.generate_sources, phase="generate-sources")
        self.add_task(self.compile_sources, phase="compile", depends=["generate_sources"])
```

Do not forget to call `super()` method to init common parameters of plugins.
