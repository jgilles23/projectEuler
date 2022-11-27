import sympy

# print((3*19)**0.5)

N = 10**6

a = 1
b = 0
p = a**3 - b**3

primes = []

while True:
    a += 1
    if a**3 - (a-1)**3 > N:
        #Cannot make a difference of cubes small enough
        break
    for b in range(a-1, 0, -1):
        p = a**3 - b**3
        if p > N:
            #Stop looking at b, difference will never be small enought
            break
        if sympy.isprime(p):
            #Found one that works
            primes.append(p)
            print("Found", "p", p, "a", a, "b", b)
print(primes)
print("ANS", len(primes))
