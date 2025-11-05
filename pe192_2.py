import math
import sympy
from decimal import *

# r = sympy.sqrt(n)
# print(r)
# for j in range(15):
#     i = sympy.floor(r)
#     print(i, end=", ")
#     f = r - i
#     r = 1/f
#     r = r.simplify()
# print()

# a,b,c,d,n,i = sympy.symbols("a b c d n i")
# r0 = a/b + c/d*sympy.sqrt(n)
# r1 = 1/(r0 - i)
# print(r1.cancel())

def iterate_continued_fraction(inputs):
    #r = a/b + c/d*sqrt(n)
    #Iterative calculation of the continued fraction of sqrt(n)
    a,b,c,d,n = inputs
    i = int(a/b + c/d*math.sqrt(n))
    denominator = n*(b*c)**2 - (a*d - b*d*i)**2
    A = -b*d*(a*d - b*d*i)
    C = b*d*b*c
    gcd_A_denom = math.gcd(A,denominator)
    a = A//gcd_A_denom
    b = denominator//gcd_A_denom
    gcd_C_denom = math.gcd(C, denominator)
    c = C//gcd_C_denom
    d = denominator//gcd_C_denom
    # print(f"i: {i}, {a}/{b} + {c}/{d}*sqrt({n})")
    return i, (a,b,c,d,n)

def continued_fraction(n):
    remainder = (0,1,1,1,n)
    remainders = [remainder]
    cf = []
    while True:
        i, remainder = iterate_continued_fraction(remainder)
        cf.append(i)
        if remainder in remainders:
            start_of_repeat = remainders.index(remainder)
            # print("Repeating starting at index:", start_of_repeat)
            break
        remainders.append(remainder)
    # print(cf)
    return cf, start_of_repeat

def generate_convergents(cf, start_of_repeat, value):
    A_m2, A_m1 = 1, cf[0]
    B_m2, B_m1 = 0, 1
    # yield (A_m1,B_m1) #Yield back the n=0 value
    index = 0
    while True:
        index += 1
        #For the repeated continued fractions
        if index == len(cf):
            index = start_of_repeat
        #Calculate A_n and B_n
        A = cf[index]*A_m1 + A_m2
        B = cf[index]*B_m1 + B_m2
        #Test to see if we have any better semiconvergents
        A_best, B_best = A_m1, B_m1
        m = 0
        while True:
            m += 1
            A_m = A_m2 + m*A_m1
            B_m = B_m2 + m*B_m1
            #Check denominator bound
            if B_m > bound:
                break
            #Have reached A & B, no more semiconvergents
            if A_m >= A or B_m >= B:
                break
            #Test if the semiconvergent is better than best found so far
            left = abs(value - Decimal(A_m)/Decimal(B_m))
            right = abs(value - Decimal(A_best)/Decimal(B_best))
            if left < right:
                A_best, B_best = A_m, B_m
                yield (A_m, B_m), "s" #Semiconvergent
            elif left == right:
                raise Exception("Percision error")
        #Check denominator bound
        if B > bound:
            return
        #yield convergent
        yield (A,B), "c" #Convergent
        #Setup next iteration
        A_m2, A_m1 = A_m1, A
        B_m2, B_m1 = B_m1, B

bound = 10**12
getcontext().prec = 70
N = 100000

denominator_sum = 0
for n in range(2, N+1):
    #Remove perfet squares
    if math.isqrt(n)**2 == n:
        continue
    cf, start_of_repeat = continued_fraction(n)
    # cf = [2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1]
    # print(cf, "repeat starts at:", start_of_repeat)
    for j, ((A,B), type) in enumerate(generate_convergents(cf, start_of_repeat, Decimal(n).sqrt())):
        pass
    denominator_sum += B
    if n % 5000 == 0:
        print(f"n: {n}, {A}/{B} {type}")

print("ans", denominator_sum)


