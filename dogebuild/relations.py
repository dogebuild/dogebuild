from typing import Dict, List

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

    def get_dependencies_recursive(self, tasks: List) -> List:
        result = OrderedDict()

        def recursive_append(target: Dict, source: Dict, key):
            if key in source:
                target[key] = source[key]
                for x in target[key]:
                    if x not in target.keys():
                        recursive_append(target, source, x)

        for task in tasks:
            dependencies = {}
            recursive_append(dependencies, self._edges, task)
            task_required = toposort_flatten(dependencies)
            for x in task_required:
                result[x] = self._DUMMY

        return list(result.keys())
