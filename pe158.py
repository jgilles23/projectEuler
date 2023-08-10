import math

N = 26

def p(n):
    count = 0
    for valley in range(0,n-1):
        for peak in range(valley+1, n):
            count += 2**(peak-valley-1)
    count *= math.comb(N, n)
    print("n:", n, "Combination:", count)
    return count


pn = [p(n) for n in range(2, N+1)]
# print(pn)
print("ans", max(pn))

        
            
