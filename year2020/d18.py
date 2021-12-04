from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class Token(Enum):
    add = "+"
    mul = "*"
    lparen = "("
    rparen = ")"

    def __repr__(self):
        return f"{self.value}"


TOKENS = set(i.value for i in Token)


class Op(Enum):
    LIT = 0
    MUL = 1
    ADD = 2


@dataclass
class Node:
    op: Op
    left: "Node" = None
    right: "Node" = None
    value: int = None

    def __post_init__(self):
        if self.op == Op.LIT:
            if self.value is None:
                raise ValueError("Literal op with no value!")
            if (self.left is not None) or (self.right is not None):
                raise ValueError(
                    f"Literal node with children! {self=}  {self.right=} {self.left=}"
                )

    def eval(self):
        if self.op == Op.LIT:
            return self.value
        elif self.op == Op.MUL:
            return self.left.eval() * self.right.eval()
        elif self.op == Op.ADD:
            return self.left.eval() + self.right.eval()


def part1(inp: str) -> int:
    parsed: List[Union[Token, int]] = []
    idx = 0
    while idx < len(inp):
        if inp[idx] in TOKENS:
            parsed.append(Token(inp[idx]))
            idx += 1
        elif inp[idx].isdigit():
            end = idx + 1
            while inp[idx : end + 1].isdigit():
                end += 1
            parsed.append(int(inp[idx:end]))
            idx = end
        else:
            idx += 1

    expr = Node(Op.MUL, Node(Op.LIT, value=3), Node(Op.LIT, value=5))
    print(expr)
    print(expr.eval())
    raise NotImplementedError


def part2(inp: List[str]) -> int:
    raise NotImplementedError


def test_part1():
    inp = """2 * 3 + (4 * 5)"""
    assert part1(inp) == 26


def test_part2():
    inp = """"""
    assert part2(inp.splitlines()) == 1
