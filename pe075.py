#Project Euler #75 date 20210503
import math

L = 1.5*10**6

count = {}
triples = {}

m_max = int((L/2)**0.5)+1
for m in range(2,m_max):
    n_max = min(m, int((L/2 - m**2)/m)+1)
    if m%2 == 0:
        #if m is even, n can be anything
        start = 1
        step = 1
    else:
        #If m is odd, n cant be odd
        start = 2
        step = 2
    for n in range(start, n_max, step):
        if math.gcd(n,m) == 1:
            #n,m are coprime
            p1 = 2*m*(m+n)
            k_max = int(L/p1) + 1
            for k in range(1,k_max):
                p = p1*k
                if p <= L:
                    a = m**2 - n**2
                    b = 2*m*n
                    c = m**2 + n**2
                    if p in count:
                        count[p] += 1
                        #triples[p].append((a,b,c,k))
                    else:
                        count[p] = 1
                        #triples[p] = [(a,b,c,k)]

#print(count)
#for t in sorted(triples.keys()): print(t, ":", triples[t])

c = 0
for n in count.values():
    if n == 1:
        c += 1

print("ans",c)

