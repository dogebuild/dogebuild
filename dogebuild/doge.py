import argparse
import sys
import os
from typing import List, Callable, Optional, Tuple, Dict

from dogebuild.common import DOGE_FILE
from dogebuild.dependencies import Dependency
from dogebuild.dependencies_functions import resolve_dependency_tree
from dogebuild.dogefile_loader import load_doge_file


def _main() -> None:
    main_parser = argparse.ArgumentParser(description='')
    main_parser.add_argument('command', nargs=1)
    main_parser.add_argument('options', nargs=argparse.REMAINDER)

    main_args = main_parser.parse_args()

    func = _get_function(main_args.command[0])

    if callable(func):
        exit(func(*main_args.options))
    else:
        tasks = main_args.command + main_args.options
        tasks = map(lambda name: name.lstrip(':'), tasks)
        exit(_run_tasks(*tasks))


def _get_function(name: str) -> Optional[Callable]:
    name = name.lower().strip().replace('-', '_')
    if not name[0].isalpha():
        return None
    else:
        return getattr(_get_current_module(), name, None)


def _get_current_module():
    module_name = globals()['__name__']
    return sys.modules[module_name]


def dependency_tree() -> int:
    deps, _ = load_doge_file(DOGE_FILE)
    deps = resolve_dependency_tree(deps)
    _print_dependencies(deps)
    return 0


def _print_dependencies(dependencies: List[Dependency], inner_level: int=0):
    for d in dependencies:
        if d.original_version:
            print(' ' * (2 * inner_level - 1) + '+' + str(d) + ' conflict resolved for {}'.format(d.original_version))
        else:
            print(' ' * (2 * inner_level - 1) + '+' + str(d))
        _print_dependencies(d.dependencies, inner_level=inner_level + 1)


def _run_tasks(*tasks) -> int:
    return _run_task_of_file(DOGE_FILE, *tasks)[0]


def _run_task_of_file(doge_file, *tasks) -> Tuple[int, Dict]:
    abs_path = os.path.abspath(doge_file)
    doge_directory = os.path.dirname(abs_path)
    doge_file_name = os.path.basename(abs_path)

    context = load_doge_file(abs_path)

    relman = context.relman
    relman.verify()

    dependencies = context.dependencies
    test_dependencies = context.test_dependencies

    for dependency in dependencies + test_dependencies:
        print('Resolving dependency {}'.format(dependency))
        dependency.acquire_dependency()
        code, artifacts = _run_task_of_file(os.path.join(dependency.get_doge_file_folder(), DOGE_FILE), 'build')
        if not code:
            dependency.artifacts = artifacts
        else:
            print('Dependency {} build failed'.format(dependency))
            return code, {}

    run_list = relman.get_tasks(tasks)
    print('Run tasks: {}'.format(', '.join(map(lambda x: x[0], run_list))))

    os.chdir(doge_directory)
    artifacts = {}
    for t in run_list:
        exit_code, current_artifacts = t[1]()
        if not exit_code:
            print('Task {} successfully terminated'.format(t[0]))
            _add_artifacts(artifacts, current_artifacts)
        else:
            print('Task {} failed'.format(t[0]))
            return exit_code, {}

    return 0, artifacts


def _add_artifacts(main: Dict, add: Dict):
    for type, artifacts in add.items():
        if type in main:
            main[type] += artifacts
        else:
            main[type] = artifacts
