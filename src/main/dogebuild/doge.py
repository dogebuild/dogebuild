import argparse
import sys
from os import path

from typing import List, Union, Tuple

from .dependencies import Dependency


DOGE_FILE = 'dogefile.py'

DEPENDENCIES_VAR = 'DEPENDENCIES'


def run():
    main_parser = argparse.ArgumentParser(description='')
    main_parser.add_argument('command', nargs=1)
    main_parser.add_argument('options', nargs=argparse.REMAINDER)

    main_args = main_parser.parse_args()

    func_name = get_function_name(main_args.command[0])
    func = getattr(get_current_module(), func_name, None)
    if not callable(func):
        print('Unknown command {}'.format(main_args.command))
        print(main_parser.format_help())
        exit(1)
    exit(func(*main_args.options))


def get_function_name(name: str) -> str:
    return name.replace('-', '_')


def get_current_module():
    module_name = globals()['__name__']
    return sys.modules[module_name]


def dependency_tree() -> int:
    deps = _get_dependencies(DOGE_FILE)
    _print_dependencies(deps)
    return 0


def _get_dependencies(file: str) -> List[Dependency]:
    dependencies = load_doge_file(file)
    for d in dependencies:
        id, version = d.get_id()
        use_version = _resolve_version_(id, version)
        if version != use_version:
            d.original_version = d.version
            d.version = use_version
        print('Acquiring {} ...'.format(d))
        d.acquire_dependency()
        d.dependencies = _get_dependencies(path.join(d.get_doge_file_folder(), DOGE_FILE))
    return dependencies


def _print_dependencies(dependencies: List[Dependency], inner_level: int=0):
    for d in dependencies:
        if d.original_version:
            print(' ' * (2 * inner_level - 1) + '+' + str(d) + ' conflict resolved for {}'.format(d.original_version))
        else:
            print(' ' * (2 * inner_level - 1) + '+' + str(d))
        _print_dependencies(d.dependencies, inner_level=inner_level + 1)


VERSIONS = {}


def _resolve_version_(id: str, version: Union[str, None]) -> Union[str, None]:
    if not version:
        return None

    # simple conflict resolving strategy
    saved_version = VERSIONS.get(id)
    if not saved_version:
        VERSIONS[id] = version
        return version
    else:
        return saved_version


def load_doge_file(filename) -> List[Dependency]:
    with open(filename) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')
        scope = {}
        exec(code, scope)

        dependencies = scope.get(DEPENDENCIES_VAR)
        if not dependencies:
            dependencies = []
        return dependencies
