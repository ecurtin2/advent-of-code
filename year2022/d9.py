
from utils import parse_run
from itertools import chain
from math import atan2, isclose, cos, sin, ceil, floor, sqrt

def round_away(x: float) -> int: 
    """If x is nearly round, round it, otherwise round away from 0"""
    if isclose(x, float(round(x)), abs_tol=0.01):
        rounded = round(x)
    else:
        rounded = ceil(x) if x > 0.0 else floor(x)
    return int(rounded)


def advance(tail, head):
    dx = (head[0] - tail[0], head[1] - tail[1])
    # Do nothing if neighboring (includes diag where magnitude = sqrt(2) = 1.1414)
    if sqrt(dx[0]**2 + dx[1]**2) > 1.42:
        theta = atan2(dx[1], dx[0])
        dt = cos(theta), sin(theta)
        dt = round_away(dt[0]), round_away(dt[1])
        return tail[0] + dt[0], tail[1] + dt[1]
    else:
        return tail


def solve(inputs: list[str], rope_length: int) -> int:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(rope_length)]
    parsed = (((s := l.split())[0], int(s[1])) for l in inputs)
    directions = chain.from_iterable((d for _ in range(m)) for d, m in parsed)
    visited = set()
    dir2coord = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0)
    }
    
    for direction in directions:
        dh = dir2coord[direction]
        rope[0] = rope[0][0] + dh[0], rope[0][1] + dh[1]
        for i in range(1, len(rope)):
            rope[i] = advance(rope[i], rope[i - 1])
        visited.add(rope[-1])
    return len(visited)


def p1(inputs: list[str]) -> int:
    return solve(inputs, 2)


def p2(inputs: list[str]) -> int:
    return solve(inputs, 10)


def test_p1():
    input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    assert parse_run(p1, input) == 13


def test_p2():
    input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    assert parse_run(p2, input) == 1


def test_p2_large():
    input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    assert parse_run(p2, input) == 36

