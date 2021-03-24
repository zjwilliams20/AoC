#########################
# day 16
#########################

from math import prod

# parse input
with open('input/day16', 'r') as file:
    raw = file.readlines()
    raw = [line.strip() for line in raw]

rawRules  = []
yours  = []
nearby = []
for pos, line in enumerate(raw):
    if pos < 20:
        rawRules.append(line)
    elif pos == 22:
        yours = line
    elif pos >= 25:
        nearby.append(line)

# generate ticket lists
yours = [int(num) for num in yours.split(',')]
for pos, line in enumerate(nearby):
    nearby[pos] = [int(num) for num in line.split(',')]

# generate rules from raw rules
rules = {}
for rule in rawRules:
    name, ranges = rule.split(':')
    ranges = ranges.split('or')
    ranges = [int(val.strip()) for r in ranges for val in r.split('-')]
    ranges = [range(ranges[0], ranges[1]+1), range(ranges[2], ranges[3]+1)]
    rules[name] = ranges

# part 1
invalidNums = []
validTickets = []
for ticket in nearby:

    # innocent until proven guilty
    ticketValid = True
    for num in ticket:

        # guilty until proven innocent
        numValid = False
        for ranges in rules.values():
            if any([num in r for r in ranges]):
                numValid = True
                break
        if not numValid:
            invalidNums.append(num)
            ticketValid = False
    if ticketValid:
        validTickets.append(ticket)

print(f'ticket scanning error rate: {sum(invalidNums)}')

# part 2
nPos = len(validTickets[0])
fields = {name:list(range(nPos)) for name in rules.keys()}

# trash bad positions
for ticket in validTickets:
    for pos, num in enumerate(ticket):
        for name, ranges in rules.items():

            # remove the position from the field if it doesn't fit
            if not any([num in r for r in ranges]):
                if pos in fields[name]:
                    fields[name].remove(pos)

# do the thing
donePos = []
change = True
while change:
    change = False

    for name, vals in fields.items():
        # update donePos
        for val in vals:
            if val not in donePos and len(vals) == 1:
                donePos.append(val)
                change = True
        
        # update fields
        for pos in donePos:
            if pos in vals and len(vals) != 1:
                fields[name].remove(pos)
                change = True

depPos = [pos[0] for field, pos in fields.items() if 'departure' in field]
depNums = [yours[pos] for pos in depPos]

print(f'Product of departure numbers = {prod(depNums)}')
