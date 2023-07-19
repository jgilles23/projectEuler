import numpy as np
import math
import itertools

N = 10**8

# Real Sum - Better than brute force, but still pretty slow
A = np.arange(1,N+1, dtype=np.int64)
real_sum = sum(A*(N//A))
print("Real     : {:,}".format(real_sum))
print()

# Hopefully a faster method for the real part
imaginary_sum = 0
a_prime_max = int(math.sqrt(N-1))
for a_prime in range(1, a_prime_max+1):
    b_prime_max = min(int(math.sqrt(N- a_prime**2)), a_prime)
    for b_prime in range(1, b_prime_max+1):
        if math.gcd(a_prime, b_prime) != 1:
            continue
        g_max = N//(a_prime**2 + b_prime**2)
        G = np.arange(1, g_max+1, dtype=np.int64)
        imaginary_sum += 2*(a_prime + b_prime)*sum(G * (N // (G*(a_prime**2 + b_prime**2)))) // (1 + (a_prime==1)) #Correct for the primary axis
print("Imaginary: {:,}".format(imaginary_sum))
total_sum = real_sum + imaginary_sum
print("Total    : {:,}".format(total_sum))
print("ans", total_sum)        

exit()

#Imaginary Sum - SLOW
print()
imaginary_sum = 0
a_max = N//2
for a in range(1, a_max+1):
    b_max = int(math.sqrt(N*min(a, N//2) - a**2))
    B = np.arange(1,b_max+1, dtype=np.int64)
    G = np.gcd(a, B)
    imaginary_sum += 2*a*sum(N // (G * ((a//G)**2 + (B//G)**2)))
print("Imaginary: {:,}".format(imaginary_sum))
total_sum = real_sum + imaginary_sum
print("Total    : {:,}".format(total_sum))

exit()

#Brute Force Method
print()
print("BRUTE FORCE")
real_sum = 0
imaginary_sum = 0
for n in range(1,N+1):
    # Real portion
    for a in range(1,n+1):
        if n%a == 0:
            real_sum += a
    # Imaginary portion
    for a in range(1,n):
        for b in range(1,n):
            g = math.gcd(a,b)
            if n % (g*((a//g)**2 + (b//g)**2)) == 0:
                # print("n: {}, a: {}, b: {}, g: {}, s+: {}".format(n, a, b, g, 2*a))
                imaginary_sum += 2*a
print("Real     : {:,}".format(real_sum))
print("Imaginary: {:,}".format(imaginary_sum))
total_sum = real_sum + imaginary_sum
print("Total    : {:,}".format(total_sum))



exit()

a_cutoff = int(math.sqrt(N))
imaginary_sum = 2*sum(A[:a_cutoff]*np.sqrt(N-A[:a_cutoff]**2).astype(int))
print("Imaginary:", imaginary_sum)


def calc_coprime(factors, N):
    #Calculate the number of coprime numbers in range [1,N]
    #Iterate through the combination of the factors as required
    s = sum(N//f for f in factors)
    for r in range(2, len(factors)+1):
        for combination in itertools.combinations(factors, r):
            s -= N//math.prod(combination)  
    return N-s

a_prime_factors = (2,3)
calc_coprime(a_prime_factors, N)
