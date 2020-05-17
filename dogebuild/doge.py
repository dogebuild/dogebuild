import logging
import logging.config
from dataclasses import dataclass
from inspect import signature
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from dogebuild.common import DOGE_FILE, DirectoryContext, sanitize_name
from dogebuild.dependencies_functions import resolve_dependency_tree
from dogebuild.dogefile_internals.context import Context, ContextHolderGuard
from dogebuild.dogefile_internals.dependencies import Dependency


@dataclass()
class TaskResult:
    exit_code: int
    artifacts: Dict
    error: Exception


class DogeFile:
    def __init__(self, doge_file: Path):
        self.doge_file = doge_file.resolve()
        self.directory = self.doge_file.parent

        context = DogeFile._load_doge_file(self.doge_file)

        self.dependencies = context.dependencies
        self.test_dependencies = context.test_dependencies
        self.relman = context.relman
        self.artifacts = {}
        self.code_context = context.code_context
        self.modules = context.modules

        self.processed_tasks = {}

    def run_tasks(self, tasks: List[str]):
        for submodule in self.modules:
            submodule_doge_file = DogeFile(self.directory / submodule / DOGE_FILE)
            submodule_doge_file.run_tasks(tasks)

        with DirectoryContext(self.directory):
            self._resolve_dependencies()

            run_list = self.relman.get_tasks(map(sanitize_name, tasks))
            logging.info("Run tasks: {}".format(", ".join(map(lambda x: x[0], run_list))))

            for current_task in run_list:
                self._run_task(current_task)

    def _resolve_dependencies(self):
        for dependency in self.dependencies + self.test_dependencies:
            logging.info(f"Resolving dependency {dependency}")
            dependency.acquire_dependency()

            dependency_doge_file = DogeFile(Path(dependency.get_doge_file_folder()) / DOGE_FILE)
            dependency_doge_file.run_tasks(["build"])

            absolute_artifacts = {}
            dff = Path(dependency.get_doge_file_folder()).resolve()
            for k, v in dependency_doge_file.artifacts.items():
                absolute_artifacts[k] = list(map(lambda d: dff / d, v))

            self._add_artifacts(absolute_artifacts)

    def _run_task(self, task: Tuple[str, Callable]) -> TaskResult:
        task_name = task[0]
        task_callable = task[1]
        sig = signature(task_callable)

        if task_name in self.processed_tasks:
            return self.processed_tasks[task_name]

        try:
            locals_values = {}
            for arg in sig.parameters:
                locals_values[arg] = self.artifacts.get(arg, [])
            callable_name = task[1].__name__
            exec(
                f'RESULT = {callable_name}({", ".join(locals_values.keys())})', self.code_context, locals_values,
            )

            res = locals_values.get("RESULT")
            if res is None:
                res = (0, {})
            res = (*res, None)
        except Exception as e:
            logging.exception(e)
            res = (1, {}, e)

        exit_code, artifacts, error = res
        if not exit_code:
            self._add_artifacts(artifacts)
            logging.debug(f"Task {task_name} successfully terminated")
        else:
            logging.error(f"Task {task_name} failed")

        task_result = TaskResult(exit_code, artifacts, error)
        self.processed_tasks[task_name] = task_result
        return task_result

    def _add_artifacts(self, add: Dict[str, List]) -> None:
        for type, artifacts in add.items():
            if type in self.artifacts:
                self.artifacts[type] += artifacts
            else:
                self.artifacts[type] = artifacts

    @staticmethod
    def _load_doge_file(doge_file: Path) -> Context:
        with open(doge_file, "r") as file, ContextHolderGuard(doge_file) as holder:
            code = compile(file.read(), doge_file.name, "exec")
            exec(code, holder.globals_context)
            holder.context.verify()
            return holder.context

    def dependency_tree(self) -> int:
        deps, _ = load_doge_file(DOGE_FILE)  # noqa
        deps = resolve_dependency_tree(deps)
        self._print_dependencies(deps)
        return 0

    def _print_dependencies(self, dependencies: List[Dependency], inner_level: int = 0):
        for d in dependencies:
            if d.original_version:
                print(
                    " " * (2 * inner_level - 1) + "+" + str(d) + " conflict resolved for {}".format(d.original_version)
                )
            else:
                print(" " * (2 * inner_level - 1) + "+" + str(d))
            self._print_dependencies(d.dependencies, inner_level=inner_level + 1)
