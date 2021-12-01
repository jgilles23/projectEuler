import sympy

M = 10**2

primes = list(sympy.primerange(0,M+1))
#print(primes)

partition_counts = [0]*(M+1)

k = 0
m = 0
prime_count = [0]*len(primes)

while True:
    #N maximum allowed value of m
    #k is the current position of iteration in prime_count
    #m is the current sum of prime count
    #print(prime_count, "k", k, "m", m)
    if k >= len(primes):
        break
    #Test if the next value is less than M
    if m + primes[k] <= M:
        #print("less")
        prime_count[k] += 1
        m += primes[k]
        k = 0
        #print("found", prime_count, "k", k, "m", m)
        partition_counts[m] += 1 #Count the found partition
        continue
    else:
        #print("more")
        m -= prime_count[k]*primes[k]
        prime_count[k] = 0
        k += 1
        continue

print(partition_counts)
first = [x>5000 for x in partition_counts].index(True)
print("ans", first)

