import subprocess
import os


class VirtualenvAdapter():
    def __init__(self, dir, venv_dir_name='.venv'):
        self.dir = dir
        self.venv_dir = os.path.join(dir, venv_dir_name)

    def enabled(self):
        return os.path.exists(self.venv_dir) and os.path.isdir(self.venv_dir)

    def create(self):
        if os.path.exists(self.venv_dir):
            os.rmdir(self.venv_dir)
        os.makedirs(self.venv_dir)
        subprocess.call([
            "virtualenv",
            self.venv_dir,
            '--system-site-packages',
        ])
        print('Virtualenv created in "%s"' % self.venv_dir)

    def activate(self):
        activate_file = os.path.join(self.venv_dir, 'Scripts', 'activate_this.py')
        with open(activate_file) as file:
            exec(file.read(), dict(__file__=activate_file))
            print('Virtualenv activated from "%s"' % self.venv_dir)
