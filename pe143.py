# PE 143
print("hello")
# from sympy import *
# a,b,c,Cx,Cy,C2 = symbols('a b c cx, cy, c2')
# #Define some points
# Ax, Ay = 0, 0
# Bx, By = c, 0

# #Solve for Point C
# res = solve([Cx + C2 - c, Cy**2 + Cx**2 - b**2, Cy**2 + C2**2 - a**2], [Cx, Cy, C2])
# Cx, Cy, C2 = res[0]

# #Solve for midpoint of BC
# BCx = (Cx + Bx)/2
# BCy = (Cy + By)/2
# BC_N_slope = -(Cx - Bx)/(Cy - By) #Negative inverse of slope from C to B
# #Solve for N
# L = sqrt(3)/2*a
# Nx = BCx + L/sqrt(1+BC_N_slope)
# Ny = BCy + Nx*BC_N_slope

# #Solve for O
# Ox = Bx/2
# Oy = -sqrt(3)/2*Bx

# #Solve for intersection of AN and CO
# x, y = symbols('x y')
# def getLineFormula(x1, y1, x2, y2):
#     return (y2 - y1)/(x2 - x1)*(x - x1) - (y - y1)
# res = solve([getLineFormula(Ax, Ay, Nx, Ny), getLineFormula(Ox, Oy, Cx, Cy)], [x, y], dict=True)
# Tx, Ty = res[0][x], res[0][y]
# print("Ty :", Ty)

# #Solve for length of p
# p = sqrt(Tx**2 + Ty**2)
# print("p :", simplify(p))

# import sympy

# def test120(a,b,c):
#     return -b*c <= b**2 + c**2 - a**2
# def testSides(a,b,c):
#     return a < b + c

# p,q,r = sympy.symbols("p q r")
# for a in range(390, 410):
#     print("a:", a)
#     for b in range(450, 460):
#         for c in range(500, 520):
#             if a==399 and b==455 and c==511:
#                 print("Known solution")
#             if testSides(a,b,c) and testSides(b,a,c) and testSides(c,a,b):
#                 pass
#             else:
#                 continue # Not a triangle
#             if test120(a,b,c) and test120(b,a,c) and test120(c,a,b):
#                 pass
#             else:
#                 continue # Not a triangle with all sides less than 120
#             Zc = p**2 + r**2 + p*r - c**2
#             Za = q**2 + r**2 +q*r - a**2
#             Zb = p**2 + q**2 + p*q - b**2
#             # print((a,b,c))
#             res = sympy.nsolve((Za, Zb, Zc), (p, q, r), (1, 1, 1))
#             for x in res:
#                 if abs(x - int(x)) > 0.0000001:
#                     break
#             else:
#                 print((a,b,c), res)

#Time to try the backtracking approach
# import math
# for c in range(1,400):
#     p = int(c/math.sqrt(3))
#     r = p
#     while r > 0:
#         res = p**2 + r**2 + p*r - c**2
#         if res == 0:
#             print(f"FOUND c:{c}, p:{p}, r:{r}")
#         if res < 0:
#             p += 1
#         else:
#             r -= 1

#That worked well, but I can do that much more directly
import math

# N = 1000
# L = [[] for _ in range(N//3 + 1)]
# for p in range(1, N//3 + 1):
#     if p%1000 == 0:
#         print("Compiling", p)
#     for r in range(p, (N-p)//2 + 1):
#         x = p**2 + r**2 + p*r
#         sqrt_x = math.isqrt(x)
#         if sqrt_x**2 == x:
#             L[p].append(r)
#             print("solution", (p,r), p**2 + r**2 + p*r)
# #Find solutions
# print("Finding Solutions:")
# solutions = set()
# for p in range(len(L)):
#     if p % 5000 == 0:
#         print("Solutioning", p)
#     if len(L[p]) > 1:
#         for r in L[p]:
#             if r < len(L):
#                 for q in L[r]:
#                     if q in L[p]:
#                         if (p+r+q <= N):
#                             solutions.add(p+r+q)
# print("SUMMING")
# ans = sum(solutions)
# print(ans)

# 18199736 is incorrect

import sympy

# def recursive_divisors(prime_factors, i = 1):
#     if len(prime_factors) == 0:
#         return [i]
#     p, e = prime_factors[0]
#     ret = []
#     for f in range(0, e + 1):
#         ret += recursive_divisors(prime_factors[1:], i*p**f)
#     return ret

def generate_r_from_p(p):
    ij = -12*p**2
    # prime_factors_ij = [(a, b*2) for a,b in prime_factors_p]
    # if prime_factors_ij[0][0] == 2:
    #     if prime_factors_ij[1][0] == 3:
    #         prime_factors = [(2, prime_factors_ij[0][1] + 2), (3, prime_factors_ij[1][1] + 1)] + prime_factors_ij[2:]
    #     else:
    #         prime_factors = [(2, prime_factors_ij[0][1] + 2), (3, 1)] + prime_factors_ij[1:]
    # else:
    #     if prime_factors_ij[0][0] == 3:
    #         prime_factors = [(2, 2), (3, prime_factors_ij[0][1] + 1)] + prime_factors_ij[1:]
    #     else:
    #         prime_factors = [(2, 2), (3, 1)] + prime_factors_ij
    # print(prime_factors)
    r_options = []
    # print(recursive_divisors(prime_factors))
    # print("sympy", sympy.ntheory.factor_.divisors(-ij))
    for i_opposite in sympy.ntheory.factor_.divisors(-ij, generator = True):
        i = -i_opposite
        j = ij//i
        x_numerator = i + j - 4*p
        if x_numerator <= 0 or x_numerator//8*8 != x_numerator:
            continue #Check for integer solutions
        y_numerator = j - i
        if y_numerator <= 0 or y_numerator//8*8 != y_numerator:
            continue #Check for integer solutions
        r_options.append(x_numerator//8)
    return r_options

N = 120000
L = [[] for _ in range(N//2 + 1)]
for p in range(N//2 + 1):
    if p%10000 == 0:
        print(p)
    L[p] = generate_r_from_p(p)

#Find solutions
print("Finding Solutions:")
solutions = set()
for p in range(len(L)):
    if p % 5000 == 0:
        print("Solutioning", p)
    if len(L[p]) > 1:
        for r in L[p]:
            if r < len(L):
                for q in L[r]:
                    if q in L[p]:
                        if (p+r+q <= N):
                            # print("Solution:", (p,r,q), p+r+q)
                            solutions.add(p+r+q)
print("SUMMING")
ans = sum(solutions)
print(ans)


