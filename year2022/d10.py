from utils import parse_run
from bisect import bisect_right


class Screen:
    def __init__(self, nrows: int = 6, ncols: int = 40):
        self.data = [[" " for _ in range(ncols)] for _ in range(nrows)]
        self.nrows = nrows
        self.ncols = ncols

    def __setitem__(self, idx, value):
        row_idx, col_idx = divmod(idx - 1, self.ncols)
        self.data[row_idx][col_idx] = value

    def get_x(self, cycle):
        return (cycle - 1) % self.ncols

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)


class CPU:
    def __init__(self, inputs: list[str]):
        self.cycles = [1]
        self.vals = [1]
        noop_cycles = 0
        for line in inputs:
            match line.split():
                case ["noop"]:
                    noop_cycles += 1
                case ["addx", x]:
                    self.cycles.append(self.cycles[-1] + 2 + noop_cycles)
                    self.vals.append(self.vals[-1] + int(x))
                    noop_cycles = 0

    def value(self, cycle: int) -> int:
        return self.vals[bisect_right(self.cycles, cycle) - 1]

    def strength(self, cycle: int) -> int:
        return cycle * self.value(cycle)


def p1(inputs: list[str]) -> int:
    cpu = CPU(inputs)
    return sum(cpu.strength(i) for i in range(20, 221, 40))


def p2(inputs: list[str]) -> str:
    cpu = CPU(inputs)
    screen = Screen()
    for cycle in range(1, 241):
        if abs(cpu.value(cycle) - screen.get_x(cycle)) <= 1:
            screen[cycle] = "█"
    return str(screen)


def test_p1():
    from pathlib import Path

    input = (Path(__file__).parent / "data") / "d10_test.txt"
    assert parse_run(p1, input.read_text()) == 13140


def test_p2():
    from pathlib import Path

    input = (Path(__file__).parent / "data") / "d10_test.txt"
    result = parse_run(p2, input.read_text())
    print("")
    print(result)
