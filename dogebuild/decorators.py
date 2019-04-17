from typing import List

from dogebuild.context import ContextHolder


def task(name: str = None, depends: List[str] = None, phase: str = None):
    if not depends:
        depends = []

    relman = ContextHolder.CONTEXT.relman

    def decorator(task_callable):
        task_name = name
        if not task_name:
            task_name = task_callable.__name__
        task_name = 'dogefile:' + _sanitize_name(task_name)

        relman.add_task(task_name, task_callable)
        relman.add_dependency(task_name, depends)

        if phase:
            relman.add_dependency(phase, [task_name])

        return task_callable

    return decorator


def _sanitize_name(name: str):
    return name.replace('_', '-')
