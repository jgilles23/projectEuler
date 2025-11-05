import sympy
import math
import numpy as np

N = 2**50

if N <= 10**6:
    count_squarefree = 0
    for i in range(1,N):
        factors = sympy.ntheory.factorint(i)
        for key in factors:
            if factors[key] >= 2:
                break
        else:
            count_squarefree += 1
    print("ans", count_squarefree)

# cumulative = 1
# for prime in sympy.primerange(0, int(math.sqrt(N)) + 1):
#     print((1 - (N//prime**2)/N))
#     cumulative *= 1 - (N//prime**2)/N
#     print(prime, cumulative)
# print("ans", N*cumulative)

count_squarefree = [N]
squared_primes = [p**2 for p in sympy.ntheory.generate.primerange(0,int(math.sqrt(N)) + 1)]
print("squared_primes generated")
def recursive_prime_counter(base, index, sign):
    for i in range(index + 1, len(squared_primes)):
        new_base = base*squared_primes[i]
        if new_base > N:
            return
        count_squarefree[0] += sign*(N//new_base)
        # print(f"base: {base}, new_base: {new_base}, i: {i}, squared prime: {squared_primes[i]}, adjustment: {sign*(N//new_base)}, new count: {count_squarefree[0]}")
        recursive_prime_counter(new_base, i, -1*sign)

recursive_prime_counter(1, -1, -1)
print("ans", count_squarefree[0])

#Try a numpy based approach that is hopefuly more efficient, but probably not
# squared_primes = np.array(list(p**2 for p in sympy.ntheory.generate.primerange(0,int(math.sqrt(N)) + 1)))
# count_squarefree = [N - np.sum(N//squared_primes)]
# def recursive_prime_counter(bases, shifted_primes, sign):
#     for i, base in enumerate(bases):
#         cutoff_value = N//base
#         cutoff_i = np.searchsorted(shifted_primes, cutoff_value, "right")
#         if cutoff_i <= i + 1:
#             #Cannot grow anymore
#             return
#         new_bases = base*shifted_primes[i+1:cutoff_i]
#         counts = N//new_bases
#         count_squarefree[0] += sign*np.sum(counts)
#         recursive_prime_counter(new_bases, shifted_primes[i+2:cutoff_i], -1*sign)

# recursive_prime_counter(squared_primes, squared_primes[1:], 1)
# print(count_squarefree)


# count_squarefree = [N - 1]
# squared_prime_list = [p**2 for p in sympy.ntheory.generate.primerange(0,int(math.sqrt(N)) + 1)]
# print("squared_prime list generated. len:", len(squared_prime_list))

# #Add back in and subtract back out combinations of the prime_lists until we finish
# def recursive_prime_counter(base, remaining_squared_primes, sign, level):
#     for i, squared_prime in enumerate(remaining_squared_primes):
#         if level == 0 and i > 0 and int(math.log2(i)) == math.log2(i):
#             print(i)
#         new_base = squared_prime*base
#         if new_base < N:
#             count_squarefree[0] += sign*(N//new_base)
#             recursive_prime_counter(new_base, remaining_squared_primes[i+1:], sign*-1, level+1)
#         else:
#             #stop checking, we has passed the threshold
#             return

# recursive_prime_counter(1, squared_prime_list, -1, 0)
# print("ans", count_squarefree[0])

