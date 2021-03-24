#########################
# day 1
#########################

import numpy as np

# load data
with open("./input/day1", 'r') as file:
    data = np.fromfile(file,sep='\n')

# find the 2020 addends
# part 1
for i in range(0,len(data)):
    for j in range(i+1,len(data)):
        if data[i] + data[j] == 2020:
            print("We have a winner!!")
            print(f"\t{data[i]:0.0f}+{data[j]:0.0f}={data[i]+data[j]:0.0f}")
            print("\nAnswer:")
            print(f"\t{data[i]:0.0f}*{data[j]:0.0f}={data[i]*data[j]:0.0f}")

# part 2
for i in range(0,len(data)):
    for j in range(0,len(data)):
        for k in range(0,len(data)):
            if i == j or j == k or k == i:
                continue
            if data[i] + data[j] + data[k] == 2020:
                print("We have a winner!!")
                print(f"\t{data[i]:0.0f}+{data[j]:0.0f}+{data[k]:0.0f}={data[i]+data[j]+data[k]:0.0f}")
                print("\nAnswer:")
                print(f"\t{data[i]:0.0f}*{data[j]:0.0f}*{data[k]:0.0f}={data[i]*data[j]*data[k]:0.0f}")
