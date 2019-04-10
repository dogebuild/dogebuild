from typing import Dict, List, Callable, Tuple

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
        self._relation_manager.add_dependency(task_name, [])

    def add_dependency(self, dependant: str, dependencies: List[str]):
        self._relation_manager.add_dependency(dependant, dependencies)

    def get_tasks(self, task_names: List[str]) -> List[Tuple[str, Callable]]:
        task_names = self._relation_manager.get_dependencies_recursive(task_names)
        return list(map(lambda name: (name, self._tasks[name]), task_names))

    def verify(self):
        known_task_names = set()
        for key in self._relation_manager._edges.keys():
            known_task_names.add(key)
            for dep in self._relation_manager._edges[key]:
                known_task_names.add(dep)

        for task_name in known_task_names:
            if task_name not in self._tasks.keys():
                raise Exception("Inconsistent task graph: unknown name '{}'".format(task_name))



TASK_RELATION_MANAGER = TaskRelationManager()


def task(name: str = None, depends: List[str] = None, phase: str = None):
    if not depends:
        depends = []

    def decorator(task_callable):
        task_name = name
        if not task_name:
            task_name = task_callable.__name__
        task_name = 'dogefile:' + _sanitize_name(task_name)

        TASK_RELATION_MANAGER.add_task(task_name, task_callable)
        TASK_RELATION_MANAGER.add_dependency(task_name, depends)

        if phase:
            TASK_RELATION_MANAGER.add_dependency(phase, [task_name])

        return task_callable

    return decorator


def _sanitize_name(name: str):
    return name.replace('_', '-')


def skip():
    pass


# Phases list

# Clean cycle

TASK_RELATION_MANAGER.add_task('clean', skip)

# Compile cycle

TASK_RELATION_MANAGER.add_task('compile', skip)

TASK_RELATION_MANAGER.add_task('test', skip)
TASK_RELATION_MANAGER.add_dependency('test', ['compile'])

TASK_RELATION_MANAGER.add_task('run', skip)
TASK_RELATION_MANAGER.add_dependency('run', ['test'])

# Documentation cycle

TASK_RELATION_MANAGER.add_task('docs', skip)
