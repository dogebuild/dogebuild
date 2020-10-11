from collections import OrderedDict
from dataclasses import dataclass
from inspect import signature
from typing import Callable, Dict, List, Optional, Iterable, Any

from toposort import toposort_flatten

from dogebuild.common import sanitize_name


class RelationManager:
    _DUMMY = 1

    def __init__(self):
        self._edges = {}

    def add_dependency(self, dependant, dependencies: Iterable):
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


@dataclass()
class TaskResult:
    exit_code: int
    artifacts: Dict
    error: Exception


class Task:
    TASK_TYPE = "Task"

    def __init__(self, canonical_name: str):
        self.canonical_name = canonical_name

    def run(self, artifacts: Dict, parameters: Dict[str, Any], code_context: Dict) -> TaskResult:
        raise NotImplementedError()


class FunctionTask(Task):
    def __init__(self, canonical_name: str, function: Callable):
        super(FunctionTask, self).__init__(canonical_name)
        self.function = function

    def run(self, artifacts: Dict, parameters: Dict[str, Any], code_context: Dict):
        try:
            sig = signature(self.function)
            locals_values = {}
            for arg in sig.parameters:
                if arg.startswith("parameter_"):
                    param_name = arg[len("parameter_") :]
                    if param_name in parameters:
                        locals_values[arg] = parameters[param_name]
                    else:
                        raise Exception(f"Parameter {param_name} not described in dogefile")
                elif arg.startswith("artifact_"):
                    artifact_name = arg[len("artifact_") :]
                    if artifact_name in artifacts:
                        locals_values[arg] = artifacts[artifact_name]
                    else:
                        raise Exception(f"Artifact {artifact_name} not found")
                else:
                    locals_values[arg] = parameters.get(arg, artifacts.get(arg, []))
            callable_name = self.function.__name__
            exec(f'RESULT = {callable_name}({", ".join(locals_values.keys())})', code_context, locals_values)
            res = locals_values.get("RESULT")
            if res is None:
                res = (0, {})
            return TaskResult(res[0], res[1], None)
        except Exception as e:
            return TaskResult(1, {}, e)


class PhaseTask(Task):
    TASK_TYPE = "Phase"

    def run(self, artifacts: Dict, parameters: Dict[str, Any], code_context: Dict) -> TaskResult:
        return TaskResult(0, {}, None)


class PluginTask(Task):
    def __init__(self, canonical_name: str, method: Callable, plugin_instance):
        super(PluginTask, self).__init__(canonical_name)
        self.method = method
        self.plugin_instance = plugin_instance

    def run(self, artifacts: Dict, parameters: Dict[str, Any], code_context: Dict):
        try:
            sig = signature(self.method)
            locals_values = {"PLUGIN_INSTANCE": self.plugin_instance}
            arguments = {}
            for arg in sig.parameters:
                locals_values[arg] = artifacts.get(arg, [])
                arguments[arg] = artifacts.get(arg, [])
            method_name = self.method.__name__
            exec(f'RESULT = PLUGIN_INSTANCE.{method_name}({", ".join(arguments.keys())})', code_context, locals_values)
            res = locals_values.get("RESULT")
            if res is None:
                res = (0, {})
            return TaskResult(res[0], res[1], None)
        except Exception as e:
            return TaskResult(1, {}, e)


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

    def __init__(self, doge_file_id: str, phases=None):
        if phases is None:
            phases = TaskRelationManager.DEFAULT_PHASES

        self._doge_file_id = doge_file_id
        self._relation_manager = RelationManager()
        self._phases = phases
        self._tasks = dict()
        self._tasks_aliases = dict()

        for phase_name, dependencies in self._phases.items():
            self._tasks[phase_name] = PhaseTask(phase_name)
            self._tasks_aliases[phase_name] = phase_name
            self.add_dependency(phase_name, dependencies)

        self.verify()

    def add_task(
        self,
        task: Callable,
        *,
        aliases: str = None,
        plugin_name: str = None,
        dependencies: List[str] = None,
        phase: str = None,
        plugin_instance=None,
    ):
        if aliases is None:
            aliases = []
        if dependencies is None:
            dependencies = []

        task_aliases = self._build_task_aliases(task.__name__, aliases, plugin_name)
        canonical_task_name = task_aliases[0]

        if plugin_instance is None:
            self._tasks[canonical_task_name] = FunctionTask(canonical_task_name, task)
        else:
            self._tasks[canonical_task_name] = PluginTask(canonical_task_name, task, plugin_instance)
        for alias in task_aliases:
            if alias in self._phases:
                # Tasks with phase name are not allowed
                continue
            if alias not in self._tasks_aliases:
                self._tasks_aliases[alias] = canonical_task_name
            else:
                if isinstance(self._tasks_aliases[alias], DuplicateAlias):
                    self._tasks_aliases[alias].duplicates.add(alias)
                else:
                    self._tasks_aliases[alias] = DuplicateAlias([self._tasks_aliases[alias], alias])

        self._relation_manager.add_dependency(canonical_task_name, map(sanitize_name, dependencies))
        if phase:
            self._relation_manager.add_dependency(phase, [canonical_task_name])
            self._relation_manager.add_dependency(canonical_task_name, self._phases.get(phase))

    def add_dependency(self, canonical_task_name: str, dependencies: List[str]):
        self._relation_manager.add_dependency(canonical_task_name, dependencies)

    def get_dependencies(self, canonical_task_name: str) -> List[str]:
        return self._relation_manager.get_dependencies(canonical_task_name)

    def get_tasks(self, task_names: List[str]) -> List[Task]:
        canonical_task_names = []
        unknown_tasks = []

        for name in task_names:
            if name in self._tasks_aliases:
                canonical_task_names.append(self._tasks_aliases[name])
            else:
                unknown_tasks.append(name)

        if unknown_tasks:
            raise Exception(f"Unknown tasks: {unknown_tasks}")

        sorted_dependencies = self._relation_manager.get_dependencies_recursive(canonical_task_names)
        return list(map(lambda canonical_name: self._tasks[canonical_name], sorted_dependencies))

    def verify(self):
        known_task_names = set()
        for key in self._relation_manager._edges.keys():
            known_task_names.add(key)
            self._relation_manager._edges[key] = set(
                map(lambda x: self._tasks_aliases[x], self._relation_manager._edges[key])
            )

            for dep in self._relation_manager._edges[key]:
                known_task_names.add(dep)

        for task_name in known_task_names:
            if task_name not in self._tasks.keys():
                raise Exception("Inconsistent task graph: unknown name '{}'".format(task_name))

    def _build_task_aliases(self, callable_name: str, aliases: List[str], plugin_name: Optional[str]) -> List[str]:
        short_names = [callable_name] + aliases
        result = []
        for short_name in short_names:
            if plugin_name is None:
                result.extend(
                    [
                        sanitize_name(f"{self._doge_file_id}:{short_name}"),
                        sanitize_name(short_name),
                    ]
                )
            else:
                result.extend(
                    [
                        sanitize_name(f"{self._doge_file_id}:{plugin_name}:{short_name}"),
                        sanitize_name(f"{plugin_name}:{short_name}"),
                        sanitize_name(short_name),
                    ]
                )
        return result


class DuplicateAlias:
    def __init__(self, duplicates):
        self.duplicates = duplicates
