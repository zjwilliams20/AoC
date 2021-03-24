#########################
# day 11
#########################

import csv
import numpy as np

def transform(string):
    numStr = []
    for char in string:
        if char == '.':
            numStr.append(0)
        elif char == 'L':
            numStr.append(-1)
        elif char == '#':
            numStr.append(1)
        else:
            print('ERROR')
            return []
    return np.array(numStr)

def printSeats(seats):
    w, l = len(seats[0]), len(seats)
    print('----------' * 10 + '+')
    for i in range(l):
        for j in range(w):
            pos = (i, j)
            current = seats[pos]
            if current == -1:
                print('L', end='')
            elif current == 0:
                print('.', end='')
            elif current == 1:
                print('#', end='')
        print('          |')


# load data
with open('input/day11', 'r') as file:
    reader = csv.reader(file)
    seats = np.array([transform(line[0]) for line in reader])

w, l = len(seats[0]), len(seats)

def getAdjacent(pos, seats, retInd=False):
    '''return seats closest to the position'''
    
    # get neighboring seats
    ind = [(pos[0]+i, pos[1]+j) for i in range(-1,2) for j in range(-1,2)]
    
    # remove current index
    ind.pop(4)

    # remove out of range indicies
    w, l = len(seats[0]), len(seats)
    inRange = lambda i: i[0] >= 0 and i[1] >= 0 and i[0] < l and i[1] < w
    ind = [i for i in ind if inRange(i)]

    # return neighboring seats
    if not retInd:
        return [seats[l] for l in ind]
    else:
        return [seats[l] for l in ind], ind

def getNeighbors(pos, seats):
    '''return closest visible seats from a position'''
    w, l = len(seats[0]), len(seats)

    # grab closest neighbors
    adjacent, adjacentInd = getAdjacent(pos, seats, True)

    neighbors = []
    for i, n in enumerate(adjacent):
        # if the adjacent is floor, look for the next closest
        if n == 0:

            # set starting neighbor position
            nPos = adjacentInd[i]

            # travel in this direction
            diff = tuple(map(lambda x, y: x - y, nPos, pos))
            
            nFound = False
            while not nFound:
                nPos = tuple(map(lambda x, y: x + y, nPos, diff))
                if nPos[0] < 0 or nPos[1] < 0 or nPos[0] >= l or nPos[1] >= w:
                    break
                if seats[nPos] != 0:
                    nFound = True
                    neighbors.append(seats[nPos])
                    
        # append the neighbor if he isn't the floor
        else:
            neighbors.append(n)

    return neighbors

nRounds = 0
changed = True
while changed:

    # reset seat changes and update flag
    newSeats = seats.copy()
    changed = False

    for i in range(l):
        for j in range(w):

            # get the current seat
            pos = (i, j)
            current = seats[pos]

            # update the seat based on occupied neighbors
            # floor - '.'
            if current == 0:
                pass

            # empty - 'L'
            elif current == -1:
                neighbors = getNeighbors(pos, seats)

                # fill seat if no neighbors are occupied
                if neighbors.count(1) == 0:
                    newSeats[pos] = 1
                    changed = True

            # filled - '#'
            elif current == 1:
                neighbors = getNeighbors(pos, seats)

                # empty seat if 4+ neighbors are filled
                if neighbors.count(1) >= 5:
                    newSeats[pos] = -1
                    changed = True

    # update seats based on changes
    seats = newSeats.copy()
    nRounds += 1

printSeats(newSeats)
unique, counts = np.unique(seats, return_counts=True)
occurences = dict(zip(unique, counts))
print(f'found {occurences[1]} occpied seats after {nRounds} rounds!')
