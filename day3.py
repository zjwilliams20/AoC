#########################
# day 3
#########################

import numpy as np

forest = []
with open("input/day3", 'r') as file:
    forest = [line.strip() for line in file.readlines()]

# part 1
right = 3
nTrees, nOpen, x = 0, 0, 0
for slope in forest:
    if slope[x] == '.':
        nOpen += 1
    elif slope[x] == '#':
        nTrees += 1
    else:
        exit("something went wrong")
    x = (x+right) % len(slope)

print(f"Counted {nTrees} trees and {nOpen} open spaces!")

# part 2
right  = [1, 3, 5, 7, 1]
down   = [1, 1, 1, 1, 2]
nTrees = [0, 0, 0, 0, 0]
nOpen  = [0, 0, 0, 0, 0]
for i in range(0,len(right)):
    x = 0
    for slope in forest[::down[i]]:
        if slope[x] == '.':
            nOpen[i] += 1
        elif slope[x] == '#':
            nTrees[i] += 1
        else:
            exit("something went wrong")
        x = (x+right[i]) % len(slope)

print(f"Product of trees: {np.prod(nTrees)}")
