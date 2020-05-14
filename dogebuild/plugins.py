from logging import getLogger
from typing import Callable, List

from dogebuild.dogefile_internals.context import ContextHolder


class DogePlugin:
    NAME = 'This is abstract doge plugin so this variable should never be used'

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, **kwargs):
        self.logger = getLogger(self.get_name())

        ContextHolder.INSTANCE.context.plugins.append(self)

        self.relman = ContextHolder.INSTANCE.context.relman
        self.dependencies = ContextHolder.INSTANCE.context.dependencies
        self.test_dependencies = ContextHolder.INSTANCE.context.test_dependencies

    def add_task(self, task_name: str, task: Callable, phase: str = None):
        task_name = self._resolve_full_task_name(task_name)

        self.relman.add_task(task_name, task)
        if phase:
            self.relman.add_dependency(phase, [task_name])
            self.relman.add_dependency(task_name, self.relman.get_dependencies(phase))

    def add_dependency(self, task_name: str, dependencies: List[str]):
        task_name = self._resolve_full_task_name(task_name)
        dependencies = list(map(lambda n: self._resolve_full_task_name(n), dependencies))

        self.relman.add_dependency(task_name, dependencies)

    def _resolve_full_task_name(self, task_name: str):
        return self.__class__.get_name() + ":" + task_name
