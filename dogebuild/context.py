from typing import Dict, List

from dogebuild.relations import TaskRelationManager


class Context:
    def __init__(self, phases: Dict[str, List[str]] = None):
        self.relman = TaskRelationManager(phases)
        self.plugins = []
        self.dependencies = []
        self.test_dependencies = []
        self.code_context = {}


class ContextHolder:
    CONTEXT = None

    @staticmethod
    def create(phases=None) -> Context:
        ContextHolder.CONTEXT = Context(phases)

    @staticmethod
    def clear_and_get() -> Context:
        context = ContextHolder.CONTEXT
        ContextHolder.CONTEXT = None
        return context


def lifecycle(phases: Dict[str, List[str]] = None):
    ContextHolder.create(phases)


def make_mode():
    lifecycle({})
