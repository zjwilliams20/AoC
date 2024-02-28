#!/usr/bin/env python

import re

test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def _count_condition(lines, overlap_func):
    count = 0
    for line in lines:
        bounds = [int(n) for n in re.findall(r"\d+", line)]
        count += overlap_func(*bounds)
    return count
    

def part1(lines):
    overlap_func = lambda lmin, lmax, rmin, rmax: \
        rmin <= lmin and rmax >= lmax or rmin >= lmin and rmax <= lmax
    return _count_condition(lines, overlap_func)


def part2(lines):
    overlap_func = lambda lmin, lmax, rmin, rmax: \
        min(rmax, lmax) - max(rmin, lmin) + 1 > 0
    return _count_condition(lines, overlap_func)


if __name__ == "__main__":
    with open("2022/input/04.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))
