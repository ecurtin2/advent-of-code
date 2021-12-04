import importlib
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev
from time import time
from typing import Any, List, Optional, Tuple, get_type_hints

import cattr
import click

AVAILABLE_DAYS: List[int] = sorted(
    int(str(p.name).replace("d", "").replace(".py", ""))
    for p in Path(__file__).parent.rglob("d*.py")
)


cattr.register_structure_hook(List[int], lambda s, _: [int(l) for l in s.splitlines()])
cattr.register_structure_hook(List[str], lambda s, _: s.splitlines())


def timeit(f, *args, **kwargs) -> Tuple[float, float]:
    times = []
    for _ in range(1):
        begin = time()
        f(*args, **kwargs)
        times.append(time() - begin)
    return mean(times), stdev(times)


@dataclass
class Run:
    day: int
    part: int
    result: Optional[Any] = None
    mean_duration_ms: Optional[float] = None
    std_duration_ms: Optional[float] = None

    def execute(self, timed: bool = False):
        module = importlib.import_module(f"d{self.day}")

        input_path = Path(f"inputs/d{self.day}p{self.part}.txt")
        if (not input_path.is_file()) and (self.part != 1):
            # fallback since sometimes same input reused.
            input_path = Path(f"inputs/d{self.day}p1.txt")
        try:
            raw_str = input_path.read_text()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No data file found for day {self.day} part {self.part}. Expected {input_path}"
            )

        func = getattr(module, f"part{self.part}")
        typ = list(get_type_hints(func).values())[0]
        inp = cattr.structure(raw_str, typ)
        self.result = func(inp)
        if timed:
            m, s = timeit(func, inp)
            self.mean_duration_ms = m * 1000
            self.std_duration_ms = s * 1000


@click.command()
@click.option(
    "--day",
    "-d",
    type=click.Choice([str(d) for d in AVAILABLE_DAYS] + ["all"]),
    required=False,
    default="all",
)
@click.option("--part", "-p", type=click.Choice(["1", "2"]), required=False)
@click.option("--timed/--no-timed", default=False)
def cli(day: int, part: Optional[int], timed: bool):
    if part is None:
        parts = [1, 2]
    else:
        parts = [part]

    if day == "all":
        runs = [Run(day=d, part=p) for d in AVAILABLE_DAYS for p in parts]
    else:
        runs = [Run(day=int(day), part=p) for p in parts]

    last_day = -1
    for run in runs:
        run.execute(timed=timed)
        if run.day != last_day:
            print(f"\nDay {run.day}\n--------------------------------")
        last_day = run.day
        print(f"Part {run.part}:\n  Result: {run.result}")
        if run.mean_duration_ms:
            print(
                f"  Time: {run.mean_duration_ms:07.4f} +/- {run.std_duration_ms:07.4f}ms"
            )


if __name__ == "__main__":
    cli()
