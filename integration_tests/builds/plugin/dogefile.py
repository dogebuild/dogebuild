from dogebuild import task
from dogebuild.plugins import DogePlugin


class TestPlugin(DogePlugin):
    NAME = "test-plugin"

    def task_1(self):
        print('task_1')

    def task_2(self):
        print('task_2')

    def task_3(self):
        print('task_3')

    def task_4(self):
        print('task_4')
        raise Exception('Boo')

    def __init__(self):
        super(TestPlugin, self).__init__()

        self.add_task(self.task_1)
        self.add_task(self.task_2, depends=['task_1'])
        self.add_task(self.task_3, depends=['task_1'])
        self.add_task(self.task_4, depends=['task_3', 'task_2'], phase='build')




TestPlugin()
