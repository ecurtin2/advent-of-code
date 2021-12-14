from collections import Counter
from dataclasses import dataclass, field
import pytest


@dataclass
class Node:
    name: str
    connects: list["Node"] = field(default_factory=list)

    def __hash__(self):
        return hash(self.name)

    def __post_init__(self):
        self.is_small = not all(c.isupper() for c in self.name)

    @staticmethod
    def get_or_create(name, graph: list["Node"]) -> "Node":
        try:
            return next(n for n in graph if n.name == name)
        except StopIteration:
            n = Node(name=name)
            graph.append(n)
            return n

    def attach(self, other: "Node"):
        self.connects.append(other)
        other.connects.append(self)

    def can_be_added(self, path: list["Node"], can_visit_twice: bool) -> bool:
        if not self.is_small:
            return True
        if self.name == "start":
            return False

        counts = Counter(n.name for n in path if n.is_small)
        if any(count == 2 for count in counts.values()):
            return counts[self.name] == 0

        if can_visit_twice:
            can_do = counts[self.name] <= 1
        else:
            can_do = counts[self.name] == 0
        return can_do

    def __repr__(self):
        return f"{self.name} -> {[n.name for n in self.connects]}"

    def find_paths_to(
        self, other: "Node", can_visit_twice: bool, path=None
    ) -> list[list["Node"]]:
        if path is None:
            path = [self]
        if self is other:
            return [path]

        return sum(
            (
                n.find_paths_to(
                    other,
                    can_visit_twice,
                    path + [n],
                )
                for n in path[-1].connects
                if n.can_be_added(path, can_visit_twice)
            ),
            [],
        )


def get_paths(inputs: str, can_visit_twice: bool) -> list:
    pairs = [l.split("-") for l in inputs.splitlines()]
    graph = []
    for n1, n2 in pairs:
        Node.get_or_create(n1, graph).attach(Node.get_or_create(n2, graph))

    start = next(n for n in graph if n.name == "start")
    end = next(n for n in graph if n.name == "end")
    return start.find_paths_to(end, can_visit_twice=can_visit_twice)


def p1(inputs: str) -> int:
    return len(get_paths(inputs, can_visit_twice=False))


def p2(inputs: str) -> int:
    return len(get_paths(inputs, can_visit_twice=True))


@pytest.fixture()
def short():
    return """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


@pytest.fixture()
def medium():
    return """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


@pytest.fixture()
def long():
    return """"fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def check_expectations(given, expects: str):
    expected_paths = {tuple(l.split(",")) for l in expects.splitlines()}
    got = {tuple(n.name for n in path) for path in given}
    missing = expected_paths - got
    extra = got - expected_paths
    if missing:
        print("Missing:")
        for p in missing:
            print(p)
    if extra:
        print("Extra:")
        for p in extra:
            print(p)

    if missing or extra:
        raise ValueError(
            f"Missing or extra: got {len(got)} expected {len(expected_paths)}"
        )


def test_p1_short(short):
    check_expectations(
        get_paths(short, False),
        """start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end""",
    )


def test_p1_medium(medium):
    check_expectations(
        get_paths(medium, False),
        """start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end""",
    )


def test_p1_long(long):
    assert len(get_paths(long, False)) == 226


def test_p2_short(short):
    check_expectations(
        get_paths(short, True),
        """start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end""",
    )


def test_p2_medium():
    assert (
        p2(
            """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
        )
        == 103
    )


def test_p2_long():
    assert (
        p2(
            """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""
        )
        == 3509
    )
