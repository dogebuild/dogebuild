import nox
from pathlib import Path


@nox.session
@nox.parametrize('build_dir', list(Path('./integration_tests/builds').glob('*')))
def run_tests(session, build_dir):
    session.install('.')
    session.cd(str(build_dir))
    session.run('doge', 'build')
