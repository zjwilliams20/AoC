#!/usr/bin/env python

import re

HEIGHT = 7


def build_stack(text):
    N_STACKS = 9
    stacks = {i: "" for i in range(1, N_STACKS+1)}
    for line in text[::-1]:
        for istack in range(N_STACKS):
            cargo = line[1+istack*4]
            if cargo != " ":
                stacks[istack+1] += cargo
    return stacks

def _setup(lines):
    stacks = build_stack(lines[:HEIGHT+1])
    instructions = lines[HEIGHT+3:]
    return stacks, instructions

def part1(lines):
    stacks, instructions = _setup(lines)
    for instr in instructions:
        n, src, dest = [int(q) for q in re.findall(r"\d+", instr)]
        stacks[dest] += stacks[src][-n:][::-1]
        stacks[src] = stacks[src][:-n]
    return "".join([cargo[-1] for cargo in stacks.values()])


def part2(lines):
    stacks, instructions = _setup(lines)
    for instr in instructions:
        n, src, dest = [int(q) for q in re.findall(r"\d+", instr)]
        stacks[dest] += stacks[src][-n:]
        stacks[src] = stacks[src][:-n]
    return "".join([cargo[-1] for cargo in stacks.values()])


if __name__ == "__main__":
    with open("2022/input/05.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))
