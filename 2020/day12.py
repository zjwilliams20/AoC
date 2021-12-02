#########################
# day 12
#########################

from csv import reader
from math import sin, cos, radians
import numpy as np

with open('input/day12', 'r') as file:
    reader = reader(file)
    directions = [line[0] for line in reader]

# part 1
pos = [0, 0]
head = 0
for idx, inst in enumerate(directions):
    direction, amount = inst[0], int(inst[1:])

    if direction == 'N':
        pos[1] += amount
    elif direction == 'S':
        pos[1] -= amount
    elif direction ==  'E':
        pos[0] += amount
    elif direction == 'W':
        pos[0] -= amount
    elif direction == 'L':
        head = (head + amount) % 360
    elif direction == 'R':
        head = (head - amount) % 360
    elif direction == 'F':
        dx, dy = cos(radians(head))*amount, sin(radians(head))*amount
        pos = [pos[0]+dx, pos[1]+dy]
    else:
        print(f'unknown direction? {direction}')
        exit

# part 2
def rotate(pos, theta):
    '''rotate a point about the origin by theta radians'''
    rot = np.array([[cos(theta), -sin(theta)], 
                    [sin(theta), cos(theta)]])
    return np.matmul(wPos, rot)

pos = [0, 0]
wPos = [10, 1]
for idx, inst in enumerate(directions):
    direction, amount = inst[0], int(inst[1:])
    
    if direction == 'N':
        wPos[1] += amount
    elif direction == 'S':
        wPos[1] -= amount
    elif direction == 'E':
        wPos[0] += amount
    elif direction == 'W':
        wPos[0] -= amount
    elif direction == 'L':
        wPos = rotate(wPos, -radians(amount))
    elif direction == 'R':
        wPos = rotate(wPos, radians(amount))
    elif direction == 'F':
        pos[0] += wPos[0] * amount
        pos[1] += wPos[1] * amount
    else:
        print(f'unknown direction? {direction}')
        exit

pos = [round(abs(p)) for p in pos]
print(sum(pos))
