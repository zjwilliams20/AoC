#!/usr/bin/env python


def _compute_score(lines, score_map):
    score = 0
    for line in lines:
        round = tuple(line.split())
        score += score_map[round]
    return score


def part1(lines):
    score_map = {
        ("A", "X"): 1 + 3,
        ("A", "Y"): 2 + 6,
        ("A", "Z"): 3 + 0,
        ("B", "X"): 1 + 0,
        ("B", "Y"): 2 + 3,
        ("B", "Z"): 3 + 6,
        ("C", "X"): 1 + 6,
        ("C", "Y"): 2 + 0,
        ("C", "Z"): 3 + 3,
    }
    return _compute_score(lines, score_map)


def part2(lines):
    score_map = {
        ("A", "X"): 3 + 0,
        ("A", "Y"): 1 + 3,
        ("A", "Z"): 2 + 6,
        ("B", "X"): 1 + 0,
        ("B", "Y"): 2 + 3,
        ("B", "Z"): 3 + 6,
        ("C", "X"): 2 + 0,
        ("C", "Y"): 3 + 3,
        ("C", "Z"): 1 + 6,
    }
    return _compute_score(lines, score_map)


if __name__ == "__main__":
    with open("2022/input/02.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))
