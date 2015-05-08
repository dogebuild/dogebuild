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

    args = process_arguments(sys.argv)

    if 'no' in args:
        print(HELLO_MESS)
        if dogefile.exist():
            print("dogefile.py found. Wow!")
            if venv.enabled():
                print(".venv found")
                venv.activate()
            dogefile.run()

    if 'init' in args:
        if dogefile.exist():
            answer = input('Doge file exists. Print "yes" to rewrite.\n')
            if answer != 'yes':
                return
            dogefile.create()

        if 'use_venv' in args:
            venv.create()

    if 'help' in args:
        show_help()


def show_help():
    print("""\
    Run 'doge' to start build.
    Run 'doge init' to init. Use '--no-venv' key to skip virtualenv creation
    Run 'doge help' to help.
    """)


def process_arguments(arg_array):
    """\
    Parse arguments and return dict with options
    """

    if len(arg_array) == 0:
        raise Exception("No arguments in array.")

    # Default
    if len(arg_array) == 1:
        return {'no': True}

    # Called with command
    args = {}
    command = arg_array[1]

    # Init
    if command == 'init':
        args['init'] = True
        if '--no-venv' not in arg_array:
            args['use_venv'] = True

    # Help
    elif command == 'help':
        args['help'] = True

    # Unknown command
    else:
        args['unknown'] = True

    return args

