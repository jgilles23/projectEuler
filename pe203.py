#PE203
import sympy
import math

target_rows = 51

pascal = [[1]]
for i in range(1, target_rows):
    pascal.append([1] + [a + b for a, b in zip(pascal[i-1][:-1], pascal[i-1][1:])] + [1])
    # print(pascal[i])

unique = set()
for row in pascal:
    for item in row:
        unique.add(item)
print("unique", len(unique))

biggest = max(unique)
primes = list(sympy.primerange(1,math.isqrt(biggest) + 1))
squarefree = []
for n in unique:
    for p in primes:
        if n % (p**2) == 0:
            break
        if p**2 > n:
            squarefree.append(n)
            break
    else:
        squarefree.append(n)

print("squarefree", len(squarefree))
ans = sum(squarefree)
print("ans", ans)
print(squarefree)
