from dogebuild import make_mode, task

make_mode()


@task
def build():
    return 1, {}
