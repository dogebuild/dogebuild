import argparse
import sys
import os
from typing import List, Callable, Optional, Tuple, Dict
import logging
import logging.config
from pathlib import Path

from dogebuild.common import DOGE_FILE, sanitize_name, GlobalsContext
from dogebuild.dependencies import Dependency
from dogebuild.dependencies_functions import resolve_dependency_tree
from dogebuild.dogefile_loader import load_doge_file
from dogebuild.logging import _config_logging


def _main() -> None:
    _config_logging()

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
    abs_path = Path(doge_file).resolve().absolute()
    doge_directory = abs_path.parent
    doge_file_name = None

    context = load_doge_file(abs_path)

    relman = context.relman
    relman.verify()

    dependencies = context.dependencies
    test_dependencies = context.test_dependencies

    for dependency in dependencies + test_dependencies:
        logging.info('Resolving dependency {}'.format(dependency))
        dependency.acquire_dependency()
        code, artifacts = _run_task_of_file(os.path.join(dependency.get_doge_file_folder(), DOGE_FILE), 'build')
        if not code:
            dependency.artifacts = artifacts
        else:
            logging.error('Dependency {} build failed'.format(dependency))
            return code, {}

    run_list = relman.get_tasks(map(sanitize_name, tasks))
    logging.info('Run tasks: {}'.format(', '.join(map(lambda x: x[0], run_list))))

    os.chdir(doge_directory)
    artifacts = {}
    for current_task in run_list:
        try:
            with GlobalsContext(current_task[1].__globals__):
                res = current_task[1]()
                if res is None:
                    res = (0, {})
        except Exception as e:
            logging.exception(e)
            res = (1, {})

        exit_code, current_artifacts = res
        if not exit_code:
            logging.debug('Task {} successfully terminated'.format(current_task[0]))
            _add_artifacts(artifacts, current_artifacts)
        else:
            logging.error('Task {} failed'.format(current_task[0]))
            return exit_code, {}

    return 0, artifacts


def _add_artifacts(main: Dict, add: Dict):
    for type, artifacts in add.items():
        if type in main:
            main[type] += artifacts
        else:
            main[type] = artifacts


