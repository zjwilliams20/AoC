#!/usr/bin/env python

from functools import reduce


def priority(letter):
    if ord(letter) in range(ord("a"), ord("z")+1):
        return ord(letter) - (ord("a") - 1)
    return ord(letter) - (ord("A") - 27)


def part1(lines):
    psum = 0
    for line in lines:
        left, right = line[:len(line)//2], line[len(line)//2:].strip()
        common = tuple(set(left) & set(right))[0]
        psum += priority(common)
    return psum
        

def part2(lines):
    psum = 0
    for igrp in range(len(lines)//3):
        group = [set(line.strip()) for line in lines[3*igrp:3*igrp+3]]
        common = tuple(reduce(set.intersection, group))[0]
        psum += priority(common)
        print(common, priority(common))
    return psum

if __name__ == "__main__":
    with open("2022/input/03.txt") as file:
        lines = list(file)

    print("1: ", part1(lines))
    print("2: ", part2(lines))
