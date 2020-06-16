import sys

from dogebuild.controller import DogeController


def main():
    controller = DogeController(sys.argv[1:])
    exit(controller.run())


if __name__ == "__main__":
    main()
