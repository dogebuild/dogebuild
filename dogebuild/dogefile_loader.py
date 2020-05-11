import os
from pathlib import Path

from dogebuild.context import ContextHolder, Context
from dogebuild.common import DOGE_FILE


def load_doge_file(dogefile: Path) -> Context:
    file_dir = dogefile.parent
    with open(dogefile) as f:
        code = compile(f.read(), DOGE_FILE, 'exec')

        ContextHolder.create()
        cwd = os.getcwd()
        os.chdir(file_dir)
        glbs = {}
        exec(code, glbs)
        os.chdir(cwd)
        ContextHolder.CONTEXT.code_context = glbs
        return ContextHolder.clear_and_get()
