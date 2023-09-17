import math

N = 10**25
P = int(math.log2(N))

#history[power] -> {n:count}
history = [dict() for _ in range(P+1)]

def recurse(n, p):
    #Check base case
    if p == 0:
        return n >= 0 and n <= 2
    #Check if a solution is possible
    if n > 2**(p+2) - 2:
        return 0
    # Check if the solution has been found before
    if n in history[p]:
        return history[p][n]
    #Recurse down to the next level
    count = 0
    for m in range(3):
        if (d := n - m*2**p) >= 0:
            count += recurse(d, p - 1)
    history[p][n] = count
    return count

print("ans", recurse(N,P))
pass