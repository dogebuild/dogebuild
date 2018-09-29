from typing import Dict, Callable, List


class DagContext:
    def __init__(self):
        self.deps = {}

    def depends_on(self, *args: List[str]):
        def decorator(func):
            self.deps[func.__name__] = args
            return func
        return decorator


class DogePlugin:
    NAME = 'This is abstract doge plugin so this variable should never be used'
    
    def __init__(self, tasks: Dict[str, Callable], dag_context: DagContext):
        self.tasks = tasks
        self.dag_context = dag_context

    @classmethod
    def get_name(cls):
        return cls.NAME
