import logging
from os import path
from typing import List, Optional

from dogebuild.dogefile_internals.dependencies import Dependency

from .common import DOGE_FILE


def resolve_dependency_tree(dependencies: List[Dependency], parents: List[str] = None) -> List[Dependency]:
    if not parents:
        parents = []

    for d in dependencies:
        id, version = d.get_id()
        if id in parents:
            raise Exception("Circular dependency")
        use_version = _resolve_version_(id, version)
        if version != use_version:
            d.original_version = d.version
            d.version = use_version
        logging.info("Acquiring {} ...".format(d))
        d.acquire_dependency()
        deps, _ = load_doge_file(path.join(d.get_doge_file_folder(), DOGE_FILE))  # noqa
        d.dependencies = resolve_dependency_tree(deps, parents + [id])
    return dependencies


VERSIONS = {}


def _resolve_version_(id: str, version: Optional[str]) -> Optional[str]:
    if not version:
        return None

    # simple conflict resolving strategy
    saved_version = VERSIONS.get(id)
    if not saved_version:
        VERSIONS[id] = version
        return version
    else:
        return saved_version
