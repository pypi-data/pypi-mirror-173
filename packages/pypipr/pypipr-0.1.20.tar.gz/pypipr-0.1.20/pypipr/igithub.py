IGITHUB = True

"""PYPIPR Module"""
from .iconsole import print_colorize, print_log, console_run

"""PYTHON Standard Module"""


"""PYPI Module"""


def github_push():
    def console(t, c):
        print_log(t)
        console_run(c)

    def console_input(prompt):
        print_colorize(prompt, text_end="")
        return input()

    console("Checking files", "git status")
    msg = console_input("Commit Message if any or empty to exit : ")
    if msg:
        console("Mempersiapkan files", "git add .")
        console("Menyimpan files", f'git commit -m "{msg}"')
        console("Mengirim files", "git push")
        print_log("Finish")


def github_pull():
    print_log("Git Pull")
    console_run("git pull")
