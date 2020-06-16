from pathlib import Path

import nox


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

    session.run("black", "--version")
    session.run("black", "--check", "--target-version", "py38", "--line-length", f"{LINE_LENGTH}", *STYLE_TARGETS)

    session.run("flake8", "--version")
    session.run(
        "flake8",
        "--max-line-length",
        f"{LINE_LENGTH}",
        "--extend-ignore",
        ",".join(FLAKE8_IGNORE),
        "--show-source",
        *STYLE_TARGETS,
    )

    # Isort is broken for virtualenvs. IDK hpw to fix it now
    # source_files = map(str, chain.from_iterable(map(lambda p: Path(p).glob("**/*.py"), STYLE_TARGETS)))
    # session.run("isort", "--version")
    # session.run(
    #     "isort",
    #     "--check-only",
    #     "--project",
    #     "dogebuild",
    #     "--multi-line",
    #     "3",
    #     "--trailing-comma",
    #     "--force-grid-wrap",
    #     "0",
    #     "--use-parentheses",
    #     "--line-width",
    #     f"{LINE_LENGTH}",
    #     *source_files,
    # )
