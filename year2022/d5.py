from dataclasses import dataclass
from utils import parse_run, is_none
from extra_itertools import split

Data = dict[str, list[str]]


@dataclass
class Instruction:
    count: int
    from_: str
    to: str

    @staticmethod
    def from_str(s: str):
        c, f, t = s.replace("move", "").replace("from", "").replace("to", "").split()
        return Instruction(int(c), f, t)


def do(i: Instruction, data: Data, multiple: bool = False):
    moved = [data[i.from_].pop() for _ in range(i.count)]
    if multiple:
        moved = reversed(moved)
    data[i.to].extend(moved)


def parse(inputs: list[str]) -> tuple[Data, list[Instruction]]:
    data, instructions = list(split(inputs, is_none))
    cols = data.pop()
    col_idxs = {c: cols.index(c) for c in cols.split()}
    column_data = {c: [] for c in col_idxs}

    for l in data:
        for col, i in col_idxs.items():
            if i <= len(l) and (val := l[i].strip()):
                column_data[col].append(val)

    for col in column_data:
        column_data[col].reverse()

    instr = [Instruction.from_str(s) for s in instructions]
    return column_data, instr


def p1(inputs: list[str]) -> str:
    data, instructions = parse(inputs)
    for instruction in instructions:
        do(instruction, data)
    return "".join(c[-1] for c in data.values())


def p2(inputs: list[str]) -> str:
    data, instructions = parse(inputs)
    for instruction in instructions:
        do(instruction, data, multiple=True)
    return "".join(c[-1] for c in data.values())


def test_p1():
    input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    assert parse_run(p1, input) == "CMZ"


def test_p2():
    input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    assert parse_run(p2, input) == "MCD"
