from typing import List, Callable

from dogebuild.common import sanitize_name
from dogebuild.dogefile_internals.context import ContextHolder
from dogebuild.dogefile_internals.relations import TaskRelationManager


DOGEFILE_TASK_PREFIX = 'dogefile:'


def task(task_callable: Callable = None, *, name: str = None, depends: List[str] = None, phase: str = None):
    if task_callable is None:
        return lambda func: task(func, name=name, depends=depends, phase=phase)

    if not depends:
        depends = []

    full_name_depends = []
    for dependency in depends:
        if TaskRelationManager.is_task_short_name(dependency):
            dependency = DOGEFILE_TASK_PREFIX + dependency
        full_name_depends.append(sanitize_name(dependency))
    depends = full_name_depends

    relman = ContextHolder.INSTANCE.context.relman
    task_name = name
    if not task_name:
        task_name = task_callable.__name__
    task_name = DOGEFILE_TASK_PREFIX + sanitize_name(task_name)

    relman.add_task(task_name, task_callable)
    relman.add_dependency(task_name, depends)

    if phase:
        relman.add_dependency(phase, [task_name])

    return task_callable


