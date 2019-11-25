from functools import reduce


def is_armstrong(number):
    return int(reduce(lambda x, y: int(x) +
                      int(y)**len(str(number)), list(str(number)))) == number


assert is_armstrong(153) == True, 'Число Армстронга'
assert is_armstrong(10) == False, 'Не число Армстронга'

