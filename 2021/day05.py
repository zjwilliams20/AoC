#!/usr/bin/env python
# day05.py

import re

import numpy as np
import matplotlib.pyplot as plt

from util import Point, LineIter

# ideas:
# - pair-wise search
# - fill out a giant array
# - dictionary of all points

N_MAX = 1_000

def count_vents(lines, do_plot=False):
    """Sum up the number of points >= 2 from a list of lines."""

    data = np.zeros((N_MAX, N_MAX))
    for line in lines:
        for pt in line:
            data[pt] += 1

    if do_plot:
        plt.imshow(data)
        plt.show()

    return np.count_nonzero(data >= 2)

IGNORE_DIAGS = True # part 1
# IGNORE_DIAGS = False # part 2

lines = []
with open("2021/input/day05", "r") as file:
    for line in file.readlines():
        match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
        nums = [int(n) for n in match.groups()]
        lines.append(LineIter([Point(*nums[:2]), Point(*nums[2:])], ignore_diags=IGNORE_DIAGS))

plt.figure(figsize=(8,8))
n_vents = count_vents(lines, True)
print(f'Part X: {n_vents}')
