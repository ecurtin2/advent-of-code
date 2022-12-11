from dataclasses import dataclass
from utils import parse_run
from math import lcm
from functools import lru_cache


class Operation:
    def __init__(self, s: str):
        self.s = s.split("=")[1]
        match self.s.split():
            case ["old", "*", "old"]:
                self.func = lambda x: x**2
            case ["old", "*", x]:
                self.func = lambda old: old * int(x)
            case ["old", "+", x]:
                self.func = lambda old: old + int(x)
            case _:
                raise ValueError(f"Unkown Operation: {s}")

    def __call__(self, x):
        return self.func(x)

    def __repr__(self):
        return f"({self.s} )"


MONKEYS: dict[int, "Monkey"] = dict()


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Operation
    test_divisible: int
    if_true: int
    if_false: int
    num_inspected: int = 0

    def __post_init__(self):
        MONKEYS[self.id] = self

    @staticmethod
    def from_list(chunk: list[str]) -> "Monkey":
        return Monkey(
            id=int(chunk[0].split()[1][:-1]),
            items=list(map(int, chunk[1].split(":")[1].split(","))),
            operation=Operation(chunk[2]),
            test_divisible=int(chunk[3].split()[-1]),
            if_true=int(chunk[4].split()[-1]),
            if_false=int(chunk[5].split()[-1]),
        )

    def throw(self, item: int, other: int):
        MONKEYS[other].items.append(item)

    @lru_cache
    @staticmethod
    def divisor_lcm():
        return lcm(*[m.test_divisible for m in MONKEYS.values()])

    def inspect(self, reduce_worry: bool):
        for item in self.items:
            self.num_inspected += 1
            worry = self.operation(item)
            if reduce_worry:
                worry //= 3
            else:
                # Use LCM of divisers to preserve modulus upon add+mul
                worry %= Monkey.divisor_lcm()

            if (worry % self.test_divisible) == 0:
                self.throw(worry, self.if_true)
            else:
                self.throw(worry, self.if_false)
        self.items = []


def solve(inputs: list[str], rounds: int, reduce_worry: bool) -> int:
    monkeys = [Monkey.from_list(inputs[i : i + 6]) for i in range(0, len(inputs), 7)]
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.inspect(reduce_worry=reduce_worry)
    sorted_m = sorted(monkeys, key=lambda m: m.num_inspected, reverse=True)
    return sorted_m[0].num_inspected * sorted_m[1].num_inspected


def p1(inputs: list[str]) -> int:
    return solve(inputs, rounds=20, reduce_worry=True)


def p2(inputs: list[str]) -> int:
    return solve(inputs, rounds=10_000, reduce_worry=False)


def test_p1():
    input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
    assert parse_run(p1, input) == 10605


def test_p2():
    input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
    assert parse_run(p2, input) == 2713310158
