import nox
from pathlib import Path
from itertools import chain


LINE_LENGTH = 120

STYLE_TARGETS = [
    "dogebuild",
    "integration_tests",
    "scripts",
    "tests",
    "noxfile.py",
    "setup.py",
]

FLAKE8_IGNORE = [
    "E203",
    "E231",
    "W503",
]


@nox.session
def unit_tests(session):
    session.install(".")
    session.install("pytest")
    session.run("pytest", "tests")


@nox.session
@nox.parametrize("build_dir", list(Path("./integration_tests/builds").glob("*")))
def integration_tests(session, build_dir):
    session.install(".")
    session.cd(str(build_dir))
    session.run("doge", "build")


@nox.session
def style(session):
    session.install("flake8", "black", "isort")

    source_files = map(str, chain.from_iterable(map(lambda p: Path(p).glob("**/*.py"), STYLE_TARGETS)))

    session.run("black", "--target-version", "py38", "--line-length", f"{LINE_LENGTH}", "--check", *STYLE_TARGETS)
    session.run(
        "flake8",
        "--max-line-length",
        f"{LINE_LENGTH}",
        "--extend-ignore",
        ",".join(FLAKE8_IGNORE),
        "--show-source",
        *STYLE_TARGETS,
    )
    session.run(
        "isort",
        "--multi-line",
        "3",
        "--trailing-comma",
        "--force-grid-wrap",
        "0",
        "--use-parentheses",
        "--line-width",
        f"{LINE_LENGTH}",
        "--check-only",
        *source_files,
    )
