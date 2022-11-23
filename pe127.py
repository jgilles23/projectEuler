import sympy
import math

N = 1000

primes = sympy.primerange(N)
factors = [set() for _ in range(N)]
for i in primes:
    for j in range(i,N,i):
        factors[j].add(i)
print("factors generated")

sum_c = 0
for c in range(N):
    for a in range(1, int(math.ceil(c/2))):
        b = c - a
        #Test if coprime
        if factors[a] & factors[b]:
            continue
        if factors[a] & factors[c]:
            continue
        if factors[b] & factors[c]:
            continue
        #Test overall radical
        u = factors[a].union(factors[b]).union(factors[c])
        rad = math.prod(u)
        if rad >= c:
            continue
        #This is an abc hit
        # print("abc hit", (a,b,c))
        sum_c += c
print("sum_c", sum_c)
