import math
from src.decoder import *


class Griewangk:
    def __init__(self, n):
        self.n = n
        self.bits = 10

    def __call__(self, bit_array):
        assert len(bit_array) == self.bits * self.n

        X = [self.decode(bit_array[self.bits * i:self.bits * (i + 1)]) for i in range(self.n)]

        temp = 1
        for i, x in enumerate(X):
            temp *= math.cos(x / math.sqrt(i + 1))

        result = 1 + sum([x**2 / 4000 for x in X]) - temp

        return -math.fabs(result)

    def decode(self, bit_array):
        assert len(bit_array) == self.bits
        return decode_u2(bit_array)  # integer [-512, 511]


class Rastrigin:
    def __init__(self, n):
        self.n = n
        self.bits = 14

    def __call__(self, bit_array):
        assert len(bit_array) == self.bits * self.n

        X = [self.decode(bit_array[self.bits * i:self.bits * (i + 1)]) for i in range(self.n)]
        result = 10 * len(X) + sum([x**2 - 10 * math.cos(2 * math.pi * x) for x in X])

        return -math.fabs(result)

    def decode(self, bit_array):
        assert len(bit_array) == self.bits

        sign = 1 if bit_array[0] == 0 else -1
        result = 0

        for i, bit in enumerate(bit_array[1:]):
            result += bit * 2.0**(2 - i)

        return sign * result  # real [-7.9990234375, 7.9990234375]
