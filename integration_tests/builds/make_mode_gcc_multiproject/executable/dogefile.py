from pathlib import Path
from shutil import rmtree
from subprocess import run

from dogebuild import dependencies, directory, doge, make_mode, task

make_mode()

dependencies(doge(directory("../library")))

src_dir = Path("./src")
sources = src_dir.glob("**/*.cpp")
headers_dir = src_dir

build_dir = Path("./build")
target = build_dir / "hello-world"


@task()
def make_build_dir():
    build_dir.mkdir(parents=True, exist_ok=True)


@task()
def clean():
    rmtree(build_dir)


@task(depends=["make_build_dir"])
def build(libraries, headers):
    run(
        [
            "g++",
            *map(lambda header: f"-I{header}", headers),
            "-o",
            str(target),
            *map(str, sources),
            *map(lambda library: f"-L{library.parent}", libraries),
            *map(lambda library: f'-l{library.with_suffix("").name[3:]}', libraries),
        ],
        check=True,
    )
