#Project euler 70, date 20210503
import numpy as np

#phi(n) = n*product[(1 - 1/p)] where p are the distinct prime numbers dividing n

N = 10**7

def unique_factor_up_to(n):
    factors = [[] for _ in range(n)]
    for i in range(2,n):
        if not factors[i]:
            for j in range(i,n,i):
                factors[j].append(i)
    return factors
A = unique_factor_up_to(N)
print("Factors found")

phis = [0,1]
for n in range(2,N):
    phi = n
    for f in A[n]:
        phi = phi*(1 - 1/f)
    phis.append(int(phi))
print("phis found")

def sort_int(x):
    y = [i for i in str(x)]
    y.sort()
    return "".join(y)

permutations = []
#Find permuations, save as ordered tuple (n/phi(n), n, phi(n))
for n, phi in enumerate(phis):
    if n < 2:
        continue
    if sort_int(n) == sort_int(phi):
        permutations.append((n/phi, n, phi))
print("# permutations",len(permutations))

#Find minimum ratio
print("ans",min(permutations))




