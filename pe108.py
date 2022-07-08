import numpy as np
import math

#Try again

N = 4*10**6

n_max = 1000000

#Get factors for all numbers up to n_max
b_factor = [{} for _ in range(n_max)]
q = 0
for i in range(2, n_max):
    q += 1
    if (q == 1000000):
        print(i//1000000)
        q = 0
    if len(b_factor[i]) != 0:
        #Only process for prime numbers
        continue
    #Set all the divisiors to 1
    for k in range(i, n_max, i):
        b_factor[k][i] = 1
    #Check for those with higher divisors
    j = i*i
    while j < n_max:
        for k in range(j, n_max, j):
            b_factor[k][i] += 1
        j = j * i
print("Factoring complete.")

biggest_divisor = 0
# d = np.full(len(b_factor),0)
#reduce to the number of divisors
for i, factors in enumerate(b_factor):
    divisors = 1
    for f, occ in factors.items():
        divisors *= (occ + 1)
    # d[i] = divisors
    if divisors > 100:
        #Calculate actual number of breakdowns
        n = i
        x = np.arange(n+1, 2*n+1, dtype=np.int64)
        c = np.sum((n*x) % (x-n) == 0)
        print("New Biggest", "n",n,"c",c,"divisors", divisors)
        biggest_divisor = divisors
        if c > N:
            break
print("Completed divisor counting.")

exit()

c_best = 0

for n in range(4,n_max):
    x = np.arange(n+1, 2*n+1, dtype=np.int64)
    # print(x.dtype)
    # break
    c = np.sum((n*x) % (x-n) == 0)
    if c > c_best:
        c_best = c
        print("n",n,"c",c,"divisors",d[n])


exit()

#Apparently this problem is equivelent to findng the number of divisors of n... NO IT IS NOT! (but it is weirdly close...)

# N = 1000

# n_max = 100000000

# #Get factors for all numbers up to n_max
# b_factor = [{} for _ in range(n_max)]
# q = 0
# for i in range(2, n_max):
#     q += 1
#     if (q == 1000000):
#         print(i//1000000)
#         q = 0
#     if len(b_factor[i]) != 0:
#         #Only process for prime numbers
#         continue
#     #Set all the divisiors to 1
#     for k in range(i, n_max, i):
#         b_factor[k][i] = 1
#     #Check for those with higher divisors
#     j = i*i
#     while j < n_max:
#         for k in range(j, n_max, j):
#             b_factor[k][i] += 1
#         j = j * i
# print("Factoring complete.")

# biggest_divisor = 0
# #reduce to the number of divisors
# for i, factors in enumerate(b_factor):
#     divisors = 1
#     for f, occ in factors.items():
#         divisors *= (occ + 1)
#     if divisors > biggest_divisor:
#         print("New Biggest", i, divisors)
#         biggest_divisor = divisors
#     if divisors > N:
#         print("ANSWER", i)
#         break
# print("Completed divisor counting.")


# exit()

# N = 20
# n_max = 10

# #Get factors for all numbers up to n_max
# b_factor = [{} for _ in range(n_max)]
# for i in range(2, n_max):
#     if len(b_factor[i]) != 0:
#         #Only process for prime numbers
#         continue
#     #Set all the divisiors to 1
#     for k in range(i, n_max, i):
#         b_factor[k][i] = 1
#     #Check for those with higher divisors
#     j = i*i
#     while j < n_max:
#         for k in range(j, n_max, j):
#             b_factor[k][i] += 1
#         j = j * i
# print("Factoring complete.")

# #Reduce factors to minimum divisor "d"
# b_min_div = []
# for factors in b_factor:
#     d = 1 #min divisor
#     for f, occ in factors.items():
#         d *= f**int(math.ceil(occ/2))
#     b_min_div.append(d)

# print(b_min_div)

# #Use the minimum divisors to find the number of breakdowns
# # a = (n-b)^2/b <- if this is divisible than a is an integer therfore 1/x + 1/y = 1/n has a solution where a = x+y
# n_breakdowns = [1]*n_max
# C = np.full((n_max,n_max),0)
# C[:,1] = 1
# for b, d in zip(range(2, n_max), b_min_div[2:]):
#     print("b", b, "d", d)
#     for c in range(d, n_max, d): #c = n + b
#         n_breakdowns[c - b] += 1
#         C[c,b] += 1

# print(C)
# print(n_breakdowns)

# exit()

N = 10

biggest_count = 0
n = 4
while True:
    y = np.arange(n+1, 2*n+1, dtype=float)
    # print(y)
    a = y / (y-n) * y
    if n == 6:
        for y, x in zip(y, a-y):
            if int(x) == x:
                print(" > x", x, "y", y)
            else:
                print(" ###### x", x, "y", y)
    # print(a)
    count  = np.sum((a - np.floor(a)) == 0)
    if True: #count > biggest_count:
        print("n", n, "count", count)
        biggest_count = count
    if count > N:
        print("SOLVED", n)
        break
    n += 1