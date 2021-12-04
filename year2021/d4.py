from dataclasses import dataclass
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def iter_columns(x: list[list]):
    ncols = len(x[0])
    for i in range(ncols):
        yield [row[i] for row in x]


@dataclass
class Board:
    values: list[list[int]]

    def wins(self, calls: list[int]) -> bool:
        calls_set = set(calls)
        row_won = any(set(row).issubset(calls_set) for row in self.values)
        col_won = any(set(col).issubset(calls_set) for col in iter_columns(self.values))
        return row_won or col_won

    def score(self, calls: list[int]) -> int:
        vals = set(val for row in self.values for val in row)
        uncalled = vals - set(calls)
        return sum(uncalled) * calls[-1]

    def __str__(self):
        return "\n".join(" ".join(f"{val:4}" for val in row) for row in self.values)


def score_of_nth_place(inputs: str, n: int) -> int:
    header, *rest = inputs.splitlines()
    calls = [int(i) for i in header.split(",")]
    parsed_lines = [[int(c) for c in row.split()] for row in rest if row.strip()]
    boards = [Board(list(chunk)) for chunk in grouper(parsed_lines, 5)]
    winning_boards = []

    if n > 0:
        idx = n - 1
    elif n < 0:
        idx = len(boards) + n
    else:
        raise ValueError(f"{n=} not supported")

    for i in range(len(calls)):
        winning_boards.extend(b for b in boards if b.wins(calls[:i]))
        boards = [b for b in boards if b not in winning_boards]
        if len(winning_boards) >= idx + 1:
            return winning_boards[idx].score(calls[:i])


def p1(inputs: str) -> int:
    return score_of_nth_place(inputs, 1)


def p2(inputs: str) -> int:
    return score_of_nth_place(inputs, -1)


def test_p1():
    inputs = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
    assert p1(inputs) == 4512


def test_p1():
    inputs = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
    assert p2(inputs) == 1924