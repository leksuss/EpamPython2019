"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    orig_init = cls.__init__

    def __init__(self, *args, **kwargs):
        cls.counter += 1
        orig_init(self, *args, **kwargs)

    def get_created_instances(self=None):
        return cls.counter

    def reset_instances_counter(self=None):
        total_instances = cls.counter
        cls.counter = 0
        return total_instances

    cls.counter = 0
    cls.__init__ = __init__
    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter

    return cls


@instances_counter
class User:
    def __init__(self, some_attr):
        self.some_attr = some_attr

    def prt(self):
        print(self.some_attr)


if __name__ == '__main__':
    print(User.get_created_instances())  # 0
    user, _, _ = User('foo'), User('bar'), User(42)
    print(user.get_created_instances())  # 3
    print(user.reset_instances_counter())  # 3
    print(user.get_created_instances())  # 0
    user.prt()  # foo
