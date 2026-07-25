from sympy import primerange

n = 20 * 10**6
k = 15 * 10**6

def factorial_factor_count(n):
    count = {}
    for p in primerange(2, n + 1):
        e = 1
        while p**e <= n:
            count[p] = count.get(p, 0) + n // (p**e)
            e += 1
    return count

def factor_count_divide(A, B):
    C = {}
    for p, a in A.items():
        b = B.get(p, 0)
        if a < b:
            raise Exception(f"Factor count of {p} in A is less than in B: {a} < {b}")
        C[p] = a - b
    return C

def sum_factor_count(A):
    s = 0
    for p, a in A.items():
        s += p*a
    return s

A = factorial_factor_count(n)
print("A sum", sum_factor_count(A))
B = factorial_factor_count(k)
print("B sum", sum_factor_count(B))
C = factorial_factor_count(n-k)
print("C sum", sum_factor_count(C))

D = factor_count_divide(A, B)
print("D sum", sum_factor_count(D))
E = factor_count_divide(D, C)
ans = sum_factor_count(E)
print("ans", ans)
