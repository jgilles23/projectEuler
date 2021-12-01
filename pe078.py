import numpy as np
import pandas as pd
import time
N = 10**5

"""
start = time.time()
A = np.full((N,N), 0)
print("made")
ceil = lambda x: int(np.ceil(x))
for n in range(1,N):
    for m in range(ceil(n/2), n):
        A[n,n-m] = sum(A[m, n-m:])%10**6
    A[n,n] = 1
    #Test if done
    if A[n,1] == 0:
        print("found answer at", n-1)
#print(A)
print(time.time() - start)
"""

start = time.time()
B = np.full((N,N//2+1),1)
print("made")
B[1,1] = 1
B[2,1] = 2
B[3,1] = 3
B[3,2] = 2
for n in range(4,N):
    if (n%100)==0:
        print(n)
    B[n,n//2] = 2
    for m in range(n//2-1, 0, -1):
        B[n,m] = (B[n,m+1] + B[n-m,m])%(1000000)
    if B[n,1] == 0:
        print("ans", n+1, B[n,1])
        break
#print(B)
print(time.time() - start)