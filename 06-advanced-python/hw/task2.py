"""
Реализовать класс Quaternion, позволяющий работать с кватернионами
https://ru.wikipedia.org/wiki/%D0%9A%D0%B2%D0%B0%D1%82%D0%B5%D1%80%D0%BD%D0%B8%D0%BE%D0%BD
Функциональность (магическими методами):
- сложение
- умножение
- деление
- сравнение
- нахождение модуля
- строковое представление и repr
По желанию:
- взаимодействие с числами других типов
"""


class Quaternion:
    """
    You can set this Quaternion -10 + 12i + 51j - 30k
    as kwargs: Quaternion(a=-10, b=12, c=51, d=-30)
    or as args: Quaternion(-10, 12, 51, -30)
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 4:
            self.q = args
        elif kwargs.keys() == {'a', 'b', 'c', 'd'}:
            self.q = [kwargs['a'], kwargs['b'], kwargs['c'], kwargs['d']]
        else:
            raise ValueError(Quaternion.__doc__)

        self.q_mapping = '', 'i', 'j', 'k'

    def __add__(self, other):
        return Quaternion(*[sum(i) for i in zip(self.q, other.q)])

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            res_s = self.q[0] * other.q[0] - \
                self.q[1] * other.q[1] - \
                self.q[2] * other.q[2] - \
                self.q[3] * other.q[3]

            res_i = self.q[1] * other.q[0] + \
                self.q[0] * other.q[1] + \
                self.q[2] * other.q[3] - \
                self.q[3] * other.q[2]

            res_j = self.q[2] * other.q[0] + \
                self.q[0] * other.q[2] + \
                self.q[3] * other.q[1] - \
                self.q[1] * other.q[3]

            res_k = self.q[3] * other.q[0] + \
                self.q[0] * other.q[3] + \
                self.q[1] * other.q[2] - \
                self.q[2] * other.q[1]
            res = [res_s, res_i, res_j, res_k]
        elif isinstance(other, (float, int)):
            res = [val * other for val in self.q]
        return Quaternion(*res)

    def __pair__(self):
        return Quaternion(*[self.q[0], -self.q[1], -self.q[2], -self.q[3]])

    def __abs__(self):
        return (sum(list(map(lambda x: x**2, self.q))))**0.5

    def __truediv__(self, other):
        paired_other = other.__pair__()
        reversed_other = paired_other.__mul__(1 / other.__abs__()**2)
        return self.__mul__(reversed_other)

    def __str__(self):
        res_str = str(self.q[0])
        signs = map(lambda x: ' - ' if x < 0 else ' + ', self.q[1:])
        for sign, real_n, i_n in zip(signs, self.q[1:], self.q_mapping[1:]):
            if real_n:
                res_str += sign + str(abs(real_n)) + i_n
        return res_str

    def __eq__(self, other):
        return self.q == other.q

    def __repr__(self):
        return f"Quaternion(*[{', '.join(map(str, self.q))}])"


if __name__ == '__main__':

    q = Quaternion(**{'a': 1, 'b': 3, 'c': 4, 'd': 3})
    q2 = Quaternion(*[4, 9, -1, -3])

    print(q)
    print(q * q2)
    print(q * 10)
    print(q / q2)
    print(q2 / q2)
    print(q == q)
    print(q == q2)
    print(repr(q))
    print(eval(repr(q)))
