from utils import parse_run
from data_structures import Grid
from extra_itertools import nwise


def solve(inputs, with_floor: bool):
    g = Grid()
    for line in inputs:
        paths = nwise(2, ([int(v) for v in x.split(",")] for x in line.split(" -> ")))
        for s, e in paths:
            g[s[0] : e[0], s[1] : e[1]] = "#"

    x, y = source = 500, 0
    g[source[0], source[1]] = "+"
    ymax = g.span[1][1] or 0
    if with_floor:
        bottom = (ymax or 0) + 2
        dy = bottom - source[1]
        g[source[0] - dy : source[0] + dy, bottom] = "-"
    else:
        bottom = ymax

    while y <= bottom:
        if (x, y + 1) not in g:
            y += 1
        elif (x - 1, y + 1) not in g:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in g:
            x += 1
            y += 1
        else:
            g[x, y] = "o"
            if (x, y) == source:
                break
            x, y = source
    return g.value_counts()["o"]


def p1(inputs: list[str]) -> int:
    return solve(inputs, with_floor=False)


def p2(inputs: list[str]) -> int:
    return solve(inputs, with_floor=True)


def test_p1():
    input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
    assert parse_run(p1, input) == 24


def test_p2():
    input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
    assert parse_run(p2, input) == 93
