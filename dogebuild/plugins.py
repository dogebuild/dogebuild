from logging import getLogger
from typing import Callable, List

from dogebuild.dogefile_internals.context import ContextHolder


class DogePlugin:
    NAME = "This is abstract doge plugin so this variable should never be used"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, **kwargs):
        self.logger = getLogger(self.get_name())

        ContextHolder.INSTANCE.context.plugins.append(self)

        self.relman = ContextHolder.INSTANCE.context.relman
        self.dependencies = ContextHolder.INSTANCE.context.dependencies
        self.test_dependencies = ContextHolder.INSTANCE.context.test_dependencies

    def add_task(self, task_callable: Callable = None, *, aliases: List[str] = None, depends: List[str] = None, phase: str = None,):
        self.relman.add_task(task_callable, aliases=aliases, dependencies=depends, plugin_name=self.NAME, phase=phase)

    def add_dependency(self, task_name: str, dependencies: List[str]):
        task_name = self._resolve_full_task_name(task_name)
        dependencies = list(map(lambda n: self._resolve_full_task_name(n), dependencies))

        self.relman.add_dependency(task_name, dependencies)

    def _resolve_full_task_name(self, task_name: str):
        return self.__class__.get_name() + ":" + task_name


class StubPlugin(DogePlugin):
    """
    Stub plugin for integration test
    """
    NAME = "Stub plugin"

    def __init__(self, **kwargs):
        super(StubPlugin, self).__init__(**kwargs)

    def task_1(self):
        pass

    def task_2(self):
        pass

    def task_3(self):
        pass

    def task_4(self):
        pass


