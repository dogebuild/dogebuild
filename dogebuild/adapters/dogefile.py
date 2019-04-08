import os


PREDEF_FILE = """#This is auto generated file
from dogebuild.doge import Doge


d = Doge()
h = d.use_plugin('hello')
h.message = 'Not def'
d.build()
"""


class DogefileAdapter():
    def __init__(self, dir, file='dogefile.py'):
        self.dogefile = os.path.join(dir, file)

    def exist(self):
        return os.path.exists(self.dogefile) and os.path.isfile(self.dogefile)

    def run(self):
        try:
            file = open(self.dogefile)
            exec(file.read())
        finally:
            file.close()

    def create(self):
        try:
            file = open(self.dogefile, 'w')
            file.seek(0)
            file.truncate()
            file.write(PREDEF_FILE)
        finally:
            file.close()

