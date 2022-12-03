from extra_itertools import split
from utils import parse_run
from heapq import nlargest


def p1(data: list[int | None]):
    return max(sum(c) for c in split(data, on=lambda x: x is None))


def p2(data: list[int | None]):
    return sum(nlargest(3, (sum(c) for c in split(data, on=lambda x: x is None))))


def test_p1():
    input = """1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000"""

    assert parse_run(p1, input) == 24000


def test_p2():
    input = """1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000"""

    assert parse_run(p2, input) == 45000
