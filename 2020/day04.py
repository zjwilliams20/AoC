#########################
# day 4
#########################

import csv
import re

categories = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
formats = [':\d{4}(\s|\Z)', ':\d{4}(\s|\Z)', ':\d{4}(\s|\Z)', ':\d+((cm)|(in))(\s|\Z)', \
           ':#[\da-f]{6}(\s|\Z)', ':((amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth))(\s|\Z)', \
           ':\d{9}(\s|\Z)']
years = [lambda x: 1920 <= x <= 2002, \
         lambda x: 2010 <= x <= 2020, \
         lambda x: 2020 <= x <= 2030]

class Passport():
    def __init__(self, passStr):
        self.passStr = passStr
    def isOkay(self):
        for cat in categories:
            if cat not in self.passStr:
                return False
        return True
    def isValid(self):
        valid = [False] * len(categories)
        for idx, cat in enumerate(categories):
            if cat not in self.passStr:
                return False
            else:
                # print(cat, idx)
                match = re.search(cat + formats[idx], self.passStr)
                if match:
                    if 0 <= idx <= 2:
                        year = int(match.group().split(':')[1])
                        valid[idx] = years[idx](year)
                    elif idx == 3:
                        meas = match.group().split(':')[1]
                        # print(meas)
                        if 'cm' in meas:
                            hgt = int(meas.replace('cm', ''))
                            valid[idx] = 150 <= hgt <= 193
                        elif 'in' in meas:
                            hgt = int(meas.replace('in', ''))
                            valid[idx] = 59 <= hgt <= 76
                        else:
                            print("something went wrong...")
                    else:
                        valid[idx] = True
        print(valid)
        return all(valid)
    def __repr__(self):
        return self.passStr

# load data
raw = []
with open("input/day4", 'r') as file:
    reader = csv.reader(file, delimiter='\n')
    raw = [line for line in reader]

# parse for passports
nPass = 0
rawPassports = ['']
for i, line in enumerate(raw):
    if line:
        rawPassports[nPass] += ' ' + line[0]
    else:
        nPass += 1
        rawPassports.append('')
passports = [Passport(pp) for pp in rawPassports]

# part 1 
nValid = 0
for p in passports:
    nValid += p.isOkay()
print(f"Counted {nValid} okay passports!")

# part 2
nValid = 0
for p in passports:
    nValid += p.isValid()
print(f"Counted {nValid} valid passports!")
