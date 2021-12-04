from functools import reduce
from itertools import tee
from operator import mul
from typing import Callable, Generator, Iterable, List, Optional, Tuple


def split(
    iterable: Iterable,
    on: Callable = lambda s: s.strip() == "",
    include_edges: bool = False,
) -> Generator[List, None, None]:
    result = []
    for thing in iterable:
        if on(thing):
            if include_edges:
                result.append(thing)
            yield result
            result = []
        else:
            result.append(thing)

    # last chunk if exists
    if result:
        yield result


def product(iterable):
    return reduce(mul, iterable, 1)


def diff(iterable):
    a, b = tee(iterable)
    next(b, None)
    return (x[1] - x[0] for x in zip(a, b))


def pop_number(s: str) -> Tuple[Optional[int], str]:
    """  '1234abcdef' -> (1234, 'abcdef') """
    for i in range(len(s)):
        if not s[: i + 1].isnumeric():
            try:
                return int(s[:i]), s[i:]
            except ValueError:
                return None, s
