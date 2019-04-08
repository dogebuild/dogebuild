from typing import Dict, Callable, List
from collections import OrderedDict
from toposort import toposort_flatten


class DagContext:
    DUMMY = 1

    def __init__(self):
        self.tasks = {}
        self.edges = {}

    def task(self, name: str = None, depends: List[str] = None):
        if not depends:
            depends = []

        def decorator(func):
            task_name = name
            if not task_name:
                task_name = func.__name__
            task_name = self._sanitize_name(task_name)
            self.tasks[task_name] = func
            self.edges[task_name] = set(depends)
            return func

        return decorator

    def get_tasks(self, tasks: List[str]) -> List[Callable]:
        dc = OrderedDict()

        def recursive_append(target: Dict, source: dict, key):
            target[key] = source[key]
            for x in target[key]:
                if not x in target.keys():
                    recursive_append(target, source, x)

        for task in tasks:
            active_tasks = {}
            recursive_append(active_tasks, self.edges, task)
            task_required = toposort_flatten(active_tasks)
            for x in task_required:
                dc[x] = self.DUMMY

        return list(map(lambda x: self.tasks[x], dc.keys()))

    @staticmethod
    def _sanitize_name(name: str):
        return name.replace('_', '-')


class DogePlugin:
    NAME = 'This is abstract doge plugin so this variable should never be used'

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, dag_context: DagContext):
        self.dag_context = dag_context

    def get_tasks(self, tasks: List[str]):
        return self.dag_context.get_tasks(tasks)
