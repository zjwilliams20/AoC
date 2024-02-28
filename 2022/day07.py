#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path

test_str = """$ cd /
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


@dataclass(repr=False)
class Node:
    path: Path

    def __repr__(self, level=0):
        return level * "  " + f"{self.path}\n"


@dataclass(repr=False)
class File(Node):
    size: int


@dataclass(repr=False)
class Directory(Node):
    children: list = field(default_factory=list)

    def pop(self, path):
        child_ind = self.children_paths.index(path)
        return self.children.pop(child_ind)

    def append(self, child):
        self.children.append(child)

    @property
    def size(self):
        return sum(child.size for child in self.children)
    
    @property
    def children_paths(self):
        return [child.path for child in self.children]

    def __repr__(self, level=0):
        self_str = super().__repr__(level)
        child_str = "".join(child.__repr__(level+1) for child in self.children)
        return self_str + child_str


def _build_filesystem(lines):

    def _handle_line(line, loc, tree):
        print(line)
        if "rzbnmn" in line:
            pass
        match line.split():
            case ["$", "cd", dest]:
                loc /= dest
                loc = loc.resolve()
                
                if dest != "..":
                    # Remove the future directory from the tree to modify.
                    tree.append(tree[-1].pop(loc))
                else:
                    # Add it back into the tree to show that we're done.
                    _put_back_last_node(tree)

            case ["$", "ls"]:
                pass

            case ["dir", name]:
                tree[-1].append(Directory(loc / name))

            case [size, name]:
                tree[-1].append(File(loc / name, int(size)))
                
            case _:
                raise RuntimeError(f"huh? {line}")
        
        return tree, loc

    def _put_back_last_node(tree):
        node = tree.pop()
        tree[-1].append(node)

    loc = Path("/")
    tree = [Directory(loc)]

    # Assume we start at root.
    for line in lines[1:]:
        tree, loc = _handle_line(line, loc, tree)
    
    _put_back_last_node(tree)
    return tree[0]


def _count_sizes_lt(node, max_size, total=0):
    if not isinstance(node, Directory):
        return 0
    if node.size <= max_size:
        total += node.size

    for child in node.children:
        total += _count_sizes_lt(child, max_size)
    return total


def _find_smallest_directory_gte(node, min_size, best_size=1e20):
    if not isinstance(node, Directory) or node.size <= min_size:
        return best_size

    if node.size <= best_size:
        best_size = node.size

    child_best = min(
        _find_smallest_directory_gte(child, min_size, best_size) 
        for child in node.children
        )

    return min(child_best, best_size)


def part1(lines):
    tree = _build_filesystem(lines)
    return _count_sizes_lt(tree, 100000)


def part2(lines):
    tree = _build_filesystem(lines)

    # disk space - current size + delete size = unused space + delete size >= update size
    disk_space = 70000000
    update_size = 30000000
    unused_space = disk_space - tree.size
    min_size = update_size - unused_space

    return _find_smallest_directory_gte(tree, min_size)


if __name__ == "__main__":
    with open("2022/input/07.txt") as file:
        lines = list(file)

    # lines = test_str.split("\n")
    print("1: ", part1(lines))
    print("2: ", part2(lines))
