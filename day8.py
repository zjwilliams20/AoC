#########################
# day 8
#########################

import csv

def parseInst(line):
    cmd, amt = line.split()
    amt = int(amt)
    return cmd, amt

instructions = []
with open('input/day8', 'r') as file:
    reader = csv.reader(file, delimiter='\n')
    instructions = [line[0] for line in reader]

visited = []
tested = []
needTest = True
acc = 0
loc = 0
c = 0
while loc != len(instructions):

    # if we've already been here
    if loc in visited:
        loc = 0
        acc = 0
        visited = []
        needTest = True
        continue

    # parse instruction
    inst = instructions[loc]
    cmd, amt = parseInst(inst)
    visited.append(loc)

    # wassup
    print(f'{c}\t{loc}:\t\t{acc=}\t\t{inst}')

    # do the thing
    if cmd == "acc":
        acc += amt
        loc += 1
    elif cmd == "jmp":
        # jmp
        if not needTest or loc in tested:
            loc += amt
        # nop
        else:
            tested.append(loc)
            needTest = False
            loc += 1
    elif cmd == "nop":
        # nop
        if not needTest or loc in tested:
            loc += 1
        # jmp
        else:
            tested.append(loc)
            needTest = False
            loc += amt

    c += 1

print(f"DONE!\tACCUMULATOR = {acc}")