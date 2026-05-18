import numpy as np 
import math

import sympy


# print(((2*10**9)/3)**0.5 * ((2*10**9)/7)**0.5)

k_options = [1,2,3,7]
N = 2*10**9

# most_restrictive_m_fraction = 2.0
# most_restrictive_m = None
# most_restrictive_m_allowed = None
# for m in range (2, 100):
#     allowable_per_m = np.full(m, True)
#     for k in k_options:
#         allowable_per_k = np.full(m, False)
#         for a in range(m):
#             for b in range(m):
#                 n = a**2 + k*b**2
#                 n = n % m
#                 allowable_per_k[n] = True
#         allowable_per_m = np.logical_and(allowable_per_m, allowable_per_k)
#         fraction_allowed = np.sum(allowable_per_m) / m
#         if fraction_allowed < most_restrictive_m_fraction:
#             most_restrictive_m_fraction = fraction_allowed
#             most_restrictive_m = m
#             most_restrictive_m_allowed = np.where(allowable_per_m == True)[0]
#             print(f"m={m} yields {np.sum(allowable_per_m)}/{m} = {np.sum(allowable_per_m)/m} results, allowed {np.where(allowable_per_m == True)[0]}")

# print(f"Most restrictive m is {most_restrictive_m} with fraction {most_restrictive_m_fraction} and allowed values {most_restrictive_m_allowed}")

