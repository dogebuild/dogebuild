from collections import OrderedDict
from typing import Callable, Dict, List, Tuple

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
        "clean": [],
        "docs": [],
        "docs-deploy": ["docs"],
        "sources": [],
        "resources": [],
        "test-sources": [],
        "test-resources": [],
        "test": ["sources", "resources", "test-sources", "test-resources"],
        "build": ["test"],
        "run": ["build"],
        "integration-test": ["build"],
        "dist": ["integration-test"],
        "deploy": ["dist"],
        "install": ["dist"],
    }

    def __init__(self, phases: Dict[str, List[str]] = None):
        self._relation_manager = RelationManager()
        self._tasks = dict()
        self._tasks_short_names = dict()

        if phases is None:
            phases = TaskRelationManager.DEFAULT_PHASES
        self._phases = phases

        for task, dependencies in self._phases.items():
            self.add_task(task, _skip)
            self.add_dependency(task, dependencies)

        self.verify()

    def add_task(self, task_name: str, task: Callable):
        self._tasks[task_name] = task
        self._relation_manager.add_dependency(task_name, [])

        short_name = TaskRelationManager._get_task_short_name(task_name)
        if short_name in self._phases.keys():
            return
        if short_name in self._tasks_short_names:
            self._tasks_short_names[short_name].append(task_name)
        else:
            self._tasks_short_names[short_name] = [task_name]

    def add_dependency(self, dependant: str, dependencies: List[str]):
        self._relation_manager.add_dependency(dependant, dependencies)

    def get_dependencies(self, dependant: str) -> List[str]:
        return self._relation_manager.get_dependencies(dependant)

    def get_tasks(self, task_names: List[str]) -> List[Tuple[str, Callable]]:
        full_names = []
        for name in task_names:
            if name in self._tasks_short_names:
                full_name = self._tasks_short_names[name]
                if len(full_name) == 1:
                    full_names.append(full_name[0])
                else:
                    raise Exception("Multiple tasks with short name " + name)
            else:
                full_names.append(name)

        task_names = self._relation_manager.get_dependencies_recursive(full_names)
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

    @staticmethod
    def _get_task_short_name(task_name: str) -> str:
        split = task_name.split(":", maxsplit=2)
        if len(split) == 2:
            return split[1]
        else:
            return task_name

    @staticmethod
    def is_task_short_name(task_name: str) -> bool:
        split = task_name.split(":", maxsplit=2)
        return len(split) == 1


def _skip():
    return 0, {}
