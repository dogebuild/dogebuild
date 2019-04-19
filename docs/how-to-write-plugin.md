# Writing plugin

## Creating class

First of all, create class that inherits `DogePlugin` class:

```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    pass

```

## Defining name of plugin

To distinguish tasks with the same name from different plugins each plugin must have uniqe name.
To define plugin name simply define `NAME` constant in plugin. 

```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

```

## Defining tasks

Create methods, that will be represents the tasks of your plugin:

```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def build_my_sources(self):
        # build sources
        return code, {'artifact-name': ['artifact-1-value', 'artifact-2-value']}

```

Methods must return tuple with return code and artifacts dictionary.
Keys are artifacts names and values are lists of artifacts values, usually values are path to files or directories.

## Defining dependencies and phases

Dogeubuild must know how to insert your tasks into lifecycle.
To achieve that you must define your task dependencies and phases in `__init__` method.


```python
from dogebuild.plugins import DogePlugin


class MyPlugin(DogePlugin):
    NAME = 'my-plugin-name'

    def build_my_sources(self):
        # build sources
        return code, {'artifact-name': ['artifact-1-value', 'artifact-2-value']}

    def build_my_resources(self):
        # build resources
        return code, {'artifacts': []}

    def prepare_resources(self):
        # prepare resources
        return 0, {}

    def __init__(self):
        super(MyPlugin, self).__init__()

        self.add_task('build_my_sources', self.build_my_sources, phase='sources')

        self.add_task('prepare_resources', self.prepare_resources)

        self.add_task('build_my_resources', self.build_my_resources, phase='resources')
        self.add_dependency('build_my_resources', ['prepare_resources'])

```

And do not forget to call `super()` method to init common parameters of plugins.


