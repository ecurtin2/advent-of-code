from utils import parse_run
from string import ascii_lowercase, ascii_uppercase
from extra_itertools import nwise


PRIORITY = {l: i for i, l in enumerate(ascii_lowercase + ascii_uppercase, 1)}

def bisect(l: str) -> tuple[str, str]:
    N = len(l) // 2
    return l[:N], l[N:]


def p1(inputs: list[str]) -> int:
    items = [
        (set.intersection(*map(set, bisect(line)))).pop()
        for line in inputs
    ]
    return sum(PRIORITY[i] for i in items)


def p2(inputs: list[str]) -> int:
    groups = nwise(3, map(set, inputs), step=3)
    stickers = [(s1 & s2 & s3).pop() for s1, s2, s3 in groups]
    return sum(PRIORITY[s] for s in stickers)


def test_p1():
    input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    assert parse_run(p1, input) == 157


def test_p2():
    input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    assert parse_run(p2, input) == 70
