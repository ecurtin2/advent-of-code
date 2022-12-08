
from itertools import chain
from math import prod

from extra_itertools import take_until, last
from utils import parse_run


def p1(inputs: list[list[int]]) -> int:
    visible = [[0 for _ in inputs[0]] for _ in inputs]
    M = len(visible)
    N = len(visible[0])
    
    idx_dirs = (
        [[(i, j) for j in range(N)] for i in range(M)] # Left
        + [[(i, j) for j in range(N - 1, -1, -1)] for i in range(M)]     # Right
        + [[(i, j) for i in range(M)] for j in range(N)]    # Top
        + [[(i, j) for i in range(M - 1, -1, -1)] for j in range(N)]    # Bottom
    )

    for idxs in idx_dirs:
        curr = -1
        for i, j in idxs:
            if (tree := inputs[i][j]) > curr:
                visible[i][j] = 1
                curr = tree

    return sum(chain.from_iterable(visible))


def scenic_score(trees, i0, j0):
    n_i, n_j = len(trees), len(trees[0])
    ranges = [
        zip(range(i0, -1, -1), [j0] * n_j),       # up
        zip([i0] * n_i, range(j0, -1, -1)),       # left
        zip(range(i0, len(trees)), [j0] * n_j),   # down
        zip([i0] * n_i, range(j0, len(trees[0]))) # right
    ]
    visible_ranges = (take_until(lambda x: (x != (i0, j0)) and (trees[x[0]][x[1]] >= trees[i0][j0]), r) for r in ranges)
    return prod(last(i for i, _ in enumerate(r)) for r in visible_ranges)


def p2(inputs: list[list[int]]) -> int:
    scores = [[scenic_score(inputs, i, j) for j in range(len(inputs))] for i in range(len(inputs[0]))]
    return max(chain.from_iterable(scores))


def test_p1():
    input = """30373
25512
65332
33549
35390"""
    assert parse_run(p1, input) == 21


def test_p2():
    input = """30373
25512
65332
33549
35390"""
    assert parse_run(p2, input) == 8

