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

    q_map = '', 'i', 'j', 'k',
    q_const = 'a', 'b', 'c', 'd',

    @staticmethod
    def _is_digit(list_symb):
        return all(map(lambda symb: isinstance(symb, (int, float)), list_symb))

    def __init__(self, *args, **kwargs):
        if args and self._is_digit(args):
            self.q = list(args)
            while len(self.q) <= 4:
                self.q.append(0)
        elif kwargs and self._is_digit(kwargs.values()):
            self.q = [
                kwargs.get('a', 0),
                kwargs.get('b', 0),
                kwargs.get('c', 0),
                kwargs.get('d', 0),
            ]
        else:
            raise ValueError(Quaternion.__doc__)

    def __add__(self, other):
        return self.__class__(*[sum(pair) for pair in zip(self.q, other.q)])

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
        return self.__class__(*res)

    def pair(self):
        return self.__class__(*[self.q[0], -self.q[1], -self.q[2], -self.q[3]])

    def __abs__(self):
        return (sum(map(lambda x: x**2, self.q)))**0.5

    def __truediv__(self, other):
        paired_other = other.pair()
        reversed_other = paired_other.__mul__(1 / other.__abs__()**2)
        return self.__mul__(reversed_other)

    def __str__(self):
        res_str = str(self.q[0])
        signs = map(lambda x: ' - ' if x < 0 else ' + ', self.q[1:])
        for sign, real_n, i_n in zip(signs, self.q[1:], self.q_map[1:]):
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

    # with default zeros
    q3 = Quaternion(4)
    q4 = Quaternion(a=5, b=-1)

    # with invalid values
    try:
        q5 = Quaternion(4, 'invalud value')
    except ValueError as e:
        print(e, 'q5 error')
    try:
        q6 = Quaternion(a=1, c='invalud value')
    except ValueError as e:
        print(e, 'q6 error')

    print(q * q2)
    print(q + q2)
    print(q * 10)
    print(q / q2)
    print(q2 / q2)
    print(q == q)
    print(q == q2)
    print(repr(q))
    print(eval(repr(q)))
