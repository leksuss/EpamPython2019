counter_name = 0


def make_it_count(func):
    def default(*args, **kvargs):
        global counter_name
        counter_name += 1
        return func(*args, **kvargs)
    return default
