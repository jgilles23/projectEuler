import math
import sympy

N = 2**40

max_prime = int(math.sqrt(N/2**3))
primes = list(sympy.primerange(max_prime+1))

def test_prime_proof(n):
    str_n = str(n)
    for i in range(len(str_n)):
        for digit in "0123456789":
            str_m = str_n[:i] + digit + str_n[i+1:]
            if sympy.isprime(int(str_m)):
                return False
    return True

candidates = []

for p in primes:
    for q in primes:
        if p == q:
            continue
        #Get the number for testing
        n = p**2 * q**3
        #Too far down this prime list, break
        if n > N:
            break
        #Test for 200 substring
        if "200" not in str(n):
            continue
        #Test for prime proof
        if not test_prime_proof(n):
            continue
        #We have found a candidate
        candidates.append(n)
    # Exit if no primes worked matched with p
    if q == 2:
        break

candidates.sort()
print("candidates", len(candidates))
print(candidates)
ans = candidates[200 - 1]
print("ans", ans)


