from dataclasses import dataclass, field
from functools import cache
from utils import parse_run
from typing import Optional


@dataclass
class Node:
    name: str
    parent: Optional["Node"] = None
    children: list["Node"] = field(default_factory=list)
    size: int = 0

    @property
    def is_dir(self):
        return self.size == 0

    def add_child(self, name: str, size: int = 0):
        self.children.append(Node(name, parent=self, size=size))

    def get_child(self, name: str) -> "Node":
        for child in self.children:
            if child.name == name:
                return child
        raise KeyError(f"{self} has no child named {name}")

    def iter_tree(self, depth=0, dirs_only: bool = False):
        yield depth, self
        for node in self.children:
            yield from node.iter_tree(depth=depth + 1)

    def total_size(self) -> int:
        return sum(c.size for _, c in self.iter_tree())

    def print_tree(self):
        for depth, node in self.iter_tree():
            pad = " " * depth
            print(
                f"{pad}{node.name.rstrip('/')}{'/' if node.is_dir else ' ' + str(node.size)}"
            )

    def __str__(self):
        return f"{self.name}, {self.size}"

    def __repr__(self):
        return str(self)


def parse(inputs: list[str]) -> Node:
    first, *rest = inputs
    root = Node(name=first.split()[-1])
    cd = root
    for line in rest:
        match line.split():
            case ["$", "ls"]:
                pass
            case ["$", "cd", ".."]:
                if cd.parent is None:
                    raise ValueError("Cannot move above root!")
                cd = cd.parent
            case ["$", "cd", d]:
                cd = cd.get_child(d)
            case ["dir", d]:
                cd.add_child(d, 0)
            case [size, f]:
                cd.add_child(f, int(size))
            case _:
                raise ValueError("Could not parse command: {line}")
    return root


def p1(inputs: list[str]) -> int:
    root = parse(inputs)
    return sum(
        n.total_size()
        for _, n in root.iter_tree()
        if (n.total_size() <= 100_000) and n.is_dir
    )


def p2(inputs: list[str]) -> int:
    root = parse(inputs)
    total_disk = 70_000_000
    update_size = 30_000_000
    unused = total_disk - root.total_size()
    needed = update_size - unused

    dir_sizes = [
        d.total_size()
        for _, d in root.iter_tree()
        if d.is_dir and d.total_size() > needed
    ]
    return min(dir_sizes)


def test_p1():
    input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
    assert parse_run(p1, input) == 95437


def test_p2():
    input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
    assert parse_run(p2, input) == 24933642
