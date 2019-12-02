import timeit
from functools import wraps


def count_stat(stat):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            stat['run_count'] += 1
            start = timeit.default_timer()
            res = func(*args, **kwargs)
            end = timeit.default_timer()
            stat['summary_time'] += end - start
            return res
        return inner
    return decorator


stat1 = {'run_count': 0, 'summary_time': 0}
stat2 = {'run_count': 0, 'summary_time': 0}
stat3 = {'run_count': 0, 'summary_time': 0}


@count_stat(stat=stat1)
def fib_rec(n):
    """Calc fibonacci by recursion"""
    return fib_rec(n - 1) + fib_rec(n - 2) if n > 2 else 1


@count_stat(stat=stat2)
def fib_rec_listcache(n, cache=None):
    """Calc fibonacci by recursion with list cache"""
    if not cache:
        cache = [0, 1, 1]
    if n < len(cache):
        return cache[n]
    cache.append(fib_rec_listcache(n - 1, cache))
    return cache[n] + cache[n - 1]


@count_stat(stat=stat3)
def fib_simple(n):
    """Calс fibonacci by sequential addition"""
    x, y = 0, 1
    for i in range(n):
        x, y = y, x + y
    return x


num = 25

print(fib_rec.__doc__, num, fib_rec(num), stat1, sep=', ')
print(fib_rec_listcache.__doc__, num, fib_rec_listcache(num), stat2, sep=', ')
print(fib_simple.__doc__, fib_simple(num), stat3, sep=', ')
