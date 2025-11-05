#Found a simpler way
#(a+b)(a+c)/(bc) = k; k = [2, 3, 4]
import math
import numpy as np

N = 1*10**8

count_slow = [0]*5
if N < 10**4:
    for a in range(1, N + 1):
        for b in range(a, N + 1 - 2*a):
            for c in range(b, N + 1 - a - b):
                if a + b <= c:
                    break
                if ((a + b)*(a + c)) % (b*c) == 0:
                    count_slow[((a + b)*(a + c))//(b*c)] += 1
    print("slow complete")


# count_double_fast = 0

# m = 1
# while 2*m**2 + 1*m <= N:
#     f = 1
#     while f**2 + f*m <= N and 2*m**2 + f*m <= N:
#         if f**2 > 2*m**2: #This gets worse as f gets bigger
#             break
#         if 2*m**2 >= f**2 + m*f: #This gets better as f gets bigger
#             f += 1
#             continue
#         #We have found a solution for n nonsquare and odd
#         # print(f"Solution: (a = {f*m}n, b = {f**2 +f*m}n, c = {2*m**2 + f*m}n) with (f = {f}, m = {m}) and (d = {f**2}n, d' = {2*m**2}n)")
#         #Count the number of actual solutions
#         n = 1
#         while (2*m**2 + f*m)*n <= N:
#             #Check if n is nonsquare
#             for i in range(2, math.isqrt(n) + 1):
#                 if n//i**2 * i**2 == n:
#                     break
#             else:
#                 count_double_fast += 1
#                 # print(f"  n = {n}, (a = {f*m*n}, b = {(f**2 + f*m)*n}, c = {(2*m**2 + f*m)*n})")
#             n += 2

#         f += 1
#     m += 1 

# print()

# m = 1
# while m**2 + 1*m <= N:
#     f = 1
#     while 2*f**2 + f*m <= N and m**2 + f*m <= N:
#         if 2*f**2 > m**2: #This gets worse as f gets bigger
#             break
#         if m**2 >= 2*f**2 + m*f: #This gets better as f gets bigger
#             f += 1
#             continue
#         #We have found a solution for n nonsquare and odd
#         # print(f"Solution: (a = {f*m}n, b = {2*f**2 + f*m}n, c = {m**2 + f*m}n) with (f = {f}, m = {m}) and (d = {2*f**2}n, d' = {m**2}n)")
#         #Count the number of actual solutions
#         n = 1
#         while (m**2 + f*m)*n <= N:
#             #Check if n is nonsquare
#             for i in range(2, math.isqrt(n) + 1):
#                 if n//i**2 * i**2 == n:
#                     break
#             else:
#                 count_double_fast += 1
#                 # print(f"  n = {n}, (a = {f*m*n}, b = {(f**2 +f*m)*n}, c = {(2*m**2 + f*m)*n})")
#             n += 2

#         f += 1
#     m += 1 
# print("fast:", count_double_fast)


# def count_scenario(k, kb_flag):
#     count = 0
#     #Set kb*kbp = k
#     if kb_flag: 
#         kb, kbp = k, 1
#     else:
#         kb, kbp = 1, k
#     #Iterate through all options for m & f
#     m = 1
#     while (1*m + kbp*m**2)/(k-1) <= N:
#         f = 1
#         while (f*m + kbp*m**2)/(k-1) <= N and (f*m + kb*f**2)/(k-1) <= N:
#             if kb*f**2 > kbp*m**2: #This gets worse as f gets bigger
#                 break
#             if kbp*m**2 >= m*f + kb*f**2: #This gets better as f gets bigger
#                 f += 1
#                 continue
#             #We have found a solution for n nonsquare and not divisible by k
#             a = f*m
#             b_num = f*m + kb*f**2
#             c_num = f*m + kbp*m**2
#             # print(f"k: {kb}|{kbp}, solution: (a = {f*m}n, b = {b_num}n/{k-1}, c = {c_num}n/{k-1}) with (f = {f}, m = {m}) and (d = {kb*f**2}n, d' = {kbp*m**2}n)")
#             #Check if n must be a multiple of k-1
#             #Count the number of actual solutions
#             n = 1
#             while c_num*n/(k-1) <= N:
#                 # Ensure n is not divisible by k
#                 if n % k == 0:
#                     n += 1
#                     continue
#                 # Ensure that the divisibility rules work
#                 if (b_num*n) % (k-1) != 0 or (c_num*n) % (k-1) != 0:
#                     n += 1
#                     continue
#                 #Check if n is nonsquare
#                 for i in range(2, math.isqrt(n) + 1):
#                     if n//i**2 * i**2 == n:
#                         break
#                 else:
#                     count += 1
#                     # print(f"  n = {n}, (a = {f*m*n}, b = {b_num*n/(k-1)}, c = {c_num*n/(k-1)})")
#                 n += 1
#             f += 1
#         m += 1
#     return count


nonsquare_flags = [[]]
#Access via cumsums[k][require_even]
cumsums = [[[], []] for _ in range(4)]

def get_fast_n(n_max, k, require_even = False, check_q = []):
    #Check if new cumsum needs to be generated
    if n_max >= len(cumsums[k][require_even]):
        #Check if new nonsquare flags need to be generated
        if n_max >= len(nonsquare_flags[0]):
            print(f"Increasing nonsquareflags to {n_max}", end="... ")
            nonsquare_flags[0] = np.full(n_max + 1, True)
            nonsquare_flags[0][0] = False
            for i in range(2, math.isqrt(n_max) + 1):
                nonsquare_flags[0][i**2::i**2] = False
            print("complete.")
        #Generate new cumsum
        print(f"Increasing cumsums[k = {k}][even = {require_even}] to {n_max}", end="... ")
        q = nonsquare_flags[0].copy()
        q[k::k] = False
        if require_even:
            q[1::2] = False
        cumsums[k][require_even] = np.cumsum(q)
        print("complete.")
        if check_q:
            for x, y in zip(q[:n_max+1], check_q[:n_max+1]):
                if x != y:
                    raise Exception("Alignment issue.")
    return int(cumsums[k][require_even][n_max])


def count_scenario_2(kb, kbp, fast_n_flag = True, fast_n_check = False):
    k = kb*kbp
    count = 0 
    f = 0
    while True: #f loop
        f += 1
        # Confirm a <= b
        if (k-2)*f*1 > kb*f**2:
            break #f too large
        # Confirm a + 2 + b <= N; assuming m = 1, n = 1
        if (k+1)*f*1 + 2*kb*f**2 > N*(k-1):
            break #f too large
        m = 0
        while True: #m loop
            m += 1
            # Confirm a <= b
            if (k-2)*f*m > kb*f**2:
                break #m too large
            # Confirm b <= c
            if kb*f**2 > kbp*m**2:
                continue #m too small
            # Confirm a + b + c <= N asssuming n = 1
            if (k+1)*f*m + kb*f**2 + kbp*m**2 > N*(k-1):
                break #m too large
            # Confirm c < a + b
            if kbp*m**2 >= (k-1)*f*m + kb*f**2:
                continue #Not sure if m too small or too large
            #Now Iterate through allowable n
            n = 0
            if fast_n_flag:
                n_max = N*(k-1)//((k+1)*f*m + kb*f**2 + kbp*m**2)
                require_even = (k == 3 and (math.gcd(f*m + kb*f**2, 2) == 1 or math.gcd(f*m + kbp*m**2, 2) == 1))
                if n_max == 1:
                    if require_even == False:
                        count += 1
                else:
                    count += get_fast_n(n_max, k, require_even)
            else:
                if fast_n_check:
                    q = [False]
                while True:
                    n += 1
                    if fast_n_check:
                        q.append(False)
                    # c <= N
                    if ((k-1)*f*m + f*m + kb*f**2 + f*m + kbp*m**2)*n > N*(k-1):
                        break #n too large
                    # gcd(n, k) == 1
                    if math.gcd(n, k) != 1:
                        continue #Divisible by k
                    # Check b divisibility
                    if (f*m + kb*f**2)*n % (k-1) != 0:
                        continue #Not an integer
                    # Check c divisibility
                    if (f*m + kbp*m**2)*n % (k-1) != 0:
                        continue #Not an integer
                    # Check non-square
                    for i in range(2, math.isqrt(n) + 1):
                        if n % i**2 == 0:
                            break
                    else:
                        #Encountered a solution
                        if fast_n_check:
                            q[-1] = True
                        count += 1
                        # print(f"  n = {n}, (a = {f*m*n}, b = {(f*m + kb*f**2)*n/(k-1)}, c = {(f*m + kbp*m**2)*n/(k-1)})")
                if fast_n_check:
                    get_fast_n(N*(k-1)//(f*m + kbp*m**2), k, k == 3 and (math.gcd(f*m + kb*f**2, 2) == 1 or math.gcd(f*m + kbp*m**2, 2) == 1), q)
    return count

count_fast = [0]*5
for k in [2, 3]:
    count_fast[k] += count_scenario_2(k, 1, True, True)
    count_fast[k] += count_scenario_2(1, k, True, True)
count_fast[4] = N//3
print("slow:", count_slow, sum(count_slow))
print("new:", count_fast, sum(count_fast))
#356760665 is incorrect

# import sympy
# from sympy import sin, cos

# def law_of_cosines_for_A(a, b, c):
#     #Return angle A of triangle ABC given opposite sides a, b, c
#     A = sympy.asin((b**2 + c**2 - a**2)/(2*b*c))
#     return A

# def law_of_cosines_for_a(A, b, c):
#     a = sympy.sqrt(b**2 + c**2 - 2*b*c*sympy.cos(A))
#     return a

# def law_of_sines_for_a(A, B, b):
#     #Return side length a of triangle ABC where angles A & B and side length b is given
#     a = sympy.sin(A)*b/sympy.sin(B)
#     return a

# a, b, c = sympy.symbols("a b c", positive = True, real = True)

# A = law_of_cosines_for_A(a, b, c)
# A = sympy.symbols("A")

# h = law_of_sines_for_a(A, sympy.pi/2, b)

# area_ABC = c*h/2

# C = sympy.symbols("C", positive = True, real = True)/2
# ACE = C/2 #law_of_cosines_for_A(c, a, b)/2
# AEC = 2*sympy.pi - A - ACE
# AE = law_of_sines_for_a(ACE, AEC, b) #Bottom of smaller triange

# B = sympy.symbols("B", positive = True, real = True)/2
# ABG = B/2 #law_of_cosines_for_A(b, a, c)/2
# AGB = 2*sympy.pi - A - ABG
# AG = law_of_sines_for_a(ABG, AGB, c)

# EG = law_of_cosines_for_a(A, AE, AG)
# AEG = law_of_cosines_for_A(AG, AE, EG)
# k = law_of_sines_for_a(A, AEG, AG)

# area_AEG = AE*k/2

# ratio = area_ABC/area_AEG
# ratio = ratio.simplify()
# print(ratio)

# # (-b*sin(C/4)*sin(A + B/4) 
# # + c*sin(B/4)*sin(A + C/4)*cos(A))
# # /
# # (sqrt(b**2*sin(C/4)**2/sin(A + C/4)**2 
# # - 2*b*c*sin(B/4)*sin(C/4)*cos(A)/(sin(A + B/4)*sin(A + C/4)) 
# # + c**2*sin(B/4)**2/sin(A + B/4)**2)*sin(B/4)*sin(C/4))

# ratio2 = ratio
# W = sympy.symbols("W")
# ratio2 = ratio2.subs(B, W)
# print(ratio2)
# # ratio2 = ratio2.subs(sin(w), sympy.sqrt((1 - sympy.cos(C/2))/2))
# # print(ratio2)

# #Perform substitutions for double and half angle formulas