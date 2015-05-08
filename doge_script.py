import sys
import os
import subprocess

from dogebuild.adapters.dogefile import DogefileAdapter
from dogebuild.adapters.virtualenv import VirtualenvAdapter
from dogebuild.adapters.pip import PipAdapter


PREDEF_FILE = """#This is auto generated file
from dogebuild.doge import Doge


d = Doge()
h = d.use_plugin('hello')
h.message = 'Not def'
d.build()
"""

HELLO_MESS = "Hi! It's dogebuild! Call me with \"init\" to create file"


def run_doge():
    current_directory = os.getcwd()
    pip = PipAdapter()
    venv = VirtualenvAdapter(current_directory)
    dogefile = DogefileAdapter(current_directory)

    if len(sys.argv) == 1:
        # Called with no arguments
        print(HELLO_MESS)
        if dogefile.exist():
            print("dogefile.py found. Wow!")
            if venv.enabled():
                venv.activate()
            dogefile.run()

    elif len(sys.argv) == 2:
        # Called with one argument
        if sys.argv[1] == 'init':
            if dogefile.exist():
                answer = input('Doge file exists. Print "yes" to rewrite.\n')
                if answer == 'yes':
                    dogefile.create()
            else:
                dogefile.create()


def process_arguments(arg_array):
    args = {}
    if len(arg_array) == 1:
        args['no'] = True
    elif len(arg_array) >= 2:
        if sys.argv[1] == 'init':
            args['init'] = True
    else:
        pass
    return args

