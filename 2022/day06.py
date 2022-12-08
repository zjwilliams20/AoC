#!/usr/bin/env python


def _find_first_packet(text, length):
    for i in range(len(text) - length):
        packet = text[i: i+length]
        if len(set(packet)) == length:
            return i + length

def part1(text):
    return _find_first_packet(text, 4)


def part2(text):
    return _find_first_packet(text, 14)
    

if __name__ == "__main__":
    with open("2022/input/06.txt") as file:
        text = file.read()

    print("1: ", part1(text))
    print("2: ", part2(text))
