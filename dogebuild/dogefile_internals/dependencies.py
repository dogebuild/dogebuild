import os
from os import path
from pathlib import Path
from shutil import rmtree
from subprocess import check_call
from typing import Optional, Tuple

from dogebuild.common import DOGE_FILE, DOGE_MODULES_DIRECTORY
from dogebuild.dogefile_internals.context import ContextHolder


class Dependency:
    def __init__(self, **kwargs):
        self.context = kwargs

    def get_id(self) -> Tuple[str, Optional[str]]:
        raise NotImplementedError

    def __str__(self):
        id, version = self.get_id()
        if not version:
            return id
        else:
            return "{} ({})".format(id, version)

    def acquire_dependency(self):
        raise NotImplementedError()

    def get_doge_file(self) -> Optional[Path]:
        return None


class GitDependency(Dependency):
    GIT_REPO_FOLDER = Path(DOGE_MODULES_DIRECTORY) / "git"

    VERSION_TAG = "tag:"
    VERSION_BRANCH = "branch:"
    # TODO: make VERSION_COMMIT

    def __init__(self, url, version, **kwargs):
        super().__init__(**kwargs)

        self.url = url
        self.version = version
        self.original_version = None
        self.name = url.split("/")[-1].replace(".git", "")
        self.org = url.split("/")[-2].split(":")[-1]
        self.dependencies = []

    def acquire_dependency(self):
        self._assert_repo_folder_exists()

        if self.version.startswith(GitDependency.VERSION_TAG):
            tag = self.version[len(GitDependency.VERSION_TAG) :]
            tag_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, "tags", tag)
            if not path.exists(tag_folder):
                os.makedirs(tag_folder)
                check_call(["git", "clone", "-b", tag, self.url, "."], cwd=tag_folder)
                rmtree(path.join(tag_folder, ".git"))

        elif self.version.startswith(GitDependency.VERSION_BRANCH):
            branch = self.version[len(GitDependency.VERSION_BRANCH) :]
            branch_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, "branches", branch)
            if not path.exists(branch_folder):
                os.makedirs(branch_folder)
                check_call(["git", "clone", "-b", branch, self.url, "."], cwd=branch_folder)
            else:
                check_call(["git", "checkout", branch], cwd=branch_folder)
                check_call(["git", "pull", "--ff-only"], cwd=branch_folder)

        else:
            raise NotImplementedError

    def get_doge_file(self) -> Optional[Path]:
        if self.version.startswith(GitDependency.VERSION_TAG):
            tag = self.version[len(GitDependency.VERSION_TAG) :]
            return Path(GitDependency.GIT_REPO_FOLDER) / self.org / self.name / "tags" / tag / DOGE_FILE

        elif self.version.startswith(GitDependency.VERSION_BRANCH):
            branch = self.version[len(GitDependency.VERSION_BRANCH) :]
            return Path(GitDependency.GIT_REPO_FOLDER) / self.org / self.name / "branches" / branch / DOGE_FILE

        else:
            raise NotImplementedError

    def get_id(self) -> Tuple[str, Optional[str]]:
        return self.url, self.version

    def _assert_repo_folder_exists(self):
        os.makedirs(GitDependency.GIT_REPO_FOLDER, exist_ok=True)


class FolderDependency(Dependency):
    def __init__(self, folder, **kwargs):
        super().__init__(**kwargs)

        self.folder = Path(folder).resolve()
        self.version = None
        self.original_version = None
        self.dependencies = []

    def acquire_dependency(self):
        pass

    def get_doge_file(self) -> Optional[Path]:
        return self.folder / DOGE_FILE

    def get_id(self) -> Tuple[str, Optional[str]]:
        return str(self.folder), None


def folder(folder: str, **kwargs) -> FolderDependency:
    return FolderDependency(folder, **kwargs)


def git(repo: str, version: str = "branch:master", **kwargs) -> GitDependency:
    return GitDependency(repo, version, **kwargs)


def dependencies(*args):
    ContextHolder.INSTANCE.context.dependencies += args


def test_dependencies(*args):
    ContextHolder.INSTANCE.context.test_dependencies += args
