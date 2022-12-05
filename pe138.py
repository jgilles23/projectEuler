import math

from sympy.solvers.diophantine import diophantine
from sympy import symbols
x, y, u = symbols("x, y, u", integer=True)

num_digits = 35

q = diophantine(x**2 - 20*y**2 + 4, u)
for n in range(20):
    for solution_tuple in q:
        solution_numeric = []
        for variable_equation in solution_tuple:
            numeric = variable_equation.evalf(num_digits, subs={u:n})
            numeric_digits = len(str(int(numeric)))
            if numeric_digits > num_digits - 2:
                raise Exception("Need more digits.", numeric_digits, "needed.")
            if numeric >= 0:
                solution_numeric.append(int(numeric))
            if len(solution_numeric) >= 2:
                B, L = solution_numeric
                if (B+4)%5 == 0:
                    b = (B+4)//5
                    print("FOUND", "B", B, ", L", L, ", b", b)
                else:
                    print("not found", "B", B, ", L", L)


exit()

def isSquare(n):
    ## Trivial checks
    if type(n) != int:  ## integer
        return False
    if n < 0:      ## positivity
        return False
    if n == 0:      ## 0 pass
        return True

    ## Reduction by powers of 4 with bit-logic
    while n&3 == 0:    
        n=n>>2

    ## Simple bit-logic test. All perfect squares, in binary,
    ## end in 001, when powers of 4 are factored out.
    if n&7 != 1:
        return False

    if n==1:
        return True  ## is power of 4, or even power of 2


    ## Simple modulo equivalency test
    c = n%10
    if c in {3, 7}:
        return False  ## Not 1,4,5,6,9 in mod 10
    if n % 7 in {3, 5, 6}:
        return False  ## Not 1,2,4 mod 7
    if n % 9 in {2,3,5,6,8}:
        return False  
    if n % 13 in {2,5,6,7,8,11}:
        return False  

    ## Other patterns
    if c == 5:  ## if it ends in a 5
        if (n//10)%10 != 2:
            return False    ## then it must end in 25
        if (n//100)%10 not in {0,2,6}: 
            return False    ## and in 025, 225, or 625
        if (n//100)%10 == 6:
            if (n//1000)%10 not in {0,5}:
                return False    ## that is, 0625 or 5625
    else:
        if (n//10)%4 != 0:
            return False    ## (4k)*10 + (1,9)


    ## Babylonian Algorithm. Finding the integer square root.
    ## Root extraction.
    s = (len(str(n))-1) // 2
    x = (10**s) * 4

    A = {x, n}
    while x * x != n:
        x = (x + (n // x)) >> 1
        if x in A:
            return False
        A.add(x)
    return True


N = 12

L_count = 0
L_sum = 0
b = 14
while L_count < N:
    b += 2
    pre_k2 = b**2//4*5 + 1
    L2_plus = pre_k2 + 2*b
    L2_minus = pre_k2 - 2*b
    if isSquare(L2_plus):
        L_count += 1
        L_sum += math.sqrt(L2_plus)
        print("#", L_count, ":", b, math.sqrt(L2_plus))
    if isSquare(L2_minus):
        L_count += 1
        L_sum += math.sqrt(L2_minus)
        print("#", L_count, ":", b, math.sqrt(L2_minus))
print("ANS", L_sum)