# %%
import numpy as np

N = 10**8

doublet_count = 0
prime_factors_count = np.full(N, 0)
for i in range(2, N):
    if i % 10**6 == 0:
        print(i)
    if prime_factors_count[i] == 0:
        # Found a prime
        e = 1
        while (j := i**e) < N:
            prime_factors_count[j:N:j] += 1
            e += 1
    elif prime_factors_count[i] == 2:
        doublet_count += 1
print("ans", doublet_count)

# %%
