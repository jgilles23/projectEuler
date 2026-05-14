import math
import numpy as np

from sympy import re

N = 100

lookup = {}
lookup_T = {}

def recurse_A_first(A, B):
    #Assumes that A takes the first move
    return 0.5*recurse(A+1, B) + 0.5*recurse(A, B) #pass, fail

def recurse(A, B):
    #Assumes that B takes the first move
    if B >= N:
        return 1.0
    elif A >= N:
        return 0.0
    if (A, B) in lookup:
        return lookup[(A, B)]
    best_grade, best_T = 0.0, 0
    T = 0
    while B + 2**(T-1) <= N:
        T += 1
        x = ((0.5)*(0.5**T)*recurse(A+1, B+2**(T-1)) + #pass, pass
             (0.5)*(1 - 0.5**T)*recurse(A+1, B) + #pass, fail
             (0.5)*(0.5**T)*recurse(A, B+2**(T-1))) #fail, pass
        x = x / (1 - (0.5)*(1 - 0.5**T)) #fail, fail
        if x > best_grade:
            best_grade, best_T = x, T
    lookup[(A, B)] = best_grade
    lookup_T[(A, B)] = best_T
    return best_grade


ans = recurse_A_first(0, 0)
print("recurse_A_first(0, 0):", ans)
print("N:", N, "ans:", round(ans, 8))

#0.60177778 wrong
#0.83587213 wrong
#0.83648556 correct

# for A in range(N):
#     for B in range(N):
#         print(lookup_T[(A, B)], end="")
#     print()

def decompose(index):
    A, B = index // N, index % N
    return A, B

def yield_grid_T():
    grid_T = np.ones((N, N), dtype=np.int32)
    index = 0
    while True:
        if index == 0:
            yield grid_T
        A, B = decompose(index)
        grid_T[A, B] += 1
        if grid_T[A, B] > math.ceil(math.log2(N - B) + 1):
            index += 1
            if index >= N*N:
                return
        else:
            for j in range(index):
                A_j, B_j = decompose(j)
                grid_T[A_j, B_j] = 1
            index = 0
        

        

def run_grid(grid_T, starting_A=0, starting_B=0):
    grid = np.zeros((N+1, N+1), dtype=np.float64)
    grid[starting_A, starting_B] = 1.0
    A_win_prob = 0
    B_win_prob = 0
    while A_win_prob + B_win_prob < (1 - 10**-12):
        #Start with all A
        new_grid = np.zeros_like(grid, dtype=np.float64)
        for a in range(N):
            for b in range(N):
                new_grid[a, b] += grid[a, b] * 0.5
                new_a, new_b = a + 1, b
                new_grid[new_a, new_b] += grid[a, b] * 0.5
        A_win_prob += new_grid[N, :].sum()
        grid = new_grid
        #Now do B winning
        new_grid = np.zeros_like(grid, dtype=np.float64)
        for a in range(N):
            for b in range(N):
                T = grid_T[a, b]
                new_grid[a, b] += grid[a, b] * (1 - 0.5**T)
                new_a, new_b = a, b + 2**(T-1)
                if new_b >= N:
                    new_b = N
                new_grid[new_a, new_b] += grid[a, b] * 0.5**T
        B_win_prob += new_grid[:, N].sum()
        grid = new_grid
    return B_win_prob


# T_max = 2
# grid_T = np.zeros((N, N))

# for i, grid_T in enumerate(yield_grid_T()):
#     if i != 2:
#         continue
#     B_win_prob = run_grid(grid_T)
#     print(str(grid_T), i, B_win_prob)
#     for a in range(N):
#         for b in range(N):
#             fast_method = recurse_A_first(a, b)
#             distribution_method = run_grid(grid_T, a, b)
#             print(f"(A: {a}, B: {b}), fast_method: {fast_method}, distribution_method: {distribution_method}")