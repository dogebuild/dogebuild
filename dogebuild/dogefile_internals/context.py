from os import chdir, getcwd
from pathlib import Path
from typing import Dict, List

from dogebuild.dogefile_internals.errors import DogeFileConfigurationError
from dogebuild.dogefile_internals.relations import TaskRelationManager


class Context:
    def __init__(self, doge_file_id: str, phases: Dict[str, List[str]] = None):
        self.relman = TaskRelationManager(doge_file_id, phases)
        self.plugins = []
        self.dependencies = []
        self.test_dependencies = []
        self.code_context = None
        self.modules = []
        self.artifacts_to_publish = []
        self.parameters = []

    def verify(self):
        self.relman.verify()


class ContextHolder:
    INSTANCE = None

    def __init__(self, doge_file_id: str):
        self._doge_file_id = doge_file_id
        self._context = None
        self._phases = None
        self._phases_set = False
        self._globals_context = {}

    @property
    def context(self):
        return self._context

    @context.getter
    def context(self):
        if not self._context:
            self._context = Context(self._doge_file_id, self._phases)
        return self._context

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value: Dict):
        if self._phases_set:
            raise DogeFileConfigurationError("Lifecycle already set")
        self._phases = value
        self._phases_set = True

    @property
    def globals_context(self):
        return self._globals_context

    @globals_context.getter
    def globals_context(self):
        return self._globals_context


class ContextHolderGuard:
    def __init__(self, dogefile: Path, doge_file_id: str):
        self.holder = ContextHolder(doge_file_id)
        self.dogefile = dogefile
        self.cwd = None

    def __enter__(self) -> ContextHolder:
        self.cwd = getcwd()
        chdir(self.dogefile.parent)

        ContextHolder.INSTANCE = self.holder
        return self.holder

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self.cwd)

        ContextHolder.INSTANCE = None
        self.holder.context.code_context = self.holder.globals_context


def lifecycle(phases: Dict[str, List[str]] = None):
    ContextHolder.INSTANCE.phases = phases


def make_mode():
    lifecycle({})
