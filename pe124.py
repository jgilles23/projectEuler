import numpy as np
import sympy

N = 100000
i = 10000

rad = np.full(N+1, 1)

for p in sympy.primerange(1, N+1):
    rad[p::p] *= p

ind = np.argsort(rad, kind="stable")
print("ans", ind[i])

for j in range(i-5, i+5):
    print(j, ":", ind[j], rad[ind[j]])
