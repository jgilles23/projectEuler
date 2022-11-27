import sympy

# By math on paper, figured out that only the vertical line from the orgin 
# And the vertical line of digits just to the right are the only possible 
# 3 or more prime difference lines

N = 2000

PD_3 = [1,2]
r = 1
n = 2
while len(PD_3) < N:
    n += 6*r
    r += 1
    #c = 0; p = 0 position
    p_count_center = 0
    p_count_right = 0
    #c = 0; p = 0; up counterclockwise & up clockwise
    p_count_center += sympy.isprime(6*r + 1)
    p_count_center += sympy.isprime(12*r + 5)
    #shared between center and right
    if sympy.isprime(6*r - 1):
        p_count_center += 1
        p_count_right += 1
    #c = 5; p = r - 1; down counterclockwise & up clockwise
    p_count_right += sympy.isprime(12*r - 7)
    p_count_right += sympy.isprime(6*r + 5)
    #Check if they have 3 primes
    if p_count_center >= 3:
        print("FOUND", n, "r", r, "center")
        PD_3.append(n)
    if p_count_right >= 3:
        print("FOUND", n + 6*r - 1, "r", r, "right")
        PD_3.append(n + 6*r - 1)
print("ANS", PD_3[N-1])



exit()

# start one ring down
n = 7 # integer
r = 1 # ringe
c = 5 # corner
p = 1 # dist from corner

outer = [17, 6, 7, 8, 9, 10, 11, 12] #Seed

PD_count = 2

for _ in range(1000000):
    n += 1
    p += 1
    if p >= r:
        c += 1
        p = 0
    if c > 5:
        r += 1
        c = 0
        #Update inner and outer rings
        inner = outer
        outer = [*range(6*r-1, 6*(r+1)+1)]
        outer[0] += 6*(r+1)
        # print("r", r, "inner", inner, "outer", outer)

    deltas = []
    #right
    if c == 0 and p == 0:
        deltas.append(6*r - 1)
    else:
        deltas.append(1)
    #left
    if c == 5 and p == r - 1:
        deltas.append(6*r - 1)
    else:
        deltas.append(1)
    #Get the inners & outers
    if p == 0:  
        deltas.append(inner[c+1])
        deltas.extend(outer[c:c+3])
    else:
        deltas.extend(inner[c+1:c+3])
        deltas.extend(outer[c+1:c+3])
        if c == 5 and p == r - 1:
            deltas[2] = inner[0]

    PD = 0
    for d in deltas:
        if sympy.isprime(d):
            PD += 1

    if PD >= 3:
        PD_count += 1
        print("#", PD_count, "n", n, "r", r, "c", c, "p", p, "deltas", deltas, "PD", PD)

    