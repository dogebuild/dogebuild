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

    def get_dependencies(self, key) -> List:
        return self._edges.get(key, [])

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
    DEFAULT_PHASES = {
        'clean': [],
        'docs': [],
        'docs-deploy': ['docs'],
        'sources': [],
        'resources': [],
        'test-sources': [],
        'test-resources': [],
        'test': ['sources', 'resources', 'test-sources', 'test-resources'],
        'build': ['test'],
        'run': ['build'],
        'integration-test': ['build'],
        'dist': ['integration-test'],
        'deploy': ['dist'],
        'install': ['dist'],
    }

    def __init__(self, phases: Dict[str, List[str]] = None):
        self._relation_manager = RelationManager()
        self._tasks = dict()

        if not phases:
            phases = TaskRelationManager.DEFAULT_PHASES

        for task, dependencies in phases.items():
            self.add_task(task, _skip)
            self.add_dependency(task, dependencies)

        self.verify()

    def add_task(self, task_name: str, task: Callable):
        self._tasks[task_name] = task
        self._relation_manager.add_dependency(task_name, [])

    def add_dependency(self, dependant: str, dependencies: List[str]):
        self._relation_manager.add_dependency(dependant, dependencies)

    def get_dependencies(self, dependant: str) -> List[str]:
        return self._relation_manager.get_dependencies(dependant)

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


def _skip():
    return 0, {}
