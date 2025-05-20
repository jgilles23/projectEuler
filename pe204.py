'''
PE204 - Genralized Hamming Numbers
Generalized hamming number of type 5
Generalized hamming numbers of type 100 which are less than 10**9

2,3,5
2*3*5 = 30
1,2,3,4,5,6,8,9,10,12,15
16,18,20,
'''

import numpy as np
import math

def brute(N, H):
    nonHamming = np.full(N + 1, False, dtype=bool)
    primes = np.full(N+1, True, dtype=bool)
    print("arrays created")

    for n in range(2,len(primes)):
        if primes[n] == True:
            primes[2*n::n] = False
            if n > H:
                nonHamming[n::n] = True

    print("hamming numbers calculated")
    ans = len(nonHamming) - np.sum(nonHamming) - 1 #To account for 0
    print("ans:", ans)

    # for i in range(1, len(nonHamming)):
    #     print(i, ":", nonHamming[i], primes[i])

N = 10**9 #Up to number of size N
H = 100 #Hamming numbers of type H

primesH = []
for h in range(2, H+1):
    for i in range(2, math.isqrt(h) + 1):
        if h % i == 0:
            break
    else:
        primesH.append(h)

print("primes:", primesH)

hammingNumbers = np.full(N + 1, False, dtype=bool)
hammingNumbers[1] = True #1 is a hamming number
for n in range(len(hammingNumbers)):
    if n%10**6 == 0:
        print(n)
    if hammingNumbers[n]:
        for p in primesH:
            m = n * p
            if m <= N:
                hammingNumbers[m] = True
            else:
                break
print("hamming numbers:", hammingNumbers)
print("ans", np.sum(hammingNumbers))

