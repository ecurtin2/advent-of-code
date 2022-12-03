from utils import parse_run
from string import ascii_lowercase, ascii_uppercase

PRIORITY = {l: i for i, l in enumerate(ascii_lowercase + ascii_uppercase, 1)}


def p1(inputs: list[str]) -> int:
    items = [
        set(line[:len(line) // 2]).intersection(set(line[len(line)//2:])).pop()
        for line in inputs
    ]
    return sum(PRIORITY[i] for i in items)


def p2(inputs: list[str]) -> int:
    return 0


def test_p1():
    input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    assert parse_run(p1, input) == 157


def test_p2():
    input = """"""
    assert parse_run(p2, input) == 1
