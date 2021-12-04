from typing import Generator, List

from utils import pop_number


def connected(matrix: List[List[int]], start_col: int) -> Generator[int, None, None]:
    nodes = [i for i in range(len(matrix)) if matrix[i][start_col] != 0]
    for node in nodes:
        yield node
        yield from connected(matrix, start_col=node)


def rules_to_connectivity_matrix(rules: List[str]):
    parsed_rules = {}
    for rule in rules:
        split = (
            rule.replace(".", "")
            .replace(",", "")
            .replace("bags", "bag")
            .replace("contain", "")
            .split("bag")[:-1]
        )
        cleaned = [s.replace(" ", "") for s in split]
        container, *rest = cleaned
        if rest == ["noother"]:
            parsed_rules[container] = {}
        else:
            parsed_rules[container] = {pop_number(x)[1]: pop_number(x)[0] for x in rest}

    color_to_idx = {k: i for i, k in enumerate(parsed_rules)}
    N = len(color_to_idx)
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    for k, v in parsed_rules.items():
        for k2, v2 in v.items():
            matrix[color_to_idx[k]][color_to_idx[k2]] = v2

    return matrix, color_to_idx


def part1(inp: List[str]) -> int:
    matrix, color_to_idx = rules_to_connectivity_matrix(inp)
    return len(set(connected(matrix, start_col=color_to_idx["shinygold"])))


def part2_recurse(matrix: List[List[int]], start_col: int) -> int:
    nodes = [i for i in range(len(matrix)) if matrix[start_col][i] != 0]
    return sum(
        matrix[start_col][node] * (1 + part2_recurse(matrix, start_col=node))
        for node in nodes
    )


def part2(inp: List[str]) -> int:
    matrix, color_to_idx = rules_to_connectivity_matrix(inp)
    return part2_recurse(matrix, start_col=color_to_idx["shinygold"])


def test_part1():
    inp = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    assert part1(inp.splitlines()) == 4


def test_part2():
    inp = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
    assert part2(inp.splitlines()) == 126
