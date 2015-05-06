import subprocess


class PipAdapter():
    """ I use this as a class, cause I cannot make pip library work
        in virtualenv normally. If I succeed in future, I will rewrite it.
    """
    def install(self, *args):
        command = ["pip", "install"]
        for x in args:
            command.append(x)
        subprocess.call(command)

