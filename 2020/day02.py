#########################
# day 2
#########################

import re

# load data
policies = []
with open("input/day2", 'r') as file:
    policies = [line.strip() for line in file.readlines()]

# parse for correct passwords
# part 1
nValid = 0
for p in range(0,len(policies)):
    info = re.split(r':|-| ',policies[p])
    pMin, pMax = int(info[0]), int(info[1])
    pLet, pStr = info[2], info[4]
    nLet = pStr.count(pLet)
    if pMin <= nLet <= pMax:
        nValid += 1

print(f"part 1: counted {nValid} good passwords...")

# part 2
nValid = 0
for p in range(0,len(policies)):
    info = re.split(r':|-| ',policies[p])
    pMin, pMax = int(info[0]), int(info[1])
    pLet, pStr = info[2], info[4]
    if pStr[pMin-1] == pLet and pStr[pMax-1] != pLet or \
       pStr[pMin-1] != pLet and pStr[pMax-1] == pLet:
        nValid += 1

print(f"part 2: counted {nValid} good passwords...")

