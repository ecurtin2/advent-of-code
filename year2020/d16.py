from dataclasses import dataclass
from typing import List, Tuple
from utils import split
from math import prod


@dataclass
class Rule:
    name: str
    ranges: List[Tuple[int, int]]

    @staticmethod
    def from_str(s: str) -> "Rule":
        n, rest = s.split(":")
        ranges = [tuple(map(int, r.split("-"))) for r in rest.split(" or ")]
        return Rule(n, ranges)

    def is_valid(self, x: int) -> bool:
        return any(l <= x <= r for l, r in self.ranges)


def no_valid(x: int, rules: List[Rule]) -> bool:
    return not any(r.is_valid(x) for r in rules)


def part1(inp: List[str]) -> int:
    rules, mine, nearby = split(inp, on=lambda s: s.strip() == "")
    rules = [Rule.from_str(r) for r in rules]
    nearby_tickets = [[int(i) for i in line.split(",")] for line in nearby[1:]]
    return sum(val for t in nearby_tickets for val in t if no_valid(val, rules))


def part2(inp: List[str]) -> int:
    rules, mine, nearby = split(inp, on=lambda s: s.strip() == "")
    rules = [Rule.from_str(r) for r in rules]
    my_ticket = [int(i) for i in mine[1].split(",")]
    nearby_tickets = [[int(i) for i in line.split(",")] for line in nearby[1:]]
    good_tickets = [t for t in nearby_tickets if all(not no_valid(v, rules) for v in t)]

    n2i = {r.name: set(range(len(good_tickets[0]))) for r in rules}

    for t in good_tickets:
        for rule in rules:
            for i, val in enumerate(t):
                if not rule.is_valid(val):
                    n2i[rule.name] -= {i}

    final_n2i = {}
    updates = {k: next(iter(s)) for k, s in n2i.items() if len(s) == 1}
    while updates:
        for k in n2i:
            n2i[k] -= set(updates.values())
        final_n2i.update(updates)
        updates = {k: next(iter(s)) for k, s in n2i.items() if len(s) == 1}

    indices = [i for n, i in final_n2i.items() if n.startswith("departure")]
    return prod(my_ticket[i] for i in indices)


def test_part1():
    inp = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    assert part1(inp.splitlines()) == 71


def test_part2():
    inp = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    assert part2(inp.splitlines()) == 1
