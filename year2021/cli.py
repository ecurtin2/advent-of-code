import cattr
from sys import argv
from importlib import import_module
from inspect import signature
from pathlib import Path
from timeit import default_timer as timer


def parse_input(to, s: str):
    if to == str:
        return s
    elif to.__origin__ == list:
        inner_t = to.__args__[0]
        lines = s.splitlines()
        if hasattr(inner_t, "__args__"):
            lines = [l.split() for l in lines]
        return [cattr.structure(l, inner_t) for l in lines]
    raise ValueError(f"Can't parse to type {to}")


def run(day: int, part: int):
    mod = import_module(f"d{day}")
    func = getattr(mod, f"p{part}")
    sig = signature(func)

    start = timer()
    if sig.parameters:
        input_type = list(sig.parameters.values())[0].annotation
        input_file = Path(f"data/d{day}p{part}.txt")

        # Fallback on part 1 since often reused
        if not input_file.is_file():
            input_file = Path(f"data/d{day}p1.txt")

        inputs = parse_input(input_type, input_file.read_text())
        result = func(inputs)
    else:
        result = func()

    end = timer()
    return result, end - start


day, part = argv[1], argv[2]
if day == "x":
    days = sorted(int(p.stem[1:]) for p in Path(__file__).parent.glob("d*.py"))
else:
    days = [int(day)]
if part == "x":
    parts = [1, 2]
else:
    parts = [int(part)]

print(" Day | Part | Duration | Answer ")
print("-----|------|----------|--------")

durations = []
for day in days:
    for part in parts:
        print(f" {day:2}  |  {part}   |", end=" ")
        result, duration = run(day, part)
        durations.append(duration)
        print(f" {duration:6.4f}", end="")
        if "hide" in "".join(argv):
            print(f"  | <redacted>")
        else:
            print(f"  | {result}")

print(f"\n Total duration for all parts: {sum(durations):6.4f}")
