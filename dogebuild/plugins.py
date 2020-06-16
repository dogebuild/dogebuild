from logging import getLogger
from typing import Callable, List

from dogebuild.dogefile_internals.context import ContextHolder


class DogePlugin:
    NAME = "This is abstract doge plugin so this variable should never be used"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, artifacts_to_publish: List[str] = None):
        if artifacts_to_publish is None:
            artifacts_to_publish = []

        self.logger = getLogger(self.get_name())

        ContextHolder.INSTANCE.context.plugins.append(self)

        self.relman = ContextHolder.INSTANCE.context.relman
        self.dependencies = ContextHolder.INSTANCE.context.dependencies
        self.test_dependencies = ContextHolder.INSTANCE.context.test_dependencies

        self.artifacts_to_publish = artifacts_to_publish

    def add_task(
        self, task_callable: Callable, *, aliases: List[str] = None, depends: List[str] = None, phase: str = None
    ):
        self.relman.add_task(
            task_callable,
            aliases=aliases,
            dependencies=depends,
            plugin_name=self.NAME,
            phase=phase,
            plugin_instance=self,
        )
