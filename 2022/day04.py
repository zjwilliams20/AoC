#!/usr/bin/env python

import re

test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def part1(lines):
    n_full_overlaps = 0
    for line in lines:
        lmin, lmax, rmin, rmax = [int(n) for n in re.findall(r"\d+", line)]
        n_full_overlaps += rmin <= lmin and rmax >= lmax \
            or rmin >= lmin and rmax <= lmax
    return n_full_overlaps


def part2(lines):
    n_overlaps = 0
    for line in lines:
        lmin, lmax, rmin, rmax = [int(n) for n in re.findall(r"\d+", line)]
        n_overlaps += min(rmax, lmax) - max(rmin, lmin) + 1 > 0
    return n_overlaps


if __name__ == "__main__":
    with open("2022/input/04.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))
