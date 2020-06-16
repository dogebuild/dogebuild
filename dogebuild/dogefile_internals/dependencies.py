from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from gitsnapshot import load_repo

from dogebuild.common import DOGE_FILE, DOGE_MODULES_DIRECTORY
from dogebuild.dogefile_internals.context import ContextHolder


class Dependency:
    def get_id(self) -> Tuple[str, Optional[str]]:
        raise NotImplementedError()

    def __str__(self):
        id, version = self.get_id()
        if version is None:
            return id
        else:
            return f"{id} ({version})"

    def acquire_dependency(self):
        pass

    def get_artifacts(self) -> Dict[str, List[Path]]:
        return {}

    def get_dependency_directory(self) -> Path:
        return Path(DOGE_MODULES_DIRECTORY) / self._get_dependency_directory_relative()

    def _get_dependency_directory_relative(self) -> Path:
        raise NotImplementedError()


class GitDependency(Dependency):
    GIT_REPO_FOLDER = Path(DOGE_MODULES_DIRECTORY) / "git"

    VERSION_TAG = "tag:"
    VERSION_BRANCH = "branch:"
    # TODO: make VERSION_COMMIT

    def __init__(self, url, version):
        self.url = url
        self.version = version
        self.name = url.split("/")[-1].replace(".git", "")
        self.org = url.split("/")[-2].split(":")[-1]

    def get_id(self) -> Tuple[str, Optional[str]]:
        return self.url, self.version

    def acquire_dependency(self):
        if self.version.startswith(GitDependency.VERSION_TAG):
            load_repo(
                self.get_dependency_directory(),
                self.url,
                tag=self.version[len(GitDependency.VERSION_TAG) :],
                use_existing=True,
            )
        elif self.version.startswith(GitDependency.VERSION_BRANCH):
            load_repo(
                self.get_dependency_directory(),
                self.url,
                branch=self.version[len(GitDependency.VERSION_BRANCH) :],
                use_existing=True,
            )
        else:
            raise NotImplementedError

    def _get_dependency_directory_relative(self) -> Path:
        return Path("git") / self.org / self.name


class DirectoryDependency(Dependency):
    def __init__(self, path):
        self.directory = Path(path).resolve()

    def get_id(self) -> Tuple[str, Optional[str]]:
        return str(self.directory), None

    def get_dependency_directory(self) -> Path:
        return self.directory

    def _get_dependency_directory_relative(self) -> Path:
        pass


class DogeDependency(Dependency):
    def __init__(self, dependency: Dependency, tasks: List[str] = None, doge_file_name: str = DOGE_FILE):
        super(DogeDependency, self).__init__()
        self.dependency = dependency
        self.tasks = tasks if tasks is not None else ["build"]
        self.doge_file_name = doge_file_name

    def get_id(self) -> Tuple[str, Optional[str]]:
        return self.dependency.get_id()

    def acquire_dependency(self):
        self.dependency.acquire_dependency()

    def get_dependency_directory(self) -> Path:
        return self.dependency.get_dependency_directory()

    def _get_dependency_directory_relative(self) -> Path:
        pass

    def get_doge_file_path(self):
        return self.get_dependency_directory() / self.doge_file_name

    def get_artifacts(self) -> Dict[str, List[Path]]:
        raise Exception("Must never be called")


def directory(path: Union[Path, str]) -> DirectoryDependency:
    return DirectoryDependency(path)


def git(repo: str, version: str = "branch:master", **kwargs) -> GitDependency:
    return GitDependency(repo, version)


def doge(dependency: Dependency, tasks: List[str] = None) -> DogeDependency:
    return DogeDependency(dependency, tasks)


def dependencies(*args):
    ContextHolder.INSTANCE.context.dependencies += args


def test_dependencies(*args):
    ContextHolder.INSTANCE.context.test_dependencies += args


def publish_artifacts(*artifacts: str):
    ContextHolder.INSTANCE.context.artifacts_to_publish += artifacts
