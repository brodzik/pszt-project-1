import math
from src.decoder import *


def decode_rastrigin(bit_array):
    assert len(bit_array) > 3

    sign = 1 if bit_array[0] == 0 else -1
    result = 0

    for i, bit in enumerate(bit_array[1:4]):
        result += bit * 2.0**(2 - i)

    for i, bit in enumerate(bit_array[4:]):
        result += bit * 2.0**(-1 - i)

    return sign * result


def rastrigin(bit_array, n=40):
    assert len(bit_array) == 8 * n

    X = [decode_rastrigin(bit_array[8 * i:8 * (i + 1)]) for i in range(n)]
    result = 10 * len(X) + sum([x**2 - 10 * math.cos(2 * math.pi * x) for x in X])

    return -math.fabs(result)


def schwefel(bit_array, n=40):
    assert len(bit_array) == 32 * n

    X = [decode_ieee754(bit_array[32 * i:32 * (i + 1)]) for i in range(n)]

    for x in X:
        if x < -512 or x > 512:
            return -10**32

    result = -sum([x * math.sin(math.sqrt(math.fabs(x))) for x in X])

    return -math.fabs(result)
