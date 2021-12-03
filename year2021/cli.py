import cattr
from sys import argv
from importlib import import_module
from inspect import signature
from pathlib import Path


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


day, part = argv[1], argv[2]
print(f"Running Day {day} part {part}")

mod = import_module(f"d{day}")
func = getattr(mod, f"p{part}")
sig = signature(func)
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

print(result)
