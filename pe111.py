import sympy
from itertools import combinations
from itertools import product


n = 10
n_comp = 10**(n-1)

parts = [[a * 10**e for e in range(n)] for a in range(10)]

full_sum = 0

for d in range(10):
    num = sum(parts[d])
    print("Digit", d, end=": ")
    N = 0
    S = 0
    M = n
    positions = [*range(n)]
    while N <= 0:
        M -= 1
        for fill_positions in combinations(positions, n - M):
            positions_product = [[*range(10)]]*(n-M)
            for fill_digits in product(*positions_product):
                new_num = num
                for pos, dig in zip(fill_positions, fill_digits):
                    new_num += -1*parts[d][pos] + parts[dig][pos]
                #check if large enough
                if (new_num < n_comp):
                    continue
                #Check if prime
                if sympy.isprime(new_num):
                    N += 1
                    S += new_num
                    print(new_num, end=", ")
    print("")
    print(" - M", M, "N", N, "S", S)
    full_sum += S
print("full sum", full_sum)

exit()

#Let's do it the stupid way to figure out what I am doing wrong
Ms = [0]*10
Ns = [0]*10
Ss = [0]*10
nums = [[] for _ in range(10)]
for i in range(10**(n-1), 10**(n)):
    if not sympy.isprime(i):
        continue
    i_str = str(i)
    counts = [i_str.count(a) for a in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]
    for j in range(10):
        if counts[j] > Ms[j]:
            Ms[j] = counts[j]
            Ns[j] = 0
            Ss[j] = 0
            nums[j] = []
        if counts[j] == Ms[j]:
            Ns[j] += 1
            Ss[j] += i
            nums[j] += [i]
for j in range(10):
    print("digit", j, ":", "M", Ms[j], "N", Ns[j], "S", Ss[j], "nums", nums[j])
print("full sum", sum(Ss))

# prime_count = 0

# for i in range(10**4, 10**4 + 10**4):
#     if (sympy.isprime(i)):
#         prime_count += 1

# print("END", prime_count)
