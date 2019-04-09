from typing import Dict, List, Callable

from collections import OrderedDict
from toposort import toposort_flatten


class RelationManager:
    _DUMMY = 1

    def __init__(self):
        self._edges = {}

    def add_dependency(self, dependant, dependencies: List):
        if dependant not in self._edges:
            self._edges[dependant] = set()

        for dependency in dependencies:
            self._edges[dependant].add(dependency)

    def get_dependencies_recursive(self, keys: List) -> List:
        result = OrderedDict()

        def recursive_append(target: Dict, source: Dict, key):
            if key in source:
                target[key] = source[key]
                for x in target[key]:
                    if x not in target.keys():
                        recursive_append(target, source, x)

        for key in keys:
            dependencies = {}
            recursive_append(dependencies, self._edges, key)
            task_required = toposort_flatten(dependencies)
            for x in task_required:
                result[x] = self._DUMMY

        return list(result.keys())


class TaskRelationManager:
    def __init__(self):
        self._relation_manager = RelationManager()
        self._tasks = dict()

    def add_task(self, task_name: str, task: Callable):
        self._tasks[task_name] = task

    def add_dependency(self, dependant: str, dependencies: List[str]):
        self._relation_manager.add_dependency(dependant, dependencies)

    def get_tasks(self, task_names: List[str]) -> List[Callable]:
        task_names = self._relation_manager.get_dependencies_recursive(task_names)
        return list(map(lambda name: self._tasks[name], task_names))


TASK_RELATION_MANAGER = TaskRelationManager()


def task(name: str = None, depends: List[str] = None, phase: str = None):
    if not depends:
        depends = []

    def decorator(task_callable):
        task_name = name
        if not task_name:
            task_name = task_callable.__name__
        task_name = _sanitize_name(task_name)

        TASK_RELATION_MANAGER.add_task(task_name, task_callable)
        TASK_RELATION_MANAGER.add_dependency(task_name, depends)

        if phase:
            TASK_RELATION_MANAGER.add_dependency(phase, [task_name])

        return task_callable

    return decorator


def _sanitize_name(name: str):
    return name.replace('_', '-')


# Here are phases
@task('compile')
def phase_compile():
    pass


@task('test', depends=['compile'])
def phase_test():
    pass


@task('run', depends=['test'])
def phase_run():
    pass
