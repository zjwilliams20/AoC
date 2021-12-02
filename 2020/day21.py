#########################
# day 21
#########################

import re

with open('input/day21', 'r') as file:
    foods = [line.strip() for line in file.readlines()]

raw = {}
allIngreds = []
for food in foods:
    allergens = re.search(r'\(([^)]+)', food)
    allergens = allergens.group(1)[8:].strip().split(', ')
    ingreds = set(food.split('(')[0].split())

    # keep track of ingredients
    allIngreds.append(list(ingreds))

    # build ingredient/allergen dictionary
    for allergen in allergens:
        if allergen not in raw:
            raw[allergen] = [ingreds]
        else:
            raw[allergen].append(ingreds)

# only keep duplicates for each allergen
fda = raw.copy()
for allergen, ingreds in fda.items():
    fda[allergen] = list(set.intersection(*ingreds))

# remove the rest to complete fda
while not all([isinstance(i, str) for i in fda.values()]):

    for allergen, ingreds in fda.items():
        # ingredient already matched, remove from other ingredient lists
        if isinstance(ingreds, str):
            for allergen2, ingreds2 in fda.items():
                if ingreds in ingreds2 and ingreds != ingreds2:
                    ingreds2.remove(ingreds)
        # new ingredient matched
        if len(ingreds) == 1:
                fda[allergen] = fda[allergen][0]

# count occurrences of non-allergenic ingredients
nGood = sum([i not in fda.values() for ingred in allIngreds for i in ingred])
print(f'part 1: {nGood}')

# part 2
alphaIngreds = ','.join([fda[allergen] for allergen in sorted(fda.keys())])
print(f'part 2: "{alphaIngreds}"')