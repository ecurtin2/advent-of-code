import numpy as np
from operator import ge, lt


def bits_to_int(bits: list[int]) -> int:
    return int("".join(map(str, bits)), 2)


def p1(data: list[str]) -> int:
    ary = [[int(i) for i in row] for row in data]
    ary_t = [list(i) for i in zip(*ary)]
    gamma_bits = [int(sum(row) > (len(row) / 2)) for row in ary_t]
    epsilon_bits = [0 if x else 1 for x in gamma_bits]
    gamma = bits_to_int(gamma_bits)
    epsilon = bits_to_int(epsilon_bits)
    return gamma * epsilon


def n_until_false(l: list[bool]) -> int:
    for i, item in enumerate(l):
        if not item:
            break
    return i


def p2(data: list[str]) -> int:
    ary = np.array([[int(i) for i in row] for row in data])

    ops = {"o2": ge, "co2": lt}
    result = dict()

    old_ary = ary.copy()
    for k, compare in ops.items():
        ary = old_ary
        mask = np.ones_like(ary[:, 0]).astype(bool)
        for i in range(len(ary[0])):
            bit = int(compare(ary[mask, i].sum(), len(ary[mask, i]) / 2))
            mask &= ary[:, i] == bit
            if mask.sum() == 1:
                idx = np.where(mask)[0][0]
                result[k] = bits_to_int(ary[idx])

    return result["o2"] * result["co2"]


def test_p1():
    inputs = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    assert p1(inputs.splitlines()) == 198


def test_p2():
    inputs = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    assert p2(inputs.splitlines()) == 230
