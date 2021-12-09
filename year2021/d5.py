import pytest
import numpy as np


def draw_line(ary, p1, p2):
    if p1[0] == p2[0]:  # special case for vertical
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1]) + 1
        ary[y_min:y_max, p1[0]] += 1
        return

    if p2[0] < p1[0]:
        p1, p2 = p2, p1
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    xs = np.arange(p1[0], p2[0] + 1)
    ys = (p1[1] + slope * np.arange(xs.shape[0])).astype(np.int32)
    ary[ys, xs] += 1


def solve(inputs, hv_only: bool) -> int:
    lines = [
        [[int(x) for x in s.split(",")] for s in line.split("->")]
        for line in inputs.splitlines()
    ]
    if hv_only:
        lines = np.array([l for l in lines if l[0][0] == l[1][0] or l[0][1] == l[1][1]])
    else:
        lines = np.array(lines)

    max_x = np.amax(lines[:, 0, :])
    max_y = np.amax(lines[:, 1, :])
    space = np.zeros((max_x + 1, max_y + 1), dtype=np.int32)
    for p1, p2 in lines:
        draw_line(space, p1, p2)
    return np.count_nonzero(space >= 2)


def p1(inputs: str) -> int:
    return solve(inputs, hv_only=True)


def p2(inputs: str) -> int:
    return solve(inputs, hv_only=False)


@pytest.fixture()
def example():
    return """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def test_p1(example):
    assert p1(example) == 5


def test_p2(example):
    assert p2(example) == 12
