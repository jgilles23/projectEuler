import numpy as np

increasing_lookup = [np.full(10,1)]


E = 3
for i in range(E):
    increasing_lookup += [np.full(10,0)]
    for j in range(10):
        increasing_lookup[-1][j] = np.sum(increasing_lookup[-2][j:])
for a in increasing_lookup:
    print(a)
print("num bouncy", (10**E - 1) - (np.sum(increasing_lookup[-1][0])*2 - 10 - 1))