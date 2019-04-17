from typing import List
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
