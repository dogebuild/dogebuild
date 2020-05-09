from typing import List, Dict
import os
import glob
from itertools import chain


DOGE_FILE = 'dogefile.py'


def files(base_dir: str, include: List[str], exclude: List[str] = None):
    if not exclude:
        exclude = []

    def expand_glob(base_dir, g):
        return glob.iglob(os.path.join(base_dir, g), recursive=True)

    return set(chain.from_iterable(map(lambda p: expand_glob(base_dir, p), include))) - set(chain.from_iterable(map(lambda p: expand_glob(base_dir, p), exclude)))


def sanitize_name(name: str):
    return name.replace('_', '-')


class GlobalsContext:
    def __init__(self, context: Dict):
        self.context = context
        self.saved = {}

    def __enter__(self):
        self.saved = globals()
        globals().clear()
        for k, v in self.context.items():
            globals()[k] = v

    def __exit__(self, exc_type, exc_val, exc_tb):
        globals().clear()
        for k, v in self.saved.items():
            globals()[k] = v
