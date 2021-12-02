#########################
# day 25
#########################

with open('input/day25', 'r') as file:
    door_public = int(file.readline().strip())
    card_public = int(file.readline().strip())


def loopsize(n, subj, m):
    cache, i = subj, 1
    while cache != n:
        cache = (cache * subj) % m
        i += 1
    return i
    

subj = 7
m = 20201227

door_loop_sz = loopsize(door_public, subj, m)
card_loop_sz = loopsize(card_public, subj, m)

key1 = pow(card_public, door_loop_sz, m)
key2 = pow(door_public, card_loop_sz, m)
assert key1 == key2

print(f'Part 1: {key1}')