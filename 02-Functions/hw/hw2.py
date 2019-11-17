def atom(val=None):
    value = val

    def get_value():
        return value

    def set_value(v):
        nonlocal value
        value = v
        return value

    def process_value(*args):
        nonlocal value
        for arg in args:
            value = arg(value)
        return value

    def delete_value():
        nonlocal value
        del(value)

    return get_value, set_value, process_value, delete_value
