
import sympy
import math
from itertools import product

N = 25_000_000

brute = N <= 10_000
if brute:
    ans = 0
    brute_set = set()
    for a in range(1, N//3 + 1):
        if a % 2_000 == 0:
            print(f"Brute Progress: {a:,}/{N//3:,}, current ans: {ans}")
        for b in range(a, N):
            c = math.isqrt(a**2 + b**2 - 1)
            C = math.sqrt(c**2 + 1)
            if b < a or C < b:
                continue
            if a + b <= C:
                continue
            if a + b + C > N:
                continue
            if a**2 + b**2 == c**2 + 1:
                brute_set.add((a, b, c))
                ans += 1
    print("Brute ans", ans)

def brute_force(c):
    count = 0
    a_max = math.isqrt((c**2 + 1)//2)
    for a in range(1, a_max+1):
        b_implied = math.isqrt(c**2 + 1 - a**2)
        if a + b_implied <= c+1:
            continue
        if a**2 + b_implied**2 == c**2 + 1:
            count += 1
    return count

def recursive_split(remaining_factors, x, y):
    if not remaining_factors:
        yield x, y
    else:
        remaining_factors_copy = remaining_factors.copy()
        p, multiplicity = remaining_factors_copy.popitem()
        for x_p in range(multiplicity+1):
            y_p = multiplicity - x_p
            yield from recursive_split(remaining_factors_copy, x * (p**x_p), y * (p**y_p))


def by_factor_decomposition(am1_factors, ap1_factors, x_base, y_base):
    combined_factors = am1_factors | ap1_factors
    # print(combined_factors)
    solution_count = 0
    for x, y in recursive_split(combined_factors, x=x_base, y=y_base):
        #print(f"x: {x}, x_factors: {x_factors}, y: {y}, y_factors: {y_factors}")
        #Test if the x & y are consistent with the triangle construction
        if x > y:
            continue
        b = (y-x)//2
        c = (y+x)//2
        if a > b or b > c + 1:
            continue
        if a + b <= c:
            continue
        if a + b + c >= N:
            continue
        if a**2 + b**2 == c**2 + 1:
            solution_count += 1
            # print(f"Found solution: a: {a}, b: {b}, c: {c}")
        else:
            continue
    return solution_count

# ans = 0
# a_start = 2
# am1_factors = sympy.factorint(a_start - 2)
# a_factors = sympy.factorint(a_start - 1)
# ap1_factors = sympy.factorint(a_start - 0)
# for a in range(a_start, (N+1)//3 + 1):
#     if a % 10000 == 0:
#         print(f"Progress: {a:,}/{(N+1)//3:,}, current ans: {ans}")
#     am1_factors = a_factors
#     a_factors = ap1_factors
#     divisor = 2 if (a+1) % 2 == 0 else 1
#     ap1_factors = sympy.factorint((a+2)//divisor)
#     ans += by_factor_decomposition(am1_factors, ap1_factors, x_base=divisor, y_base=divisor)
# print(ans)
# ans0 = ans
    

ans = 0
a_max = int(N/3.4)
factor_sets = [[] for _ in range(a_max+2)]
for p in range(2, a_max+2):
    if math.log2(p) % 1 == 0:
        print(f"Factoring Progress: {p:,}/{a_max:,}")
    if len(factor_sets[p]) == 0:
        e = 1
        for j in range(p, a_max+2, p):
            factor_sets[j].append([1])
        while p**e <= a_max:
            for j in range(p**e, a_max+2, p**e):
                factor_sets[j][-1].append(p**e)
            e += 1
print("Finished Factoring.")
ans = 0
for a in range(3, a_max+1):
    factor_2 = 2 if (a+1) % 2 == 0 else 1
    if a % 100_000 == 0:
        print(f"Progress: {a:,}/{a_max:,}, current ans: {ans}")
    for factors in product(*factor_sets[(a-1)//factor_2], *factor_sets[(a+1)//factor_2]):
        x = math.prod(factors)*factor_2
        y = (a-1)*(a+1)//x
        if x > y:
            continue
        b = (y-x)//2
        c = (y+x)//2
        C = math.sqrt(c**2 + 1)
        if a > b or b > C:
            continue
        if a + b <= C:
            continue
        if a + b + C > N:
            continue
        if a**2 + b**2 == c**2 + 1:
            if brute:
                brute_set.remove((a, b, c))
            ans += 1
        else:
            raise Exception(f"ERROR: Found invalid solution with a: {a}, b: {b}, c: {c}")
print("Finished counting.")
print(ans)
print("Rounding out side length 1")
ans += N//2 - 1
print(ans)
# print(ans0, ans)

# #trying again but just using built in divisors function, which is very fast in sympy
# ans = 0
# a_max = int(N/3.4)
# for a in range(3, a_max+1):
#     factor_2 = 2 if (a+1) % 2 == 0 else 1
#     if a % 100_000 == 0:
#         print(f"Progress: {a:,}/{a_max:,}, current ans: {ans}")
#     for x in sympy.divisors((a-1)//factor_2*(a+1)//factor_2):
#         x *= factor_2
#         y = (a-1)*(a+1)//x
#         if x > y:
#             break
#         b = (y-x)//2
#         c = (y+x)//2
#         if a > b or b > c + 1:
#             continue
#         if a + b <= c + 1:
#             continue
#         if a + b + c >= N:
#             continue
#         if a**2 + b**2 == c**2 + 1:
#             if brute:
#                 brute_set.remove((a, b, c))
#             ans += 1
#         else:
#             raise Exception(f"ERROR: Found invalid solution with a: {a}, b: {b}, c: {c}")
# print(ans)

# if brute:
#     for triple in brute_set:
#         print(f"ERROR: Triple {triple} was found in brute force but not in optimized code.")


#wrong answer for 25M is 49114849
#61614848 right!