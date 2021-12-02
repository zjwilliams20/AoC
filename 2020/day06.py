#########################
# day 6
#########################

import csv

# load data
raw = []
with open("input/day6", 'r') as file:
    reader = csv.reader(file, delimiter='\n')
    raw = [line for line in reader]


# part 1 - find total # of yeses
nYeses = 0
yestions = set()
for idx, line in enumerate(raw):
    if line:
        [yestions.add(c) for c in line[0]]

        if idx == len(raw)-1:
            nYeses += len(yestions)
    else:
        nYeses += len(yestions)
        yestions = set()

print(f"Found {nYeses} yeses!")

# part 2 - find total # of everybody yeses
def countChars(group):
    '''count how many characters all strings contain'''
    chars = set(''.join(group))
    nChars = 0
    for c in chars:
        nChars += all([c in person for person in group])
    return nChars

nGroups, nAllYeses = 0, 0
groups = [[]]
for idx, line in enumerate(raw):
    if line:
        groups[nGroups].append(line[0])

        if idx == len(raw)-1:
            nAllYeses += countChars(groups[nGroups])
    else:
        nAllYeses += countChars(groups[nGroups])
        nGroups += 1
        groups.append([])

print(f"Found {nAllYeses} yestions!")
