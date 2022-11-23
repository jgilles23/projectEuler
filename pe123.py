import sympy

N = 10**10

max_p = 5 * N**0.5
for i, p in enumerate(sympy.primerange(1, max_p)):
    n = i + 1
    r = (pow(p-1, n, p**2) + pow(p+1, n, p**2)) % p**2
    if r > N:
        print("n", n, "r", r)
        break