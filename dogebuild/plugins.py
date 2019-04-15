from typing import Callable, List

from dogebuild.context import ContextHolder


class DogePlugin:
    NAME = 'This is abstract doge plugin so this variable should never be used'

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, **kwargs):
        ContextHolder.CONTEXT.plugins.append(self)

        self.relman = ContextHolder.CONTEXT.relman
        self.dependencies = ContextHolder.CONTEXT.dependencies
        self.test_dependencies = ContextHolder.CONTEXT.test_dependencies

    def add_task(self, task_name: str, task: Callable, phase: str = None):
        task_name = self._resolve_full_task_name(task_name)

        self.relman.add_task(task_name, task)
        if phase:
            self.relman.add_dependency(phase, [task_name])

    def add_dependency(self, task_name: str, dependencies: List[str]):
        task_name = self._resolve_full_task_name(task_name)
        dependencies = list(map(lambda n: self._resolve_full_task_name(n), dependencies))

        self.relman.add_dependency(task_name, dependencies)

    def _resolve_full_task_name(self, task_name: str):
        return self.__class__.get_name() + ":" + task_name
