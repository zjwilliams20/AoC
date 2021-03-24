#########################
# day 17
#########################

import numpy as np

def tupAdd(t1, t2):
    return tuple(map(lambda a, b: a + b, t1, t2))

with open('input/day17', 'r') as file:
    plane = [line.strip() for line in file.readlines()]
    conway = np.zeros((len(plane), len(plane[0])))
    for i, line in enumerate(plane):
        for j, char in enumerate(line):
            conway[i, j] = 1 if char == '#' else 0

# create space from conway
xM, yM = conway.shape
extra = 12
space = np.zeros([17, 17, yM+extra, xM+extra], dtype=int)
w, z, y, x = space.shape
space[w//2, z//2, y//2 - yM//2: y//2 + yM//2, x//2 - xM//2:x//2 + xM//2] = conway

def getNeighbors(space, pos):
    """return the sum of the 26 neighbors from a position in space"""
    neighborInd = []
    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                for w in range(-1,2):
                    neighborInd.append(tupAdd(pos, (w, z, y, x)))
    neighborInd.pop(40)
    return neighborInd

def sumNeighbors(space, pos):
    neighbors = getNeighbors(space, pos)
    nW, nZ, nY, nX = zip(*neighbors)
    return sum(space[nW, nZ, nY, nX])

def mapInd(space, pos):
    """map spatial index (0, 0, 0) to the np index in the middle of the space, etc."""
    w, z, y, x = space.shape
    return tupAdd(pos, (w//2, z//2, y//2, x//2))

def activeRegion(space):
    """find the two points that bound the currently active region"""
    wH, zH, yH, xH = (0, 0, 0, 0)
    wL, zL, yL, xL = space.shape
    w, z, y, x = space.shape
    for i in range(w):
        for j in range(z):
            for k in range(y):
                for l in range(x):
                    if space[i, j, k, l] != 0:
                        if i < wL: wL = i
                        if j < zL: zL = j
                        if k < yL: yL = k
                        if l < xL: xL = l
                        if i > wH: wH = i
                        if j > zH: zH = j
                        if k > yH: yH = k
                        if l > xH: xH = l
    return (wL-1, zL-1, yL-1, xL-1), (wH+1, zH+1, yH+1, xH+1)

def showSpace(space, pos=None, mark=False):
    """only works in 3D bc i'm lazy"""
    (zL, yL, xL), (zH, yH, xH) = activeRegion(space)
    
    safeSpace = space.copy()

    # TEMP: mark neighbors
    if mark:
        neighbors = getNeighbors(space, pos)
        nZ, nY, nX = zip(*neighbors)
        safeSpace[nZ, nY, nX] = -1

    for z in range(zL, zH+1):
        print('--------------------------')
        print(f'z = {z}\n')
        print('_' * (xH - xL + 5))
        for y in range(yL, yH+1):
            print('| ', end='')
            for x in range(xL, xH+1):
                if (z, y, x) == pos: print('@', end='')
                elif safeSpace[z, y, x] == 1: print('#', end='')
                elif safeSpace[z, y, x] == 0: print('.', end='')
                else: print('+', end='')
            print(' |')
        print('_' * (xH - xL + 5))


# iterate through every point in the active region, apply the rules
#   to determine the evolution over 6 cycles
for cycle in range(6):
    nextSpace = space.copy()
    (wL, zL, yL, xL), (wH, zH, yH, xH) = activeRegion(space)
    print('==========' * 8)
    print(f'CYCLE: {cycle+1}')
    print(f'MIN: ({wL}, {zL}, {yL}, {xL})', end='\t')
    print(f'Max: ({wH}, {zH}, {yH}, {xH})')
    # showSpace(space)

    for w in range(wL, wH+1):
        for z in range(zL, zH+1):
            for y in range(yL, yH+1):
                for x in range(xL, xH+1):
                    # if active cube, needs 2 | 3 to stay active
                    if space[w, z, y, x]:
                        neighborSum = sumNeighbors(space, (w, z, y, x))
                        if neighborSum not in range(2, 3+1):
                            nextSpace[w, z, y, x] = 0
                    
                    # if inactive cube, needs 3 to become active
                    if not space[w, z, y, x]:
                        neighborSum = sumNeighbors(space, (w, z, y, x))
                        if neighborSum == 3:
                            nextSpace[w, z, y, x] = 1
    space = nextSpace.copy()

print(f'active cubes: {np.sum(space)}')