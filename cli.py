from importlib import import_module
from pathlib import Path
from timeit import default_timer as timer
from typing import Optional

from typer import Typer
from rich.console import Console
from rich.table import Table

from utils import parse_run


App = Typer()


def run(year: int, day: int, part: int):
    mod = import_module(f"year{year}.d{day}")
    func = getattr(mod, f"p{part}")

    input_file = Path(f"year{year}/data/d{day}p{part}.txt")

    start = timer()

    # Fallback on part 1 since often reused
    if not input_file.is_file():
        input_file = Path(f"year{year}/data/d{day}p1.txt")

    input = input_file.read_text()
    result = parse_run(func, input)

    end = timer()
    return result, end - start


@App.command()
def main(year: int = 2022, day: int = 0, part: int = 0):

    year_folder = Path(__file__).parent / f"year{year}"
    if day == 0:
        days = sorted(int(p.stem[1:]) for p in year_folder.glob("d*.py"))
    else:
        days = [int(day)]
    if part == 0:
        parts = [1, 2]
    else:
        parts = [int(part)]

    data = []
    for day in days:
        for part in parts:
            result, duration = run(year, day, part)
            data.append(
                {
                    "Day": day,
                    "Part": part,
                    "Duration (ms)": f"{duration * 1000:5.2f}",
                    "Answer": result,
                }
            )

    if not data:
        print("No days / parts match, exiting...")
        exit()

    table = Table(title=f"Advent of Code {year} Results")

    for key in data[0]:
        table.add_column(key)

    for row in data:
        table.add_row(*[str(v) for v in row.values()])

    console = Console()
    console.print(table)


if __name__ == "__main__":
    App()
