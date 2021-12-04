from typing import List


def part1(numbers: List[int], total: int = 2020):
    set_ = set(numbers)
    pairs = {
        tuple(sorted((i, total - i))) for i in numbers if (total - i) in (set_ - {i})
    }
    if len(pairs) != 1:
        raise ValueError(f"Ambiguous answer: {pairs}")
    first, second = pairs.pop()
    return first * second


def part2(numbers: List[int], total: int = 2020) -> int:
    for first in numbers:
        total_2 = total - first
        seconds = [n2 for n2 in numbers if n2 <= total_2]
        if not seconds:
            continue

        for second in seconds:
            total_3 = total_2 - second
            third = [n3 for n3 in numbers if n3 == total_3]
            if len(third) == 1:
                return first * second * third[0]

    raise ValueError("No triplets found")


def test_part1():
    assert part1([1721, 979, 366, 299, 675, 1456]) == 514579


def test_part2():
    assert part2([1721, 979, 366, 299, 675, 1456]) == 241861950
