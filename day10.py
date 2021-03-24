#########################
# day 10
#########################

import numpy as np

with open('input/day10', 'r') as file:
    adapters = np.fromfile(file, dtype=int, sep='\n')

# part 1
diffs = []
chain = [0]
while len(chain) < len(adapters)+1:
    
    # get current number
    current = chain[-1]

    # find the closest adapter
    one_jolt   = np.where(adapters == current+1)
    two_jolt   = np.where(adapters == current+2)
    three_jolt = np.where(adapters == current+3)

    if one_jolt[0].size > 0:
        diffs.append(1)
        chain.append(int(*adapters[one_jolt]))
    elif two_jolt[0].size > 0:
        diffs.append(2)
        chain.append(int(*adapters[two_jolt]))
    elif three_jolt[0].size > 0:
        diffs.append(3)
        chain.append(int(*adapters[three_jolt]))
    else:
        raise AssertionError(f"<ERROR: couldn't find adapter for {current}>")

# built-in adapter
chain.append(chain[-1]+3)
diffs.append(3)

nOnes = diffs.count(1)
nThrees = diffs.count(3)
print(f'{nOnes} * {nThrees} = {nOnes * nThrees} adapters')

# part 2
# make lists of contigous steps
newList = True
seqs = []
for n in diffs:
    if n == 1:
        if newList:
            seqs.append([])
            seqs[-1].append(n)
            newList = False
        else:
            seqs[-1].append(n)
    else:
        newList = True

# brainstorm
# sequence -->     # ones: # ways (ncr(<2), ncr(>2))
# 3 1 3 -->             0: 1 (1, 0)
# 3 1 1 3 -->           1: 2 (2, 0)
# 3 1 1 1 3 -->         2: 4 (4, 0)
# 3 1 1 1 1 3 -->       3: 7 (7, 0)   
# 3 1 1 1 1 1 3 -->     4: 13 (11, 2) 
# 3 1 1 1 1 1 1 3 -->   5: 22 (16, 6)

# compute amount of combinations for each sequence
comboMap = {1:1, 2:2, 3:4, 4:7, 5:13, 6:22}
combos = [comboMap[len(seq)] for seq in seqs]

# number of arrangements is permutation of all combos
ans = np.prod(combos)
print(f'found {ans} combinations!!!')