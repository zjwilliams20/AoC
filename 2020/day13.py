#########################
# day 13
#########################

import math
import numpy as np

def arr_lcm(arr):
    lcm = arr[0]
    for i in arr[1:]:
        lcm = lcm*i//math.gcd(lcm, i)
    return lcm

def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")
    
    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase

with open('input/day13', 'r') as file:
    wait = int(file.readline())
    buses = file.readline().strip().split(',')
    buses = np.array([int(bus) if bus != 'x' else 0 for bus in buses])

# part 1
busIDs = buses[buses != 0]
waitTimes = []
for bus in busIDs:
    reps = wait // bus
    time = bus * (reps+1) - wait
    waitTimes.append(time)

chooseInd = waitTimes.index(min(waitTimes))
chooseWait = waitTimes[chooseInd]
chooseBus = buses[chooseInd]
print(f'{chooseWait} * {chooseBus} = {chooseWait * chooseBus}')

# part 2
# test examples:
# buses = np.array([17, 0, 13, 19])
# buses = np.array([67, 7, 59, 61])
# buses = np.array([67,0,7,59,61])
# buses = np.array([67,7,0,59,61])
# buses = np.array([1789,37,47,1889])
# busIDs = buses[buses != 0]

busInd = np.arange(len(buses))
busInd = busInd[buses != 0]

# initialize phase rotation of first bus
p_a, phi_a = busIDs[0], -busInd[0]

# combine phase rotations of all except last bus, because doing all 9
#   in the input causes scalar overflow (no overflow in the examples, 
#   the answer is just the final phase.)
for i, bus in enumerate(busIDs[1:-2]):
    p_b, phi_b = bus, -busInd[i+1]
    p_c, phi_c = combine_phased_rotations(p_a, phi_a, p_b, phi_b)
    p_a, phi_a = p_c, phi_c

print(f'combined period: {p_c}\tcombined phase: {phi_c}')

# manually search for intersection with the last bus by looking through 
#   each combined period, starting at the combined phase
ts = phi_c
winner = False
while not winner:
    if all((ts + busInd) % busIDs == 0):
        winner = True
    ts += p_c

print(f'WE HAVE A WINNER!! {ts-p_c-busInd[0]}')
