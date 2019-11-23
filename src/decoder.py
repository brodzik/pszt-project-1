def decode_binary(bit_array):
    assert len(bit_array) > 0

    result = 0

    for i, bit in enumerate(bit_array):
        result += bit * 2**(len(bit_array) - 1 - i)

    return result


def decode_u2(bit_array):
    assert len(bit_array) > 0

    result = bit_array[0] * -2**(len(bit_array) - 1)

    for i, bit in enumerate(bit_array[1:]):
        result += bit * 2**(len(bit_array) - 2 - i)

    return result


def decode_ieee754(bit_array):
    assert len(bit_array) == 32

    sign = 1 if bit_array[0] == 0 else -1

    exponent = -127
    for i, bit in enumerate(bit_array[1:9]):
        exponent += bit * 2.0**(7 - i)

    mantissa = 0
    for i, bit in enumerate(bit_array[9:]):
        mantissa += bit * 2.0**(-1 - i)

    return sign * 2.0**exponent * (1 + mantissa)
