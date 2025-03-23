'''
PE211
1 > every 1th slot with the value in the 1th slot (except 1^2 where it only goes once)
2 > every 2nd slot with the value in the 2th slot (except 2^2 where it only goes once)
[ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1]
[ *,  2,  3,  4,  5,  6,  7,  8,  9, 10]
[ 0,  0,  0,  2,  0,  2,  0,  2,  0,  2]
[ 0,  0,  0,  *,  0,  3,  0,  4,  0,  5]
[ 0,  0,  0,  0,  0,  0,  0,  0,  3,  0]
[ 0,  0,  0,  0,  0,  0,  0,  0,  *,  0]
'''
import numpy as np
import math

N = 64*(10**6)
allN = np.zeros(N, int)

for n in range(1, math.isqrt(N)+1):
    if n%500 == 0:
        print(n)
    allN[n**2::n] += n**2
    allN[(n**2+n)::n] += np.arange(n+1, math.ceil(N/n))**2

print("Calculating sum")
ans = 0
for n in range(1,N):
    if math.isqrt(allN[n])**2 == allN[n]:
        ans += n
print("ans", ans)