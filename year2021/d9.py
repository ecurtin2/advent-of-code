import pytest
import numpy as np
from math import prod
from functools import lru_cache

from extra_itertools import neighbors


def local_mins(ary):
    return [
        (i, j)
        for i in range(ary.shape[0])
        for j in range(ary.shape[1])
        if all(
            ary[n[0], n[1]] > ary[i, j]
            for n in neighbors(i, j, ary.shape[0], ary.shape[1])
        )
    ]


def crawl_uphill(ary, start, until=9):
    @lru_cache()
    def f(start):
        uphill_neighbors = filter(
            lambda n: ary[start[0], start[1]] < ary[n[0], n[1]] < until,
            neighbors(*start, ary.shape[0], ary.shape[1]),
        )
        yield start
        for n in uphill_neighbors:
            yield from f(n)

    return f(start)


def p1(inputs: str) -> int:
    ary = np.array([[int(i) for i in line] for line in inputs.splitlines()])
    return sum(ary[i, j] + 1 for i, j in local_mins(ary))


def p2(inputs: str) -> int:
    ary = np.array([[int(i) for i in line] for line in inputs.splitlines()])
    mins = local_mins(ary)
    basins = {
        basin: set(crawl_uphill(ary, start=min)) for basin, min in enumerate(mins)
    }
    return prod(sorted(map(len, basins.values()), reverse=True)[:3])


@pytest.fixture()
def example():
    return """2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_p1(example):
    assert p1(example) == 15


def test_p2(example):
    assert p2(example) == 1134
