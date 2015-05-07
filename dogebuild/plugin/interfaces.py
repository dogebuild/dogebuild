#


class Plugin():
    """\
    Inherit yours plugin classes from this class
    """
    def get_active_tasks(self):
        """\
        This function should return array of task selected to run by dogefile (or another)
        """
        raise NotImplementedError()


class Task():
    """\
    This class represent single task
    """
    def run(self):
        """\
        Override task behavior in this function
        """
        raise NotImplementedError()
