from typing import Callable, List

from dogebuild.dogefile_internals.context import ContextHolder

DOGEFILE_TASK_PREFIX = "dogefile:"


def task(
    task_callable: Callable = None,
    *,
    aliases: List[str] = None,
    depends: List[str] = None,
    phase: str = None,
):
    if task_callable is None:
        return lambda func: task(func, aliases=aliases, depends=depends, phase=phase)

    if aliases is None:
        aliases = []
    if depends is None:
        depends = []

    relman = ContextHolder.INSTANCE.context.relman
    relman.add_task(task_callable, aliases=aliases, plugin_name=DOGEFILE_TASK_PREFIX, dependencies=depends, phase=phase)

    return task_callable
