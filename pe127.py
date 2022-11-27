import sympy
import math
import numpy as np

N = 120_000

primes = [*sympy.primerange(N)]
factors = [set() for _ in range(N)]
rads = np.full(N, 1)
for i in primes:
    for j in range(i,N,i):
        factors[j].add(i)
for i, f in enumerate(factors):
    rads[i] = math.prod(f)
log_rads = np.log(rads)
all_c = np.arange(N)
log_c = np.log(all_c)
print("primes, factors, and rads generated")


sum_c = 0
b_sieve = np.full(N, False)
log_sum = np.full(N, 0.0)
print("memory allocated")
for a in range(1, N//2):
    if a%512 == 0: print(a)
    #Work the sums
    log_sum[a+1:N-a] = log_rads[a] + log_rads[a+1:N-a] + log_rads[a+a+1:N] - log_c[a+a+1:N]
    b_sieve[a+1:N-a] = log_sum[a+1:N-a] < 0
    #Make sure the pure radical of a is not too large
    # b_sieve[a+1:N-a] = True
    for f in factors[a]:
        b_sieve[a:N-a:f] = False
    sum_c += np.sum(b_sieve[a+1:N-a] * all_c[a+a+1:N])

print("ANS", sum_c)

exit()

sum_c = 0
b_sieve = np.full(N, False)
for a in range(1, N//2):
    if a%128 == 0: print(a)
    #Make sure the pure radical of a is not too large
    b_sieve[a+1:N-a] = True
    for f in factors[a]:
        b_sieve[a:N-a:f] = False
    for b in range(a+1, N-a):
        if b_sieve[b]:
            c = a + b
            #Check if radical of ab is too large
            if log_rads[a] + log_rads[b] + log_rads[c] >= log_c[c]:
                continue
            #The sum of two co-prime numbers are always co-prime!
            sum_c += c

print("ANS", sum_c)

exit()


# sum_c = 0
# for a in range(1, N//2):
#     if not a%128: print(a)
#     for b in range(a+1, N-a):
#         c = a + b
#         if log_rads[a] + log_rads[b] + log_rads[c] >= log_c[c]:
#             continue
#         if not(factors[a] & factors[b]):
#             #a & b are co-prime
#             sum_c += c
# print("ANS", sum_c)
# exit()

def recurse_a(facts_a, facts_b, i, level):
    i_used = False
    new_facts_a = set(facts_a)
    new_facts_b =set(facts_b)
    factors[i]
    #Add to the set
    new_facts_a.add(primes[i])
    n_a = math.prod(new_facts_a)
    # print(" -"*level, primes[i], ":", "a", new_facts_a, n_a, "b", facts_b, end=" ")
    if n_a >= N/2:
        # print("Fail A")
        pass
    else:
        # print("cont")
        i_used = True
        if n_a < math.prod(new_facts_b): print("a", new_facts_a, n_a, "b", facts_b, math.prod(facts_b))
        recurse_a(new_facts_a, facts_b, i+1, level+1)
    #Try in set b
    new_facts_b.add(primes[i])
    n_b = math.prod(new_facts_b)
    # print(" -"*level, primes[i], ":", "a", facts_a, "b", new_facts_b, n_b, end=" ")
    if n_b > N/2:
        # print ("Fail B")
        pass
    else:
        # print("cont")
        i_used = True
        if math.prod(facts_a) < n_b: print("a", facts_a, math.prod(facts_a), "b", new_facts_b, n_b)
        recurse_a(facts_a, new_facts_b, i+1, level+1)
    #try not in either set
    # print(" -"*level, primes[i], ":", facts)
    if i_used:
        # print(" -"*level, primes[i], ":", "a", facts_a, "b", facts_b)
        recurse_a(facts_a, facts_b, i+1, level+1)

recurse_a(set(), set(), 0, level=0)

exit()

sum_c = 0
for c in range(N):
    for a in range(1, int(math.ceil(c/2))):
        b = c - a
        #Test if coprime
        if factors[a] & factors[b]:
            continue
        if factors[a] & factors[c]:
            continue
        if factors[b] & factors[c]:
            continue
        #Test overall radical
        u = factors[a].union(factors[b]).union(factors[c])
        rad = math.prod(u)
        if rad >= c:
            continue
        #This is an abc hit
        print("abc hit", (a,b,c))
        sum_c += c
print("sum_c", sum_c)
