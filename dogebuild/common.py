import glob
import os
from itertools import chain
from pathlib import Path
from typing import Dict, List, Union

DOGE_FILE = "dogefile.py"
DOGE_MODULES_DIRECTORY = ".doge_modules"


def files(base_dir: str, include: List[str], exclude: List[str] = None):
    if not exclude:
        exclude = []

    def expand_glob(base_dir, g):
        return glob.iglob(os.path.join(base_dir, g), recursive=True)

    return set(chain.from_iterable(map(lambda p: expand_glob(base_dir, p), include))) - set(
        chain.from_iterable(map(lambda p: expand_glob(base_dir, p), exclude))
    )


def sanitize_name(name: str):
    return name.replace("_", "-")


def merge_dicts(*dicts: Dict[str, List]):
    result = {}
    for d in dicts:
        for k, v in d.items():
            if k not in result:
                result[k] = []
            result[k].extend(v)
    return result


class DirectoryContext:
    def __init__(self, directory: Union[Path, str]):
        if isinstance(directory, str):
            directory = Path(directory)
        directory = directory.resolve()
        self.directory = directory
        self.saved = None

    def __enter__(self):
        self.saved = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved)
