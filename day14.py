#########################
# day 14
#########################

import csv
import numpy as np

def setBits(val, idx):
    for i in idx:
        val |= (1 << i)
    return val

def clcBits(val, idx):
    for i in idx:
        val &= ~(1 << i)
    return val

def countBin(nBits):
    binNums = [[]]
    for c in range(2 ** nBits):
        for i in range(nBits)[::-1]:
            binNums[c].append(int((c >> i & 1) != 0))
        binNums.append([])
    binNums.pop()

    return binNums

with open('input/day14', 'r') as file:
    reader = csv.reader(file)
    program = [line[0] for line in reader]

# part 1
memory = {}
for line in program:
    cmd, num = line.split('=')

    # udpate mask
    if cmd.strip() == 'mask':
        mask = num.strip()
        setIdx = [(-i-1) % len(mask) for i in range(len(mask)) if mask[i] == '1']
        clcIdx = [(-i-1) % len(mask) for i in range(len(mask)) if mask[i] == '0']

    # apply mask to value
    elif 'mem' in cmd:
        addr = int(cmd[4:-2])
        val = setBits(int(num), setIdx)
        val = clcBits(val, clcIdx)
        memory[addr] = val
    else:
        raise AssertionError(f"huhh?? --> {line}")

print(f'Memory ended with: {sum(memory.values())}!')

# part 2
memory = {}
for line in program:
    # print(line)
    cmd, num = line.split('=')

    # update mask and binary list
    if cmd.strip() == 'mask':
        mask = num.strip()
        setIdx = [(-i-1) % len(mask) for i in range(len(mask)) if mask[i] == '1']
        fltIdx = [(-i-1) % len(mask) for i in range(len(mask)) if mask[i] == 'X']

        nBits = len(fltIdx)
        binNums = countBin(nBits)

    # compute target addresses from binary list and update those addresses
    elif 'mem' in cmd:
        baseAddr = int(cmd[4:-2])
        baseAddr = setBits(baseAddr, setIdx)
        addrs = []
        for b in binNums:
            addr = setBits(baseAddr, [fltIdx[i] for i in range(nBits) if b[i] == 1])
            addr = clcBits(addr, [fltIdx[i] for i in range(nBits) if b[i] == 0])
            addrs.append(addr)
        for addr in addrs:
            memory[addr] = int(num)
    else:
        raise AssertionError(f"huhh?? --> {line}")

print(f'Memory ended with: {sum(memory.values())}!')
