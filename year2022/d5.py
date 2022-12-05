
from utils import parse_run, is_none
from extra_itertools import split

def get(l: list, i: int, default=None):
    try:
        return l[i]
    except IndexError:
        return default


def pop_move(l: list, to: list, n: int):
    for _ in range(n):
        to.append(l.pop())


def p1(inputs: list[str]) -> int:
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

    
    for row in instructions:
        count, from_, to_ = row.replace("move", "").replace("from", "").replace("to", "").split()
        pop_move(column_data[from_], column_data[to_], int(count))
    
    return "".join(c[-1] for c in column_data.values())


def p2(inputs: list[str]) -> int:
    return 0


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
    input = """"""
    assert parse_run(p2, input) == 1

