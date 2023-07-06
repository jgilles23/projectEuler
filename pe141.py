import math
import sympy

def progressive_brute_force(n):
    #Check if n is a progressive number
    n_print = False
    for d in range(1,n+1):
        r = n % d
        q = (n - r)//d
        X = sorted([q,r,d])
        ratio = 0
        if X[0] != 0 and X[0]/X[1] == X[1]/X[2]:
            ratio = q/r
        if ratio > 0:
            if n_print == False:
                print(n, "sqrt:", n**0.5)
                n_print = True
            print("   (q:{}, r:{}, d:{}), ratio:{}".format(q,r,d,ratio))

def progressive_symmetric_square(m):
    #Check if n = m**2 is progressive
    n = m**2
    n_print = False
    # d_max = int((n/2)**(2/3))
    d_max = m
    for d in range(2,d_max+1):
        r = n % d
        q = (n - r)//d
        if q*r == d**2:
            if n_print == False:
                print("m: {:,}, n: {:,}, d_max: {}".format(m, n, d_max))
                n_print = True
            print("   (q:{}, r:{}, d:{}), ratio:{}".format(q,r,d,q/d))
            return n
    return 0

# New try on speed

def recursive_gamma_delta(factors, m_power, first_loop = True):
    # factors: the REMAINING factors of m: format [(factor, count), (factor, count), ...]
    # first_loop: checks if iteration should end (at the middle of the factorizaion), and swap gamma/delta:
    # m_power: the power of m with which to produce gamma and delta up to; usually 2 or 4
    #Return: gamma, delta: where gamma*delta = m**2 and gamma > delta
    # gamma
    if len(factors) == 0:
        yield 1, 1
        return
    factor, count = factors[0]
    count = count*m_power
    for i in range(0, count + 1):
        for gamma, delta in recursive_gamma_delta(factors[1:], m_power, False):
            gamma = gamma*factor**i
            delta = delta*factor**(count - i)
            if first_loop:
                if gamma == delta:
                    #Stop at the square root
                    return
                #Otherwise, gamma should always be bigger than delta on the return, flip if needed
                if gamma > delta:
                    yield gamma, delta
                else:
                    yield delta, gamma
            else:
                #Otherwise return gamma and delta
                yield gamma, delta



def diophantine_square(m, factors):
    # Determine if m has solutions, using the diophantine equation (solved on paper)
    # gamma*delta = m^4
    for gamma, delta in recursive_gamma_delta(factors, m_power=2):
        epsilon, exactFlag = sympy.integer_nthroot(gamma - delta, 3)
        if delta >= epsilon:
            continue
        if exactFlag == False:
            continue
        q,r,d = epsilon**2, delta**2, delta*epsilon
        print("m: {:,}, n: {:,}, (gamma: {:,}, delta: {:,}, epsilon: {:,}), (q: {:,}, r: {:,}, d: {:,}), ratio: {:.4}".format(m, m**2, *(gamma, delta, epsilon), *(q, r, d), d/r))
        return m**2
    return 0

def integer_divide(a, b):
    # Return integer division of a & b; return flag if perfect divisons
    return a//b, a % b == 0

def diophantine_four(m, factors):
    # Determine if m is progressive using the factors of the 4th power of m
    # Assumes q > d > r to work
    n = m**2
    for gamma, delta in recursive_gamma_delta(factors, m_power=4):
        q, integerFlag = sympy.integer_nthroot(gamma + delta - 2*n, 3)
        if integerFlag == False:
            continue
        j, integerFlag = integer_divide(gamma - delta, q)
        if integerFlag == False:
            continue
        d, integerFlag = integer_divide(-q**2 + j, 2)
        if integerFlag == False:
            continue
        r, integerFlag = integer_divide(d**2, q)
        if integerFlag == False:
            continue
        if (not q>d) or (not d>r):
            continue
        print("m: {:,}, n: {:,}, (gamma: {:,}, delta: {:,}), (q: {:,}, r: {:,}, d: {:,}), ratio: {:.4}".format(m, n, *(gamma, delta), *(q, r, d), d/r))
        return n
    return 0


#Fist devise all the factors up to M
M = int(10**(6))

prime_factors = [{} for _ in range(M)]
for i in range(2,M):
    # More than 2 factors - already factorized
    if len(prime_factors[i]) >= 2:
        continue
    # Either prime or having only a single factor
    if len(prime_factors[i]) == 0:
        #prime
        for j in range(i, M, i):
            prime_factors[j][i] = 1
    else:
        # Single factor
        f = list(prime_factors[i])[0]
        for j in range(i, M, i):
            prime_factors[j][f] += 1
print("Prime factors found.")
#Convert the prime factors into tuples
for i,f in enumerate(prime_factors):
    prime_factors[i] = list(f.items())
print("Translated to tuples.")

# m = 102
# factors = prime_factors[m]
# print("m", m, "n", m**2, "factors", factors)
# for gamma, delta in recursive_gamma_delta(factors):
#     print(gamma, delta, (gamma - delta)**(1/3))

# for m in range(2, M):
#     if m%10000 == 0: print(m)
#     for gamma, delta in recursive_gamma_delta(list(prime_factors[m].items())):
#         pass
# exit()

s = 0
# s2 = 0
s3 = 0
for m in range(2, M):
    # progressive_brute_force(n**2)
    # s += progressive_symmetric_square(m)
    # s2 += diophantine_square(m, prime_factors[m]) #Method failed to find some answers
    s3 += diophantine_four(m, prime_factors[m])
print("ans", s)
# print("ans2", s2)
print("ans3", s3)

exit()

m = 312
n = m**2
q,r,d = (1058, 8, 92)

print(q**6 + 4*q**3*m**2)
j = (q**4 + 4*q*m**2)**0.5
print(j, "int OK")
j = int(j)
r = q**3
k = j*q
print("r", r, "k", k)
print(r**2 + 4*m**2*r - k**2, "zero OK")
x, y = (r, k)
alpha, beta = (-8*m**2, 0)
D = 4
X, Y = (D*x - alpha, D*y - beta)
k_right = 64*m**4
print("X", X, "Y", Y, "k_right", k_right)
print(X**2 - Y**2 == k_right, "True OK")
gamma0, delta0 = (X+Y, X-Y)
print("gamma", gamma0, "delta", delta0)
gamma3, delta3 = (gamma0/8, delta0/8)
print("gamma", gamma3, "delta", delta3, "integers OK")
gamma3, delta3 = (int(gamma3), int(delta3))
print("x", x, "y", y)
x, y = (gamma3 + delta3 - 2*m**2, gamma3 - delta3)
print("x", x, "y", y, "match OK")
gamma, delta = gamma3, delta3
print(q**3, (gamma**0.5 - delta**0.5)**2, "OK if equal")
gamma_prime, delta_prime = (gamma3**0.5, delta3**0.5)
print("gamma_prime", gamma_prime, "delta_prime", delta_prime, "integers OK")
gamma_prime, delta_prime = int(gamma_prime), int(delta_prime)
q = (gamma_prime - delta_prime)**(2/1)
print(q)
print((gamma*delta)**0.5)


exit()

#New Method: Diophantine -> choose Epsilon first -> VERY SLOW
for epsilon in range(1, int(M**(2/3))):
    for delta in range(1, int((M**2 - epsilon**3)**0.5)+1):
        gamma = epsilon**3 + delta
        n = epsilon*delta
        m = n**0.5
        q, r, d = (epsilon**2, delta**2, delta*epsilon)
        print("m: {}, n: {}, (q: {}, r: {}, d: {})". format(m, n, q,r,d))

