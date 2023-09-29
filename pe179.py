# %%
import sympy

#%%
N = 10**7

count = 0
previous_divisors = 0
for n in range(1, N):
    if n % 10**5 == 0:
        print("n:", n, "count:", count)
    divisors = sympy.ntheory.divisor_count(n)
    if divisors == previous_divisors:
        count += 1
    previous_divisors = divisors

print("ans", count)