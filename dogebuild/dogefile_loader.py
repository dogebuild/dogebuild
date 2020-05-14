from typing import Dict
import os
from pathlib import Path

from dogebuild.dogefile_internals.context import ContextHolder, Context, ContextHolderGuard
from dogebuild.common import DOGE_FILE


def load_doge_file(dogefile: Path) -> Context:
    with open(dogefile, 'r') as file, ContextHolderGuard(dogefile) as holder:
        code = compile(file.read(), dogefile.name, 'exec')
        exec(code, holder.globals_context)
        return holder.context
