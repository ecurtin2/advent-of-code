from utils import parse_run


def overlaps(p1, p2, total=True):
    r1 = set(range(p1[0], p1[1] + 1))
    r2 = set(range(p2[0], p2[1] + 1))
    if total:
        return r1.issubset(r2) or r2.issubset(r1)
    else:
        return not r1.isdisjoint(r2)


def parse(inputs: list[str]) -> list[list[tuple[int]]]:
    return [[tuple(map(int, p.split("-"))) for p in l.split(",")] for l in inputs]


def p1(inputs: list[str]) -> int:
    return sum(overlaps(*p, total=True) for p in parse(inputs))


def p2(inputs: list[str]) -> int:
    return sum(overlaps(*p, total=False) for p in parse(inputs))


def test_p1():
    input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    assert parse_run(p1, input) == 2


def test_p2():
    input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    assert parse_run(p2, input) == 4
