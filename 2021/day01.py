#!/usr/bin/env python 
# day01.py

import numpy as np

data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
with open("./input/day01", 'r') as file:
    data = np.fromfile(file,sep='\n')

# part 1
print(f'part 1: {np.count_nonzero(np.diff(data) > 0)}')

# part 2
windows = []
for i in range(len(data)-2):
    windows.append(sum(data[i:i+3]))
    assert len(data[i:i+3]) == 3

print(f'part 2: {np.count_nonzero(np.diff(windows) > 0)}')
