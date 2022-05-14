#!/usr/bin/env python
# day03.py

import numpy as np

with open("./input/day03", 'r') as file:
    data = [list(line.strip().split()[0]) for line in file.readlines()]
    data = np.array([[int(n) for n in line] for line in data])

# Part 1
means = np.mean(data, axis=0)
gamma = [1 if n > 0.5 else 0 for n in means]
epsilon = [1 if n < 0.5 else 0 for n in means]

gamma_rate = ''.join([str(g) for g in gamma])
epsilon_rate = ''.join([str(e) for e in epsilon])

print(f'Part 1: {int(gamma_rate, 2) * int(epsilon_rate, 2)}')

# Part 2
n, n_bits = data.shape
ox_mask = np.ones(n, dtype=bool)
co2_mask = np.ones(n, dtype=bool)
do_ox = True
do_co2 = True
for i_bit in range(n_bits):
    if np.count_nonzero(ox_mask) == 1:
        do_ox = False
    if np.count_nonzero(co2_mask) == 1:
        do_co2 = False

    if do_ox:
        ox_mean = np.mean(data[ox_mask,i_bit])
        ox_bit = 1 if ox_mean >= 0.5 else 0
        ox_mask &= data[:,i_bit] == ox_bit
    if do_co2:
        co2_mean = np.mean(data[co2_mask,i_bit])
        co2_bit = 1 if co2_mean < 0.5 else 0
        co2_mask &= data[:,i_bit] == co2_bit

    # print(data[ox_mask], end='\n\n')

ox_rating = data[ox_mask].flatten()
co2_rating = data[co2_mask].flatten()

ox_rating = ''.join([str(o) for o in ox_rating])
co2_rating = ''.join([str(c) for c in co2_rating])

print(ox_rating, co2_rating)
print(f'Part 2: {int(ox_rating, 2) * int(co2_rating, 2)}')