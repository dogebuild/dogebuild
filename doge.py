import sys
import os

PREDEF_FILE = """1
demotest bla"""

HELLO_MESS = "Hi! It's dogebuild! Call me with \"init\""


def run_doge():
    print("Doge greets you!")
    current_directory = os.getcwd()
    dogefile = os.path.join(current_directory, 'dogefile.py')

    if len(sys.argv) == 1:
        print(HELLO_MESS)

    elif len(sys.argv) == 2:
        if sys.argv[1] == 'init':
            if os.path.exists(dogefile) and not os.path.isfile(dogefile):
                print("doggefile.py is not file")

            elif os.path.exists(dogefile) and os.path.isfile(dogefile):
                rewrite = input("File exists. Print \"yes\" if you want to rewrite file.")
                if rewrite:
                    init_file(dogefile)

            else:
                init_file(dogefile)


def init_file(file_name):
    file = open(file_name, 'w')
    file.seek(0)
    file.truncate()
    file.write(PREDEF_FILE)
    file.close()

if __name__ == "__main__":
    run_doge()







