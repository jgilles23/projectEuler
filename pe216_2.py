import sympy

N = 50_000_000

prime_count = 0
for n in range(1, N+1):
    if n % 1_000_000 == 0:
        print(f"n: {n:,}, prime count: {prime_count}")
    t = 2*n**2 - 1
    if sympy.isprime(t):
        prime_count += 1
print(prime_count)