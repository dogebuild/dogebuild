from subprocess import check_call
import os
from os import path
from shutil import rmtree

from typing import Tuple, Union


class Dependency:
    def get_id(self) -> Tuple[str, Union[str, None]]:
        raise NotImplementedError

    def __str__(self):
        id, version = self.get_id()
        if not version:
            return id
        else:
            return '{} ({})'.format(id, version)


class GitDependency(Dependency):
    GIT_REPO_FOLDER = path.expanduser(path.join('~', '.doge', 'repo', 'git'))

    VERSION_TAG = 'tag:'
    VERSION_BRANCH = 'branch:'
    # TODO: make VERSION_COMMIT

    def __init__(self, url, version):
        self.url = url
        self.version = version
        self.original_version = None
        self.name = url.split('/')[-1].replace('.git', '')
        self.org = url.split('/')[-2].split(':')[-1]
        self.dependencies = []

    def acquire_dependency(self):
        self._assert_repo_folder_exists()

        if self.version.startswith(GitDependency.VERSION_TAG):
            tag = self.version[len(GitDependency.VERSION_TAG):]
            tag_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'tags', tag)
            if not path.exists(tag_folder):
                os.makedirs(tag_folder)
                check_call(['git', 'clone', '-b', tag, self.url, '.'], cwd=tag_folder)
                rmtree(path.join(tag_folder, '.git'))

        elif self.version.startswith(GitDependency.VERSION_BRANCH):
            branch = self.version[len(GitDependency.VERSION_BRANCH):]
            branch_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'branches', branch)
            if not path.exists(branch_folder):
                os.makedirs(branch_folder)
                check_call(['git', 'clone', '-b', branch, self.url, '.'], cwd=branch_folder)
            else:
                check_call(['git', 'checkout', branch], cwd=branch_folder)
                check_call(['git', 'pull', '--ff-only'], cwd=branch_folder)

        else:
            raise NotImplementedError

    def get_doge_file_folder(self):
        if self.version.startswith(GitDependency.VERSION_TAG):
            tag = self.version[len(GitDependency.VERSION_TAG):]
            return path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'tags', tag)

        elif self.version.startswith(GitDependency.VERSION_BRANCH):
            branch = self.version[len(GitDependency.VERSION_BRANCH):]
            return path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'branches', branch)

        else:
            raise NotImplementedError

    def get_id(self) -> Tuple[str, Union[str, None]]:
        return self.url, self.version

    def _assert_repo_folder_exists(self):
        os.makedirs(GitDependency.GIT_REPO_FOLDER, exist_ok=True)


class FolderDependency(Dependency):
    def __init__(self, folder):
        self.folder = folder
        self.version = None
        self.original_version = None
        self.dependencies = []

    def acquire_dependency(self):
        pass

    def get_doge_file_folder(self):
        return self.folder

    def get_id(self) -> Tuple[str, Union[str, None]]:
        return self.folder, None


def folder(folder: str) -> FolderDependency:
    return FolderDependency(folder)


def git(repo: str, version: str='branch:master') -> GitDependency:
    return GitDependency(repo, version)

