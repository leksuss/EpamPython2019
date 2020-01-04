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
        return issubclass(args[0], self.list_exceptions)


with Suppressor(ArithmeticError, AttributeError):
    [].upper()
    1 / 0

print("It's fine")
