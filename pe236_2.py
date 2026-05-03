import math
import sympy
import random

def reduce(numerator, denominator):
    #Return new numerator, new denominator, and common facotor
    f = math.gcd(numerator, denominator)
    return numerator // f, denominator // f, f

def divisor_pairs(n):
    for i in sympy.divisors(n):
        yield i, n//i


c = {'a': [5248, 1312, 2624, 5760, 3936],
     'b': [640, 1888, 3776, 3776, 5664]}
c_A_sum = sum(c['a'])
c_B_sum = sum(c['b'])


m_options = set()
i_test = 0
c_A, c_B = c['a'][i_test], c['b'][i_test]
for b_A in range(1, c_A+1):
    for b_B in range(1, c_B+1):
        n , d, _ = reduce(b_B * c_A, c_B * b_A)
        if n <= d:
            continue
        m_options.add((n, d))
print(f"m options: {len(m_options)}")

def yield_x_max_k(I, n, d):
    i = I[0]
    cA, cB = c['a'][i], c['b'][i]
    gA, gB, f = reduce(cA, cB)
    for gA_bA, gA_n in divisor_pairs(gA):
        if n % gA_n != 0: 
            continue
        np = n // gA_n
        for gB_bB, gB_d in divisor_pairs(gB):
            if d % gB_d != 0: 
                continue
            dp = d // gB_d
            bAk =  dp * gA_bA
            bBk = np * gB_bB
            max_k = 0
            for j in I:
                sub_max_k = min(c['a'][j] // bAk, c['b'][j] // bBk)
                if sub_max_k < 1:
                    break
                max_k += sub_max_k
            else:
                #All k_max > 0
                x = d*c_B_sum*bAk - n*c_A_sum*bBk
                yield x, max_k

solutions = set()

def run_on_m(n, d):
    for x0, kmax0 in yield_x_max_k([0], n, d):
        for x3, kmax3 in yield_x_max_k([3], n, d):
            for xr, kmaxr in yield_x_max_k([1, 2 ,4], n, d):
                #Cannot all be the same sign
                if (x0<0 and x3<0 and xr<0) or (x0>0 and x3>0 and xr>0):
                    continue
                #Reduce if possible
                g = math.gcd(math.gcd(x0, x3), xr)
                x0, x3, xr = x0//g, x3//g, xr//g
                #Find kr that solves the equation x0*k0 + x3*k3 + xr*kr = 0, where kr is an integer between 1 and kmaxr
                for k0 in range(1, kmax0+1):
                    for k3 in range(1, kmax3+1):
                        kr_numerator = -1*(x0*k0 + x3*k3)
                        if kr_numerator % xr == 0:
                            kr = kr_numerator // xr
                            if 3 <= kr and kr <= kmaxr:
                                print(f"FOUND Solution m={n}/{d}, x0*k0={x0}*{k0}, x3*k3={x3}*{k3}, xr*kr={xr}*{kr}")
                                solutions.add((n/d, n, d))
                                return True
    return False

solutions_count = 0
for m in m_options:
    n, d = m
    solutions_count += run_on_m(n, d)
print(f"Total solutions found: {solutions_count}")

#Sort solutions from largest to smalles
solutions = sorted(solutions, reverse=True)
print(f"Highest m: {solutions[0][0]} = {solutions[0][1]}/{solutions[0][2]}")
    


#******** FOUND ONE! Solution m=1476/1475, 0:2065/5248, 1:25/1312, 2:25/2624, 3:1125/5760, 4:2700/3936 | count: [14267, 204362, 18976580, 246949674, 4314]
