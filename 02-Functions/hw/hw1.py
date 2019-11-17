def letters_range(*args, **kvargs):

    """Range for letters"""

    len_args = len(args)

    def is_char(s):
        return isinstance(s, str) and s.isalpha() and len(s) == 1

    if len_args == 1 and is_char(args[0]):
        range_params = ord('a'), ord(args[0]), 1
    elif len_args == 2 and is_char(args[0]) and is_char(args[1]):
        range_params = ord(args[0]), ord(args[1]), 1
    elif len_args == 3 and is_char(args[0]) and is_char(args[1]) and \
            isinstance(args[2], int):
        range_params = ord(args[0]), ord(args[1]), args[2]
    else:
        raise TypeError('Wrong positional arguments!')
    res = list(map(chr, range(*range_params)))
    if kvargs:
        res = [str(kvargs[i]) if i in kvargs else i for i in res]
    return res
