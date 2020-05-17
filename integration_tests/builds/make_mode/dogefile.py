from dogebuild import make_mode, task


make_mode()


@task
def task1():
    print("task1")


@task()
def task2():
    print("task2")


@task(
    name="Task 3 verbose name", depends=["task1", "task2"],
)
def task3():
    print("task3")


@task(depends=["Task 3 verbose name"])
def task4():
    print("task4")
