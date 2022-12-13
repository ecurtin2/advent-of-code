import json
from utils import parse_run
from extra_itertools import nwise
from math import prod
from functools import cmp_to_key


def sign(x: int):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def cmp(l: list | int, r: list | int) -> int:
    """1 = right   -1 = wrong   0 = indeterminate"""
    if isinstance(l, int) and isinstance(r, int):
        return sign(r - l)
    if isinstance(r, int):
        return cmp(l, [r])
    if isinstance(l, int):
        return cmp([l], r)

    for i in range(max(len(l), len(r))):
        if i == len(r):
            return -1
        if i == len(l):
            return 1
        if val := cmp(l[i], r[i]):
            return val
    return 0


def p1(inputs: list[str]) -> int:
    pairs = list(nwise(2, [json.loads(l) for l in inputs if l], step=2))
    got = {i: cmp(l, r) for i, (l, r) in enumerate(pairs, 1)}
    return sum([i for i, v in got.items() if v >= 0])


def p2(inputs: list[str]) -> int:
    keys = [[[2]], [[6]]]
    data = [json.loads(l) for l in inputs if l] + keys
    sort = sorted(data, key=cmp_to_key(cmp), reverse=True)
    return prod(sort.index(k) + 1 for k in keys)


def test_p1():
    input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    assert parse_run(p1, input) == 13


def test_p2():
    input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    assert parse_run(p2, input) == 140
