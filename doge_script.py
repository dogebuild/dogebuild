import sys
import os
import subprocess

import site

PREDEF_FILE = """#This is auto generated file
import pip


pip.main(['install', 'salve', '--require-venv'])
pip.main(['-V'])
"""

HELLO_MESS = "Hi! It's dogebuild! Call me with \"init\" to create file"


def run_doge():
    print("Doge greets you!")
    current_directory = os.getcwd()
    dogefile = os.path.join(current_directory, 'dogefile.py')
    venv_dir = os.path.join(current_directory, '.venv')

    if len(sys.argv) == 1:
        print(HELLO_MESS)
        if os.path.exists(dogefile) and os.path.isfile(dogefile):
            print("dogefile found. Wow!")

            if not os.path.exists(venv_dir):
                init_venv(venv_dir)
            activate_venv(venv_dir)
            print(sys.path)
            exec(open(dogefile).read())

    elif len(sys.argv) == 2:
        if sys.argv[1] == 'init':
            if os.path.exists(dogefile) and not os.path.isfile(dogefile):
                print("doggefile.py is not file.")

            elif os.path.exists(dogefile) and os.path.isfile(dogefile):
                rewrite = input("File exists. Print \"yes\" if you want to rewrite file. ")
                if rewrite:
                    init_file(dogefile)
                    print("File was rewrited.")

            else:
                init_file(dogefile)


def init_file(file_name):
    file = open(file_name, 'w')
    file.seek(0)
    file.truncate()
    file.write(PREDEF_FILE)
    file.close()


def init_venv(venv_dir):
    os.makedirs(venv_dir)
    subprocess.call(["virtualenv", venv_dir, '--no-site-packages', ])
    print("Venv created")


def activate_venv(venv_dir):
    activate_file = os.path.join(venv_dir, 'Scripts', 'activate_this.py')
    exec(open(activate_file).read(), dict(__file__=activate_file))
    print("venv activated!!!")





if __name__ == "__main__":
    run_doge()







