from dogebuild import make_mode, task
from pathlib import Path
from shutil import rmtree, copy
from subprocess import run

make_mode()

src_dir = Path('./src')
sources = src_dir.glob('**/*.cpp')
headers = src_dir.glob('**/*.h')

build_dir = Path('./build')
target = build_dir / 'libtools.a'


@task()
def make_build_dir():
    build_dir.mkdir(parents=True, exist_ok=True)


@task()
def clean():
    rmtree(build_dir)


@task(depends=['make_build_dir'])
def build():
    for src in sources:
        run(
            [
                'g++',
                '-c',
                '-fPIC',
                '-o', str((build_dir / src.name).with_suffix('.o')),
                str(src),
                f'-I{headers}',
            ],
            check=True,
        )

    object_files = build_dir.glob('**/*.o')
    run([
        'ar',
        'rcs',
        str(target),
        *map(str, object_files),
    ])

    headers_dir = build_dir / 'headers'
    headers_dir.mkdir(parents=True, exist_ok=True)
    for header in headers:
        rel = header.relative_to(src_dir)
        copy(str(header), str(headers_dir / rel))

    return 0, {
        'libraries': [
            target,
        ],
        'headers': [
            headers_dir,
        ],
    }
