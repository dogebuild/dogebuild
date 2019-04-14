import argparse
import sys
from typing import List

from dogebuild.common import DOGE_FILE
from dogebuild.dependencies import Dependency
from dogebuild.dependencies_functions import resolve_dependency_tree
from dogebuild.dogefile_loader import load_doge_file

from dogebuild.relations import TASK_RELATION_MANAGER


def run() -> None:
    main_parser = argparse.ArgumentParser(description='')
    main_parser.add_argument('command', nargs=1)
    main_parser.add_argument('options', nargs=argparse.REMAINDER)

    main_args = main_parser.parse_args()

    func_name = _get_function_name(main_args.command[0])
    func = getattr(_get_current_module(), func_name, None)
    if not callable(func):
        print('Unknown command {}'.format(main_args.command))
        print(main_parser.format_help())
        exit(1)
    exit(func(*main_args.options))


def _get_function_name(name: str) -> str:
    return name.replace('-', '_')


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


def run_plugin(*task) -> int:
    deps, plugins = load_doge_file(DOGE_FILE)
    z = TASK_RELATION_MANAGER

    z.verify()
    tsks = z.get_tasks(task)

    for t in tsks:
        exit_code = t[1]()
        if not exit_code:
            print('Task {} successfully terminated'.format(t[0]))
        else:
            print('Task {} failed'.format(t[0]))
            return exit_code

    return 0


