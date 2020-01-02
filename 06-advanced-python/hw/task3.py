""""
Реализовать контекстный менеджер, который подавляет переданные исключения
with Suppressor(ZeroDivisionError):
    1/0
print("It's fine")
"""


class Suppressor:
    def __init__(self, *args):
        self.list_exceptions = args

    def __enter__(self):
        pass

    def __exit__(self, *args):
        return args[0] in self.list_exceptions


with Suppressor(ZeroDivisionError, AttributeError):
    [].upper()
    1 / 0

print("It's fine")
