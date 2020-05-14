from dogebuild.dogefile_internals.context import ContextHolder


def modules(*args: str):
    ContextHolder.INSTANCE.context.modules += args
