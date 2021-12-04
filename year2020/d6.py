from collections import Counter
from itertools import chain
from typing import List

from utils import split


def part1(inp: List[str]) -> int:
    return sum(
        len(set("".join(chunk))) for chunk in split(inp, lambda s: s.strip() == "")
    )


def part2(inp: List[str]) -> int:
    total = 0
    for chunk in split(inp, lambda s: s.strip() == ""):
        counter = Counter(chain.from_iterable(chunk))
        for k, v in counter.items():
            if v == len(chunk):
                total += 1
    return total


def test_part1():
    inp = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    assert part1(inp.splitlines()) == 11


def test_part2():
    inp = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    assert part2(inp.splitlines()) == 6
