#########################
# day 15
#########################

from time import perf_counter as pc

# numbers = [0, 3, 6]
# numbers = [1, 3, 2]
# numbers = [2, 1, 3]
# numbers = [1, 2, 3]
# numbers = [2, 3, 1]
# numbers = [3, 2, 1]
# numbers = [3, 1, 2]
numbers = [18, 8, 0, 5, 4, 1, 20]

# say the numbers
ages = {n:i+1 for i, n in enumerate(numbers)}

t0 = pc()
prev = numbers[-1]
# for turn in range(len(numbers)+1, 2020+1):    # part 1
for turn in range(len(numbers)+1, 30000000+1):  # part 2

    # if new number, say 0
    if prev not in ages or turn == len(numbers) + 1:
        ages[prev] = turn - 1
        prev = 0
    # old number, say age
    else:
        prevAge = turn - 1 - ages[prev]
        ages[prev] = turn - 1
        prev = prevAge

print(f'final val: {prev}')
print(f'took {pc() - t0}!')