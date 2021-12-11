import pytest
import numpy as np
from extra_itertools import neighbors
from typing import Generator


def solve(octopi) -> Generator[np.ndarray, None, None]:
    i_max, j_max = octopi.shape
    flash_at = 9
    while True:
        octopi += 1
        flashed = set()
        should_flash = {tuple(x) for x in np.transpose((octopi > flash_at).nonzero())}
        while should_flash:
            flash = should_flash.pop()
            flashed.add(flash)
            for i, j in neighbors(*flash, i_max=i_max, j_max=j_max, diagonals=True):
                octopi[i, j] += 1
                if octopi[i, j] > flash_at and (i, j) not in flashed:
                    should_flash.add((i, j))

        for i, j in flashed:
            octopi[i, j] = 0
        yield octopi


def p1(inputs: str) -> int:
    octopi = np.array([[int(i) for i in row] for row in inputs.splitlines()])
    flashes_gen = solve(octopi)
    return sum((next(flashes_gen) == 0).sum() for _ in range(100))


def p2(inputs: str) -> int:
    octopi = np.array([[int(i) for i in row] for row in inputs.splitlines()])
    flashes_gen = solve(octopi)
    for i, octopi in enumerate(flashes_gen):
        if np.all(octopi == 0):
            return i + 1


@pytest.fixture()
def example():
    return """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_p1(example):
    assert p1(example) == 1656


def test_p2(example):
    assert p2(example) == 195
