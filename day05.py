#########################
# day 5
#########################

import csv

# load data
passes = []
with open("input/day5", 'r') as file:
    reader = csv.reader(file, delimiter='\n')
    passes = [line[0] for line in reader]

# part 1
seatID = [0]*len(passes)
binCast = [['F', 'B', 'L', 'R'], ['0', '1', '0', '1']]
for idx, p in enumerate(passes):
    for i in range(0, len(binCast[0])):
        p = p.replace(binCast[0][i], binCast[1][i])
    row, col = int(p[:7], 2), int(p[7:], 2)
    seatID[idx] = row * 8 + col

print(f"Highest seatID found ---> {max(seatID)}")

# part 2
prev = 0
for idx, seat in enumerate(sorted(seatID)):
    if idx <= 2:
        continue
    elif idx >= len(seatID) - 3:
        break
    if (seat - prev) == 2:
        print(f"Found an empty seat! {seat, prev}")
    prev = seat
