from dogebuild.plugins import ContextHolder
from dogebuild.common import DOGE_FILE


def load_doge_file(filename):
    with open(filename) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')

        ContextHolder.create()
        exec(code)
        return ContextHolder.clear_and_get()