def test(n, k):
    if n < k:
        return False
    max_a = math.isqrt(n-k)
    for a in range(1, max_a + 1):
        max_b = math.isqrt((n - a**2) // k)
        for b in range(1, max_b + 1):
            if a**2 + k*b**2 == n:
                return True
    return False

def multi_test(n):
    for k in k_options:
        if test(n, k) == False:
            return False, k
    return True, None

# k = 7
# for n in range(1, 1000):
#     if multi_test(n):
#         print(f"{n} can be expressed as a^2 + k*b^2 for k in [1,2,3,7], with (n-1) factors as {sympy.factorint(n-1)}")


# q = 10**6
# for p in sympy.primerange(1, 10**9):
#     if p > q:
#         print(p)
#         q += 10**6


# k = 3
# m = 3

# for n in range(1, 1000):
#     # if sympy.isprime(n):
#     #     if test(n, k):
#     #         print(f"{n} can be expressed as a^2 + k*b^2 for k={k}, (n%{m}={n%m})")
#     #         continue
#     # #Test if n contains a square factor
#     # factors = sympy.factorint(n)
#     # for factor, exponent in factors.items():
#     #     if exponent >= 2:
#     #         break
#     # else:
#     #     # Does not have square or greater factors
#     #     if test(n, k):
#     #         print(f"{n} can be expressed as a^2 + k*b^2 for k={k}, (n%{m}={n%m}), factors: {sympy.factorint(n)}")
#     t = test(n, k)
#     if n % 3 == 1 and (n % 4 == 1 or n % 4 == 1) and t == False:
#         print(f"{n} cannot be expressed as a^2 + k*b^2 for k={k}, (n%{3}={n%3}, n%{4}={n%4}), factors: {sympy.factorint(n)}")

# k_options = [1,2,3,7]
# for m in range(840, 841):
#     m_option = True 
#     for p in sympy.primerange(3, 10**7):
#         if p % m == 1:
#             t, k = multi_test(p)
#             if t == False:
#                 m_option = False
#                 break
#     if m_option == True:
#         print(f"m={m} allows 1/{m} value: {m_option}")

#p congruent to 1 (mod 24)

# m = 24
# fails = []
# for p in sympy.primerange(3, 76000):
#     t, k = multi_test(p)
#     if p % m == 1 and t == False:
#         fails.append(p)
#         # print(f"Unexpected prime {p} congruent to 1 mod {m} that cannot be expressed as a^2 + k*b^2 for k in {k_options}, failing for k={k}")

# best = 1.0
# for m in range(25, 10000):
#     results = set(range(m))
#     for f in fails:
#         if f % m in results:
#             results.remove(f % m)
#     if len(results) == 2:
#         print(f"m={m} allows {len(results)}/{m} values, which are {results}")

#Goal to find the largest m such that all solutions are congruent to 1 mod m
# for k in k_options:
#     for m in range(2, 1000):
#         allowable_per_k = np.full(m, False)
#         for a in range(m):
#             for b in range(m):
#                 n = a**2 + k*b**2
#                 n = n % m
#                 allowable_per_k[n] = True
#         if np.sum(allowable_per_k) <= 3:
#             print(f"m={m} allows only 1 value for k={k}, which is {np.where(allowable_per_k == True)}")

# primes = np.array(list(sympy.primerange(10, 10**5)))
# print(primes)
# it_works = np.full_like(primes, False)
# print("Testing primes...")
# for i, p in enumerate(primes):
#     t = test(p, 7)
#     it_works[i] = t
# print("Testing modulus...")
# for m in range(2, 1000):
#     modulus = primes % m
#     if np.all(it_works[modulus == 1] == True) and np.all(it_works[modulus != 1] == False):
#         print(f"m={m} works for all primes up to {primes[-1]}")

# def hard_combine(allowed_moduli, moduli):
#     M = math.prod(moduli)
#     combined_allowed = []
#     for i in range(M):
#         for j, m in enumerate(moduli):
#             if i % m == allowed_moduli[j]:
#                 continue
#             else:
#                 break
#         else:
#             combined_allowed.append(i)
#     return combined_allowed, M

# for x in [1, 9, 11]:
#     results, M = hard_combine([x, 1, 1, 1], [14, 3, 8, 4])
#     print(results, M, "->", M//8, [r % (M//8) for r in results])


# for p in sympy.primerange(3, 10**6):
#     t0 = (p % 168) in [1, 25, 121]
#     t1, _ = multi_test(p)
#     if t0 != t1:
#         print(f"Unexpected prime {p} that fails the test, congruent to {p%168} mod 168")

# N = 10**4

# if True:
#     count = 0
#     answer_set = set()
#     for n in range(1, N):
#         if multi_test(n)[0] == True:
#             count += 1
#             answer_set.add(n)
#             # print(f"{n} passes the test")
#     print(f"Count of n that pass the test up to N: {count}")


# primes = []
# for base in range(0, N, 168):
#     for i in [1, 25, 121]:
#         if base + i == 1:
#             pass
#         if sympy.isprime(base + i):
#             primes.append(base + i)
# count = 0
# answer_set_2 = set()
# for i in range(0, len(primes)):
#     #Prime on it's own
#     k = 1
#     while primes[i] * k**2 <= N:
#         count += 1
#         answer_set_2.add(primes[i] * k**2)
#         k += 1
#     #test combination with another prime
#     for j in range(i+1, len(primes)):
#         if primes[i] * primes[j] > N:
#             break
#         k = 1
#         while primes[i] * primes[j] * k**2 <= N:
#             count += 1
#             answer_set_2.add(primes[i] * primes[j] * k**2)
#             k += 1
# print("num primes:", len(primes), "primes[:10]:", primes[:10])
# print("ans", count)

# #Compare the two sets to find any discrepancies
# discrepancies = answer_set.symmetric_difference(answer_set_2)
# print("Discrepancies between the two methods:", discrepancies)

#Ok, so the new plan, is to look at each of the primes with each of the k options, up to some reasonable limit
#We will see which output n moduli are allowed, and use compute to get that down to a hopefully reasonable number less that 1% range
#Then we will write a much faster checker that looks at only those options

def determine_allowed_n_moduli(k_options, m):
    overall_allowed = np.full(m, True)
    for k in k_options:
        allowed = np.full(m, False)
        a = np.arange(m).reshape(-1, 1)
        b = np.arange(m)
        n = (a**2 + k*b**2) % m
        allowed[n] = True
        overall_allowed = np.logical_and(overall_allowed, allowed)
    return np.where(overall_allowed == True)[0]

collect = [] #(overall, p, i, count_n)
for p in sympy.primerange(2, 100):
    base_fraction = 1.0
    base_allowed_n = 1
    base_m = 1
    for i in range(1,10):
        m = p**i
        if m < 1000:
            #Determine the allowed number of n at this modulus
            step_allowed_n = determine_allowed_n_moduli(k_options, m)
            count_n = len(step_allowed_n)
            #Determine the factor of multiplication to yield this new n from the baseline
            step_count_n_multiplier = count_n / base_allowed_n
            step_m_multiplier = m / base_m
            step_score = step_count_n_multiplier / step_m_multiplier
            if count_n != m:
                s = f"{p}^{i} allows {count_n}/{m} = {count_n/m:.4f}, ".ljust(30)
                s += f"base({base_allowed_n})*multiplier({step_count_n_multiplier:.4f}), ".ljust(30)
                s += f"score: {step_score:.4f}"
                print(s)
                base_allowed_n = count_n
                base_m = m
                collect.append((step_score, p, i, count_n, step_count_n_multiplier))
#Sort the collect by score, from low to high
collect.sort()
best_moduli = 1
allowed_n = 1
for step_score, p, i, count_n, step_count_n_multiplier in collect:
    best_moduli *= p
    allowed_n *= step_count_n_multiplier
    if best_moduli > N:
        break
    print(f"Adding p={p}(^{i}) with count_n={count_n}, step_score={step_score:.4f}, overall: {allowed_n:,}/{best_moduli:,}= {allowed_n/best_moduli:.5f}")


# def iterative_moduli_selection(N, p_max=100):
#     best_prime_powers = {} #p: (i, allowed_n)
#     best_moduli = 1
#     best_count_n = 1

#     best_step_p = 1
#     for p in sympy.primerange(2, p_max):
#         new_moduli = best_moduli * p
#         while best_moduli*p < N:
#             if p in best_prime_powers:
#                 old_i, old_allowed_n = best_prime_powers[p]
#                 old_count_n = len(old_allowed_n)
#             else:
#                 old_i = 0
#                 old_count_n = 1
#             step_allowed_n = determine_allowed_n_moduli(k_options, p**(old_i+1))
#             step_count_n = len(step_allowed_n)
#             new_count_n = best_count_n // old_count_n * step_count_n
#             if new_count_n / new_moduli < best_count_n / best_moduli:
#                 best_step_p = p
#                 best_step_old_count_n = old_count_n
#                 best_step_new_allowed_n = step_allowed_n
#     #Update the best that were found for this step
#     save_old_best_count_n = best_count_n
#     best_prime_powers[best_step_p] = (best_prime_powers[best_step_p][0] + 1, best_step_new_allowed_n)
#     best_moduli *= best_step_p
#     best_count_n = best_count_n // best_step_old_count_n * len(best_step_new_allowed_n)
#     #Print the updated best
#     s = f"Best is p:{best_step_p}, "
#     s += f"({save_old_best_count_n}//{best_step_old_count_n}*{len(best_step_new_allowed_n)}={best_count_n}) / "
#     s += f"({best_moduli//best_step_p}*{best_step_p}={best_moduli}), "
#     s += f"frac: {best_count_n/best_moduli:.5f}"

# iterative_moduli_selection(1000, p_max=100)

class package:
    def __init__(self):
        self.prime_powers = {}
        self.prime_allowed_n = {}
    
    def score(self):
        allowed_n_count = 1
        moduli = 1
        for p in self.prime_powers:
            i, allowed_n = self.prime_powers[p], self.prime_allowed_n[p]
            allowed_n_count *= len(allowed_n)
            moduli *= p**i
        score = allowed_n_count / moduli
        return score, allowed_n_count, moduli
    
    def copy(self):
        new_package = package()
        new_package.prime_powers = self.prime_powers.copy()
        new_package.prime_allowed_n = self.prime_allowed_n.copy()
        return new_package
    
    def updated(self, p, delta_i):
        new_package = self.copy()
        if p in new_package.prime_powers:
            new_i = new_package.prime_powers[p] + delta_i
        else:
            new_i = delta_i
        #Cannot compute numbers that are too large
        if p**new_i > 5000:
            return None
        new_package.prime_powers[p] = new_i
        new_package.prime_allowed_n[p] = determine_allowed_n_moduli(k_options, p**new_i)
        return new_package
    
    def __repr__(self):
        score, allowed_n_count, moduli = self.score()
        print_dict = [f"{p}^{self.prime_powers[p]}:{len(self.prime_allowed_n[p])}" for p in self.prime_powers]
        return f"<score: {allowed_n_count:,}/{moduli:,} = {score:.5f}, {str(print_dict)}>"


base_package = package()
for _ in range(5):
    best_package = base_package.copy()
    best_score = base_package.score()
    #Add the next best step
    for p in sympy.primerange(2, 100):
        for delta_i in range(1, 11):
            if p**delta_i > 1000:
                break
            new_package = base_package.updated(p, delta_i)
            if new_package is None:
                continue
            score = new_package.score()
            if score[0] < best_score[0]:
                best_package = new_package
                best_score = score
    print(f"New best package: {str(best_package)}")
    base_package = best_package.copy()



