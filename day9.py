#########################
# day 9
#########################

import numpy as np

with open('input/day9', 'r') as file:
    numbers = np.fromfile(file, sep='\n', dtype=int)

# part 1
for idx, n in enumerate(numbers[25:]):
    nFound = False
    for i in range(idx,idx+25):
        for j in range(idx,idx+25):
            if i == j:
                continue
            else:
                if numbers[i] + numbers[j] == n:
                    nFound = True
    if not nFound:
        print(f'CULPRIT: {n}')
        culprit = n
        break

# part 2
nTest = []
nFound = False
for idx, n in enumerate(numbers):
    nTest = [n]
    c = 1
    while np.sum(nTest) < culprit:
        nTest.append(numbers[idx+c])
        c += 1
        if np.sum(nTest) == culprit:
            weakness = nTest
            print(f'found the culprit!! {nTest}')
            print(f'weakness={np.min(nTest) + np.max(nTest)}')
            exit()
