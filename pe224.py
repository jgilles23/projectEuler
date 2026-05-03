import math
import sympy

N = 75_000_000

def brute(N):
    ans = 0
    for a in range(1, N//3 + 1):
        for b in range(a, N):
            c = math.isqrt(a**2 + b**2 + 1)
            C = math.sqrt(c**2 - 1)
            if b < a or C < b:
                continue
            if a + b <= C:
                continue
            if a + b + C > N:
                continue
            if a**2 + b**2 == c**2 - 1:
                ans += 1
                # print(f"Found triple: {a}, {b}, {c}")
    return ans

if N <= 10_000:
    print("Brute ans", brute(N))

def test1(N):
    ans = 0
    allowed_c = set()
    for c in range(1, N//2 + 1, 2):
        if c % 10_000 == 1:
            print(f"Test1 Progress: {c:,}/{N//2:,}, current ans: {ans}")
        if c == 1: c = 2
        factor_multiplicity = sympy.factorint(c**2 - 1)
        for factor, multiplicity in factor_multiplicity.items():
            multiplicity = multiplicity % 2
            if multiplicity == 0:
                continue
            elif factor == 2:
                continue
            elif factor % 4 == 1:
                continue
            else:
                #Not a valid factorization
                break
        else:
            #for loop completed without break, so we have a valid factorization
            #Test if the c is valid
            allowed_c.add(c)
            for b in range(1, c):
                a = math.isqrt(c**2 - 1 - b**2)
                if a < 1 or a > b:
                    continue
                elif a + b <= c:
                    continue
                elif a + b + c > N:
                    continue
                elif a**2 + b**2 == c**2 - 1:
                    # print(f"Found triple: {a}, {b}, {c}")
                    ans += 1
    return ans, allowed_c

if N <= 100_000:
    ans, allowed_c = test1(N)
    print("Test1 ans", ans)

# def CRT_combine(solutions, moduli):
#     #Subcessivly combine the solutions of CRT using
#     #x = a (mod n), x = b (mod m)
#     #x = b*m_inv_n*m + a*n_inv_m*n (mod m*n)
#     a = solutions[0]
#     m = moduli[0]
#     for b, n in zip(solutions[1:], moduli[1:]):
#         a = (b*pow(m, -1, n)*m + a*pow(n, -1, m)*n) % (m*n)
#         m *= n
#     return a

# m, n = 25, 101
# A = [7, 18]
# B = [10, 91]
# for a in A:
#     for b in B:
#         x = (b*pow(m, -1, n)*m + a*pow(n, -1, m)*n) % (m*n)
#         print(f"Found x: {CRT_combine([a, b], [m, n])} for a: {a}, b: {b}")

#let's see how quickly we can reduce the search space for c
import numpy as np
alpha_flag = np.full(N//4 + 1, True, dtype=bool)
for p in sympy.primerange(3, N//4 + 1):
    if p % 4 == 1:
        continue
    extract = np.full(len(alpha_flag[::p]), False, dtype=bool)
    e = 2
    while p**e <= N//4:
        extract[p**(e-1)::p**(e-1)] = (e % 2 == 0)
        e += 1
    alpha_flag[::p] = alpha_flag[::p] & extract

print(f"Compiled all allowable alpha values up to {N//4:,}")

ans = 0
c_count = 0
for c in range(3, N//2 + 1, 2):
    if c%10_000 == 1:
        print(f"Test2 Progress: {c:,}/{N//2:,}, current ans: {ans}")
    alpha = (c-1)//2
    allowed = alpha_flag[alpha] and alpha_flag[alpha + 1]
    if allowed:
        c_count += 1
        C = (c-1)//2
        for A in range(1, C + 1):
            B = math.isqrt(C**2 + C - A**2)
            a = 2*A
            b = 2*B
            if a < 1 or a > b:
                continue
            elif a + b <= c:
                continue
            elif a + b + c > N:
                continue
            elif a**2 + b**2 == c**2 - 1:
                # print(f"Found triple: {a}, {b}, {c}")
                ans += 1
print(f"Found {c_count:,} allowed c values up to {N//2:,}")
print("Test2 ans", ans)