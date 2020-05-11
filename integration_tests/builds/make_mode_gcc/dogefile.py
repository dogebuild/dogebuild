from dogebuild import make_mode, task
from pathlib import Path
from shutil import rmtree
from subprocess import run

make_mode()

src_dir = Path('./src')
sources = src_dir.glob('**/*.cpp')
headers = src_dir

build_dir = Path('./build')
target = build_dir / 'hello-world'


@task()
def make_build_dir():
    build_dir.mkdir(parents=True, exist_ok=True)


@task()
def clean():
    rmtree(build_dir)


@task(depends=['make_build_dir'])
def build():
    run(
        [
            'g++',
            '-o', str(target),
            *map(str, sources),
            f'-I{headers}',
        ],
        check=True,
    )
