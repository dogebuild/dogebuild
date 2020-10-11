from dogebuild import make_mode, task, add_parameter

make_mode()

add_parameter("message")


@task
def build(message: str):
    print(message)
