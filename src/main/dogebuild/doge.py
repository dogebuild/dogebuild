import argparse
import sys
from os import path


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
    _recursive_file_process(DOGE_FILE)
    return 0


def _recursive_file_process(file):
    dependencies = load_doge_file(file)
    for d in dependencies:
        print(d)
        d.acquire_dependency()
        _recursive_file_process(path.join(d.get_doge_file_folder(), DOGE_FILE))


def load_doge_file(filename=DOGE_FILE):
    with open(filename) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')
        scope = {}
        exec(code, scope)

        dependencies = scope.get(DEPENDENCIES_VAR)
        if not dependencies:
            dependencies = []
        return dependencies
