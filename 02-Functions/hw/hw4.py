import inspect
from functools import wraps

import hw1
import hw2
import hw3


def modified_func(func, *fixated_args, **fixated_kvargs):
    @wraps(func)
    def inner(*args, **kvargs):
        if fixated_args or fixated_kvargs:
            kvargs.update(fixated_kvargs)
            args += fixated_args
        return func(*args, **kvargs)
    inner.__doc__ = f"""
A func implementation of {inner.__name__}
with pre-applied arguments being:
{fixated_args}, {fixated_kvargs}
source_code:
{inspect.getsource(func)}"""
    return inner


if __name__ == '__main__':
    docstrings = []

    print('---\n', 'apply this function for hw1:')
    letters_range_with_zero_o = modified_func(hw1.letters_range, o='0')
    docstrings.append(letters_range_with_zero_o.__doc__)
    print(letters_range_with_zero_o('k', 'q'))

    print('---\n', 'apply this function for hw2:')
    atom_with_10 = modified_func(hw2.atom, 10)
    docstrings.append(atom_with_10.__doc__)
    get_, set_, process_, delete_ = atom_with_10()
    print(get_())
    set_(12)
    print(get_())

    print('---\n', 'apply this function for hw3:')
    set_make_it_count = modified_func(hw3.make_it_count, set_)
    set__counter = set_make_it_count()
    docstrings.append(set_make_it_count.__doc__)
    print('counter_name', hw3.counter_name)
    print(set__counter(27))
    print(get_())
    print('counter_name', hw3.counter_name)

    print('---\n', 'apply this function for built-in functions:')
    for func in ['min', 'max', 'any']:
        try:
            modify_func = modified_func(func)
        except TypeError:
            print(f"Can't get cource code for built-in function {func}", sep="\n")

    print("---\n", "Show docstrings for hw functions:\n", *docstrings)
