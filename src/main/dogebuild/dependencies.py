from subprocess import check_call
import os
from os import path
from shutil import rmtree


class GitDependency:
    GIT_REPO_FOLDER = path.expanduser(path.join('~', '.doge', 'repo', 'git'))

    def __init__(self, url, commit=None, tag=None, branch='master'):
        self.url = url
        self.name = url.split('/')[-1].replace('.git', '')
        self.org = url.split('/')[-2].split(':')[-1]
        self.commit = commit
        self.tag = tag
        self.branch = branch

    def acquire_dependency(self):
        self._assert_repo_folder_exists()

        if self.tag:
            tag_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'tags', self.tag)
            if not path.exists(tag_folder):
                os.makedirs(tag_folder)
                check_call(['git', 'clone', '-b', self.tag, self.url, '.'], cwd=tag_folder)
                rmtree(path.join(tag_folder, '.git'))

        elif self.branch:
            branch_folder = path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'branches', self.branch)
            if not path.exists(branch_folder):
                os.makedirs(branch_folder)
                check_call(['git', 'clone', '-b', self.branch, self.url, '.'], cwd=branch_folder)
            else:
                check_call(['git', 'checkout', self.branch], cwd=branch_folder)
                check_call(['git', 'pull', '--ff-only'], cwd=branch_folder)

        elif self.commit:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def get_doge_file_folder(self):
        if self.tag:
            return path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'tags', self.tag)
        elif self.branch:
            return path.join(GitDependency.GIT_REPO_FOLDER, self.org, self.name, 'branches', self.branch)
        elif self.commit:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def __str__(self):
        return self.url + " - " + self.branch

    def _assert_repo_folder_exists(self):
        os.makedirs(GitDependency.GIT_REPO_FOLDER, exist_ok=True)


class FolderDependency:
    def __init__(self, folder):
        self.folder = folder

    def acquire_dependency(self):
        pass

    def get_doge_file_folder(self):
        return self.folder

    def __str__(self):
        return self.folder


def folder(folder: str) -> FolderDependency:
    return FolderDependency(folder)


def git(repo: str, **kwargs) -> GitDependency:
    return GitDependency(repo, **kwargs)

