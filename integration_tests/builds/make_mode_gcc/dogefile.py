from dogebuild import make_mode, task
from pathlib import Path
from shutil import rmtree

make_mode()

src_dir = Path('./src')
sources = src_dir.glob('**/*.cpp')
headers = src_dir.glob('**/*.h')

build_dir = Path('./build')
target = build_dir / 'hello-world'


@task()
def make_build_dir():
    build_dir.mkdir(parents=True, exist_ok=True)


@task()
def clean():
    rmtree(build_dir)