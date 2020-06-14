from dogebuild import make_mode, task

make_mode()


@task
def build():
    raise Exception("Build must fail")
