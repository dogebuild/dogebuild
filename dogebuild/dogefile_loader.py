from typing import List, Tuple

from .dependencies import Dependency
from .plugins import DogePlugin
from .common import DOGE_FILE

DEPENDENCIES_VAR = 'DEPENDENCIES'
PLUGINS_VAR = 'PLUGINS'


def load_doge_file(filename) -> Tuple[List[Dependency], List[DogePlugin]]:
    with open(filename) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')
        scope = {}
        exec(code, scope)

        return scope.get(DEPENDENCIES_VAR, []), scope.get(PLUGINS_VAR, [])
