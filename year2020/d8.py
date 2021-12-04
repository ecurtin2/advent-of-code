from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


class OpCode(Enum):
    acc = "acc"
    jmp = "jmp"
    nop = "nop"


@dataclass
class Emu:
    program: List[Tuple[OpCode, int]]
    acc: int = 0
    pointer: int = 0
    history: List[int] = field(default_factory=list)

    @staticmethod
    def from_iterable(iterable):
        return Emu(
            [(OpCode[line.split()[0]], int(line.split()[1])) for line in iterable]
        )

    def with_sub(self, idx: int, code: OpCode, value: int) -> "Emu":
        new_program = self.program.copy()
        new_program[idx] = code, value
        return Emu(new_program)

    def execute(self) -> Tuple[int, bool]:
        while True:
            if self.pointer in self.history:
                return self.acc, False
            if self.pointer >= len(self.program):
                return self.acc, True
            self.history.append(self.pointer)
            code, val = self.program[self.pointer]
            self._execute_code(code, val)

    def _execute_code(self, code: OpCode, value: int):
        if code == OpCode.acc:
            self.acc += value
            self.pointer += 1
        elif code == OpCode.jmp:
            self.pointer += value
        elif code == OpCode.nop:
            self.pointer += 1


def part1(inp: List[str]) -> int:
    emulator = Emu.from_iterable(inp)
    return emulator.execute()[0]


def part2(inp: List[str]) -> int:
    base_emu = Emu.from_iterable(inp)
    for i, (code, val) in enumerate(base_emu.program):
        if code == OpCode.nop:
            emu = base_emu.with_sub(i, OpCode.jmp, val)
        elif code == OpCode.jmp:
            emu = base_emu.with_sub(i, OpCode.nop, val)
        else:
            continue
        val, terminated = emu.execute()
        if terminated:
            return val


def test_part1():
    inp = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    assert part1(inp.splitlines()) == 5


def test_part2():
    inp = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    assert part2(inp.splitlines()) == 8
