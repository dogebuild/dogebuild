from abc import ABC, abstractmethod


class Plugin(ABC):
    """\
    Inherit yours plugin_old classes from this class
    """
    @abstractmethod
    def get_active_tasks(self):
        """\
        This function should return array of task selected to run by dogefile (or another)
        """
        raise NotImplementedError()


class Task(ABC):
    """\
    This class represent single task
    """
    @abstractmethod
    def run(self):
        """\
        Override task behavior in this function
        """
        raise NotImplementedError()
