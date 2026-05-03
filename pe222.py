
import math
from itertools import permutations


def baseline_height(w, r0, r1):
    return math.sqrt((r0+r1)**2 - (w - r0 - r1)**2)

def full_height(w, r0, r1):
    return baseline_height(w, r0, r1) + r0 + r1

def chain_baseline_height(w, radii):
    height = 0
    for i in range(1, len(radii)):
        height += baseline_height(w, radii[i-1], radii[i])
    return height

def chain_full_height(w, radii):
    return chain_baseline_height(w, radii) + radii[0] + radii[-1]

#The order of the radii matters
#Question: does a greedy search on savings work?
#Uncorked height is different than corked 

for N in range(49, 45, -1):
    best_height = 10**12
    best_perm = None
    for perm in permutations(range(N,51)):
        height = chain_full_height(50*2, perm)
        if height < best_height:
            best_height = height
            best_perm = perm
    print(N, best_height, best_perm)
    # Has a symetry counting up with a parity then down with the other parity

w = 50*2
radii = list(range(49, 29, -2)) + list(range(30, 51, 2))
print(radii)
print(chain_full_height(w, radii)*1_000)

#1547952 INCORRECT
#1548951 INCORRECT
#1590933 CORRECT

#Try a swapping search, assumes no local minima
#THIS DOES NOT WORK
"""
best_height = 10**12
best_radii = None
radii = list(range(30, 51))
found_better = True
while found_better:
    found_better = False
    for i in range(len(radii)-1):
        for j in range(i+1, len(radii)):
            new_radii = radii.copy()
            new_radii[i], new_radii[j] = new_radii[j], new_radii[i]
            height = chain_full_height(w, new_radii)
            if height < best_height:
                best_height = height
                best_radii = new_radii
                found_better = True
print(best_radii)
print(chain_full_height(w, best_radii)*1_000)
"""