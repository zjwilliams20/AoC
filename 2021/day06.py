#!/usr/bin/env python
# day06.py

from time import perf_counter as pc
from collections import Counter

# fish = [3,4,3,1,2] # test
with open('2021/input/day06') as file:
    fish = list(map(int, file.readline().strip().split(',')))

n_days = 80
NEW_AGE = 8
RESET_AGE = 6

def advance_day(fish):
    """Advance the fish generation by changing their ages manually."""
    
    n_babies = fish.count(0)
    # fish = deque(map(lambda n: n-1 if n else RESET_AGE, fish))
    fish = list(map(lambda n: n-1 if n else RESET_AGE, fish))
    fish.extend([NEW_AGE]*n_babies)
    return fish

def advance_generation(fish, n_days=RESET_AGE):
    """Advance the fish generation using the moduli of their reset age."""
    assert n_days <= RESET_AGE

    if n_days == 0:
        return fish

    babies = []
    for i, f in enumerate(fish):
        fish[i] = (f - n_days) % (RESET_AGE + 1)
        has_baby = abs((f - n_days) // (RESET_AGE + 1)) > 0
        if has_baby:
            babies.append(NEW_AGE - (RESET_AGE - fish[i]))
    new_fish = fish + babies
    return new_fish

def advance_day_count(cnt):
    """Advance the population by counting the numbers of fish."""

    n_babies = cnt[0]
    for age in sorted(list(cnt)):
        if age >= 1:
            cnt[age-1] = cnt[age]
            cnt[age] = 0
    cnt[NEW_AGE] = n_babies
    cnt[RESET_AGE] += n_babies
    return cnt

# n_days = 80 # part 1
n_days = 256 # part 2
t0 = pc()

# for day in range(n_days):
#     fish = advance_day(fish) Attempt 1 

# Attempt 2
# Handle first number of iterations to fit n_days within modulus.
# n_init_days = n_days % RESET_AGE
# print(n_init_days)
# fish = advance_generation(fish, n_init_days)
# for day in range(n_init_days, n_days, RESET_AGE):
#     fish = advance_generation(fish)
# n_fish = len(fish)

# Attempt 3
cnt = Counter(fish)
for day in range(n_days):
    cnt = advance_day_count(cnt)
n_fish = sum(cnt.values())

print(f'Counted {n_fish} fish. Took {pc() - t0:.3g} seconds')

