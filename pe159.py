import numpy as np

N = 10**6

def single_digital_root(x):
    return sum([int(y) for y in str(x)])

def recursive_digital_root(x):
    while x >= 10:
        x = single_digital_root(x)
    return x

def quick_digital_root(x):
    return (x-1)%9 + 1

digital_root = np.arange(N)
digital_root = (digital_root-1)%9 + 1

# Store the maximum digital root sum of each number
mdrs = np.full(N, 0)

def recursive_factor_buildup(n=1, drs=0, smallest_factor=2, max_n=N, mdrs=mdrs):  
    # Add the next factor
    for next_factor in range(smallest_factor, N):
        next_n = n*next_factor
        next_drs = drs + quick_digital_root(next_factor)
        # Check if too large
        if next_n >= max_n:
            break
        # Add a new maximum drs
        if mdrs[next_n] < next_drs:
            mdrs[next_n] = next_drs
        # Recursive call
        recursive_factor_buildup(next_n, next_drs, next_factor, max_n, mdrs)

recursive_factor_buildup()
ans = sum(mdrs)
print("ans", ans)