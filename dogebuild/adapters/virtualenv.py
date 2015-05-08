import subprocess
import os


class VirtualenvAdapter():
    def __init__(self, dir):
        self.dir = dir
        self.venv_dir = os.path.join(dir, '.venv')

    def enabled(self):
        os.path.exists(self.venv_dir) and os.path.isdir(self.venv_dir)

    def create(self):
        if os.path.exists(self.venv_dir):
            os.rmdir(self.venv_dir)
        os.makedirs(self.venv_dir)
        subprocess.call([
            "virtualenv",
            self.venv_dir,
            '--no-site-packages',
            ])
        print('.venv created')

    def activate(self):
        activate_file = os.path.join(self.venv_dir, 'Scripts', 'activate_this.py')
        try:
            file = open(activate_file)
            exec(file.read(), dict(__file__=activate_file))
            print(".venv activated!!!")
        finally:
            file.close()

