from sys import argv
from importlib import import_module

from pathlib import Path
from timeit import default_timer as timer


from utils import parse_run


def run(year: int, day: int, part: int):
    mod = import_module(f"year{year}.d{day}")
    func = getattr(mod, f"p{part}")

    input_file = Path(f"year{year}/data/d{day}p{part}.txt")

    start = timer()

    # Fallback on part 1 since often reused
    if not input_file.is_file():
        input_file = Path(f"year{year}/data/d{day}p1.txt")

    input =  input_file.read_text()
    result = parse_run(func, input)

    end = timer()
    return result, end - start

def main(year: int, day: int = None, part: int = None):
    if day is None:
        days = sorted(int(p.stem[1:]) for p in Path(__file__).parent.glob("d*.py"))
    else:
        days = [int(day)]
    if part is None:
        parts = [1, 2]
    else:
        parts = [int(part)]

    print(" Day | Part | Duration | Answer ")
    print("-----|------|----------|--------")

    durations = []
    for day in days:
        for part in parts:
            print(f" {day:2}  |  {part}   |", end=" ")
            result, duration = run(year, day, part)
            durations.append(duration)
            print(f" {duration:6.4f}", end="")
            if "hide" in "".join(argv):
                print(f"  | <redacted>")
            else:
                print(f"  | {result}")

    print(f"\n Total duration for all parts: {sum(durations):6.4f}")

if __name__ == "__main__":
    match argv[1:4]:
        case []:
            main(2022, 2, 2)
        case [year]:
            main(year)
        case [year, day]:
            main(year, day)
        case [year, day, part]:
            main(year, day, part)