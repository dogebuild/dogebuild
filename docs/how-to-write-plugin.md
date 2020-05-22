# Writing plugin

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


## Defining dependencies and phases

Dogebuild must know how to insert your tasks into build graph.
To achieve that you must define your task dependencies and phases in `__init__` method.


```python
from typing import Tuple, Dict
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def build_my_sources(self) -> Tuple[int, Dict]:
        # build sources
        exit_code = 0
        return exit_code, {'artifact-name': ['artifact-1-value', 'artifact-2-value']}

    def build_my_resources(self) -> Tuple[int, Dict]:
        # build resources
        return 0, {'artifacts': []}

    def prepare_resources(self) -> Tuple[int, Dict]:
        # prepare resources
        return 0, {}

    def __init__(self):
        super(MyPlugin, self).__init__()

        self.add_task('build_my_sources', self.build_my_sources, phase='sources')
        self.add_task('prepare_resources', self.prepare_resources)
        self.add_task('build_my_resources', self.build_my_resources, phase='resources', dependencies=['prepare_resources'])
```

Do not forget to call `super()` method to init common parameters of plugins.
