#!/usr/bin/env python
# day02.py

import numpy as np

with open("./input/day02", 'r') as file:
    data = [line.strip().split() for line in file.readlines()]

pos = np.zeros(2)
for step in data:
    cmd = step[0]
    X = int(step[1])

    if cmd == 'forward':
        pos[0] += X
    elif cmd == 'up':
        pos[1] -= X
    elif cmd == 'down':
        pos[1] += X

print(f'Part 1: {int(np.prod(pos))}')

aim = 0.0
pos = np.zeros(2)
for step in data:
    cmd = step[0]
    X = int(step[1])

    if cmd == 'forward':
        pos[0] += X
        pos[1] += aim * X
    elif cmd == 'up':
        aim -= X
    elif cmd == 'down':
        aim += X

print(f'Part 2: {int(np.prod(pos))}')
