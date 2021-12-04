from itertools import count
from typing import List

from utils import diff


def part1(inp: List[str]) -> int:
    earliest = int(inp[0])
    buses = [int(i) for i in inp[1].split(",") if i != "x"]
    bus_t, bus_id = min(((earliest // b + 1) * b, b) for b in buses)
    return bus_id * (bus_t - earliest)


def part2(inp: List[str]) -> int:
    raise NotImplementedError


def test_part1():
    inp = """939
7,13,x,x,59,x,31,19"""
    assert part1(inp.splitlines()) == 295


def test_part2():
    inp = """939
    7,13,x,x,59,x,31,19"""
    assert part2(inp.splitlines()) == 1068781
