from typing import TypeVar, Callable, Optional, Generic

from dogebuild.dogefile_internals.context import ContextHolder

T = TypeVar("T")


def identity(a: T) -> T:
    return a


def add_parameter(name: str, *, parser: Callable[[str], T] = identity, default: Optional[T] = None) -> None:
    ContextHolder.INSTANCE.context.parameters += [Parameter(name, parser, default)]


class Parameter(Generic[T]):
    def __init__(self, name: str, parser: Callable[[str], T], default: Optional[T]):
        self.name = name
        self.parser = parser
        self.default = default
