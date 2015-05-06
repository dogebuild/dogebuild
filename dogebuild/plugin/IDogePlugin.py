class IDogePlugin():
    """ Inherit you plugin class from this interface
    """
    def get_active_tasks(self):
        """ This function returns task selected as active after settings in dogefile (or another). All task objects
        will be passed to run_task() function after sorting in main Doge program
        :return: Active tasks of this plugin
        """
        raise NotImplementedError

    def run_task(self, task):
        """ Main Doge program call this function with task when time is came =)
        :param task:
        """
        raise NotImplementedError
