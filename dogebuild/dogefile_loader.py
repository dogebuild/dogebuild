import os
from pathlib import Path

from dogebuild.plugins import ContextHolder
from dogebuild.common import DOGE_FILE


def load_doge_file(filename):
    dir = Path(filename).resolve().parent
    with open(filename) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')

        ContextHolder.create()
        cwd = os.getcwd()
        os.chdir(dir)
        exec(code)
        os.chdir(cwd)
        return ContextHolder.clear_and_get()
