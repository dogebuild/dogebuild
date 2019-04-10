from typing import Dict, Callable, List
from collections import OrderedDict
from toposort import toposort_flatten

from dogebuild.relations import TASK_RELATION_MANAGER


class DogePlugin:
    NAME = 'This is abstract doge plugin so this variable should never be used'
    _TASK_RELATION_MANAGER = TASK_RELATION_MANAGER

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, **kwargs):
        pass

    def add_task(self, task_name: str, task: Callable, phase: str = None):
        task_name = self._resolve_full_task_name(task_name)

        DogePlugin._TASK_RELATION_MANAGER.add_task(task_name, task)
        if phase:
            DogePlugin._TASK_RELATION_MANAGER.add_dependency(phase, [task_name])

    def add_dependency(self, task_name: str, dependencies: List[str]):
        task_name = self._resolve_full_task_name(task_name)
        dependencies = list(map(lambda n: self._resolve_full_task_name(n), dependencies))

        DogePlugin._TASK_RELATION_MANAGER.add_dependency(task_name, dependencies)

    def _resolve_full_task_name(self, task_name: str):
        return self.__class__.get_name() + ":" + task_name
