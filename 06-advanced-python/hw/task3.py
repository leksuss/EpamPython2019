""""
Реализовать контекстный менеджер, который подавляет переданные исключения
with Suppressor(ZeroDivisionError):
    1/0
print("It's fine")
"""


class Suppressor:
    def __init__(self, error):
        self.error = error

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if args[0] == self.error:
            return True


with Suppressor(ZeroDivisionError):
    print(1 / 0)
print("It's fine")
