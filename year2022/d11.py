from dataclasses import dataclass
from utils import parse_run
from math import lcm
from typing import Union


ModIntAble = Union["ModularInt", int]


class ModularInt:
    def __init__(self, value: int, mod: int):
        self.value = value % mod
        self.mod = mod

    def __add__(self, other: ModIntAble) -> "ModularInt":
        if isinstance(other, int):
            return ModularInt(self.value + other, self.mod)
        elif isinstance(other, ModularInt):
            if self.mod == other.mod:
                return ModularInt(self.value + other.value, self.mod)
            else:
                raise NotImplemented(f"I didn't find this or need it")
        else:
            raise TypeError(f"Unsupported: {other} (type={type(other)})")

    def __mul__(self, other: ModIntAble) -> "ModularInt":
        if isinstance(other, int):
            return ModularInt(self.value * other, self.mod)
        elif isinstance(other, ModularInt):
            return ModularInt(self.value * other.value, self.mod)

    def __floordiv__(self, other):
        # Is this even right idk but it works for this problem?
        return ModularInt(self.value // other, self.mod)

    def __mod__(self, value):
        return self.value % value

    def __str__(self):
        return f"{self.value} mod {self.mod}"


class Operation:
    def __init__(self, s: str):
        self.s = s.split("=")[1]
        match self.s.split():
            case ["old", "*", "old"]:
                self.func = lambda x: x * x
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
    items: list[ModularInt]
    operation: Operation
    test_divisible: int
    if_true: int
    if_false: int
    num_inspected: int = 0

    def __post_init__(self):
        MONKEYS[self.id] = self

    @staticmethod
    def from_list(chunk: list[str], modulo: int) -> "Monkey":
        items = [ModularInt(int(v), modulo) for v in chunk[1].split(":")[1].split(",")]
        return Monkey(
            id=int(chunk[0].split()[1][:-1]),
            items=items,
            operation=Operation(chunk[2]),
            test_divisible=int(chunk[3].split()[-1]),
            if_true=int(chunk[4].split()[-1]),
            if_false=int(chunk[5].split()[-1]),
        )

    def throw(self, item: ModIntAble, other: int):
        MONKEYS[other].items.append(item)

    def inspect(self, reduce_worry: bool):
        for item in self.items:
            self.num_inspected += 1
            worry = self.operation(item)
            if reduce_worry:
                worry //= 3
            if (worry % self.test_divisible) == 0:
                self.throw(worry, self.if_true)
            else:
                self.throw(worry, self.if_false)
        self.items = []


def solve(inputs: list[str], rounds: int, reduce_worry: bool) -> int:
    divisibles = [int(l.split()[-1]) for l in inputs if l and "divisible" in l]
    mod = lcm(*divisibles)
    monkeys = [
        Monkey.from_list(inputs[i : i + 6], mod) for i in range(0, len(inputs), 7)
    ]
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
