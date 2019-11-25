from functools import reduce


problem9 = [a * b * (1000 - a - b) for b in range(500) for a in range(500)
            if (a**2 + b**2) == (1000 - a - b)**2 and
            a < b and
            b < (1000 - a - b)][0]
print(problem9)

problem6 = sum(i for i in range(1, 101))**2 - sum(i**2 for i in range(1, 101))
print(problem6)

problem48 = sum(i**i for i in range(1, 1001)) % 10**10
print(problem48)

problem40 = reduce(lambda x, y: x * y,
                   list((int(num) for idx, num in enumerate(
                         ''.join(str(i) for i in range(0, 1000001)))
                        if idx in [1, 10, 100, 1000, 10000, 100000, 1000000])))
print(problem40)
