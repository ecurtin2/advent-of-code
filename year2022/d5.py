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


def get(l: list, i: int, default=None):
    try:
        return l[i]
    except IndexError:
        return default


def do(i: Instruction, data: Data, cratemover_version=9000):
    moved = [data[i.from_].pop() for _ in range(i.count)]
    if cratemover_version == 9001:
        moved = reversed(moved)
    data[i.to].extend(moved)


def parse(inputs: list[str]) -> tuple[Data, list[Instruction]]:
    data, instructions = list(split(inputs, is_none))
    cols = data.pop().split()
    indices = range(1, (len(cols) - 1) * 4 + 2, 4)
    col_idxs = dict(zip(cols, indices))
    column_data = {c: [] for c in col_idxs}
    for l in data:
        for col, i in col_idxs.items():
            val = get(l, i, "").strip()
            if val:
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
        do(instruction, data, cratemover_version=9001)
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
