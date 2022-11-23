import math
import itertools

T = 15

numerator = 0
denominator = math.prod(range(2,T+2))
blue_required = T//2 + 1
for r in range(blue_required, T + 1):
    for perm in itertools.combinations(range(2,T+2), T-r):
        n = 1
        for p in perm:
            n = n * (p-1)
        # print(perm, n)
        numerator += n

print(numerator, "/", denominator, numerator/denominator)
print("ANS", denominator//numerator)