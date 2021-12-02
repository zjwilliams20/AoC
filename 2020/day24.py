#########################
# day 24
#########################

import re
import numpy as np
import matplotlib.pyplot as plt


with open('input/day24', 'r') as file:
    instructions = [line.strip() for line in file.readlines()]
instructions = list(re.findall(r'(se|sw|ne|nw|e|w)', i) for i in instructions)


def walk(lobby, instruction):
    '''follow the instructions and flip the tile at the last position'''
        
    # find the displacement
    dx, dy = 0, 0
    for i in instruction:
        if i == 'e':
            dx += 2
        elif i == 'se':
            dx += 1
            dy += 1
        elif i == 'sw':
            dx -= 1
            dy += 1
        elif i == 'w':
            dx -= 2
        elif i == 'nw':
            dx -= 1
            dy -= 1
        elif i == 'ne':
            dx += 1
            dy -= 1
    
    # flip the tile at that displacement from the reference tile
    if (dx, dy) in lobby:
        lobby[(dx, dy)] = lobby[(dx, dy)] == 0
    else:
        lobby[(dx, dy)] = True


def balconyView(lobby):
    
    blacks = [key for key, val in lobby.items() if val]
    whites = [key for key, val in lobby.items() if not val]
    bX, bY = [b[0] for b in blacks], [b[1] for b in blacks]
    wX, wY = [w[0] for w in whites], [w[1] for w in whites]

    plt.figure()
    plt.scatter(bX, bY, c='k')
    plt.scatter(wX, wY, c='r')
    plt.scatter(0, 0, s=80, c='b')


# iterate through instructions, traverse the lobby
lobby = {}
for instruction in instructions:
    walk(lobby, instruction)
print(f'Part 1: {sum(lobby.values())}')


def getNeighbors(pos):
    '''get the indicies of the neighbors at a given position'''

    x, y = pos[0], pos[1]
    neighbors = [(x+2, y), (x+1, y+1), (x-1, y+1),
                 (x-2, y), (x-1, y-1), (x+1, y-1)]
    return neighbors


def livingArt(lobby):
    '''evolve the lobby over one day'''

    changes = {}
    for tile in lobby:

        # check the tile and all of its neighbors
        neighbors = getNeighbors(tile)
        neighbors.append(tile)

        for nTile in neighbors:
            
            # count number of black neighbors
            itsNeighbors = getNeighbors(nTile)
            neighborSum = 0
            for neighbor in itsNeighbors:
                if neighbor in lobby:
                    neighborSum += lobby[neighbor]
            
            # black tile needs 0 or 2+ black neighbors to flip
            if (nTile in lobby and lobby[nTile] and 
               (neighborSum == 0 or neighborSum > 2)):
                changes[nTile] = False
            # white tile needs 2 black neighbors to flip
            elif ((nTile in lobby and not lobby[nTile] or nTile not in lobby) 
                   and neighborSum == 2):
                changes[nTile] = True
    
    # update the lobby with the changes
    for change, val in changes.items():
        lobby[change] = val

for day in range(100):
    livingArt(lobby)
print(f'Part 2: {sum(lobby.values())}')
