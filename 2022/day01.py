#!/usr/bin/env python


def tally(lines):
    rsum = 0
    totals = []
    for line in lines:
        if stripped := line.strip():
            rsum += int(stripped)
        else:
            totals.append(rsum)
            rsum = 0
    totals.append(rsum)
    return totals


def part1(lines):
    return max(tally(lines))


def part2(lines):
    return sum(sorted(tally(lines))[-3:])


if __name__ == "__main__":
    with open("2022/input/01.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))

