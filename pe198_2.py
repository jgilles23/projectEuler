import math
# import sympy

#Try to limit a for the next level of recursion so that we don't do more than is strictly necessary for recursive calls

# def get_bezout(a, b):
#     #Thank you wikipedia for this
#     old_r, r = a, b
#     old_s, s = 1, 0
#     old_t, t = 0, 1
    
#     while r != 0:
#         quotient = old_r//r
#         (old_r, r) = (r, old_r - quotient * r)
#         (old_s, s) = (s, old_s - quotient * s)
#         (old_t, t) = (t, old_t - quotient * t)
    
#     return (old_s, old_t)

# def generate_a_k_pairs(a_coeff, constant, denominator):
#     #Solve diophantine equation of the form:
#     # k = (a_coeff*a + constant)/denominator
#     # ASSUMES: gcd(a_coeff, consts) = 1!!!!
#     # Yields solutions in the form of (a, k)
#     #Uses bezout coefficients
#     bezout_0, bezout_1 = get_bezout(a_coeff, -1*denominator)
#     print("bezout:", (bezout_0, bezout_1))
#     print(f"a_5 = {-1*bezout_0*c_5} + {d_5}t")
#     print(f"k = {-1*bezout_1*c_5} + {b_5}t")
#     print(f"t > {bezout_0*c_5/d_5} AND t > {bezout_1*c_5/b_5}")
#     t = int(math.ceil(max(bezout_0*constant/denominator, bezout_1*constant/a_coeff)))
#     while True:
#         yield -1*bezout_0*constant + denominator*t, -1*bezout_1*constant + a_coeff*t
#         t += 1

# def brute_iterate_a(A_m2, A_m1, B_m2, B_m1, a = 1):
#     # Return False if failed on the first iteration
#     # Otherwise return True
#     while True:
#         A = A_m2 + A_m1*a
#         B = B_m2 = B_m1*a
#         #Test if we are done with this iteration
#         if B > B_limit:
#             return a == 1
#         a += 1


# def brute_force_solutions(zaro_lambda):
#     # k = (a_coeff*a + constant)/denominator
#     pass


# #Lets look at some maths
# B_limit = 1000
# K = 2
# L = 6
# k = sympy.symbols("k")
# a = [sympy.symbols(f"a{i}", integer=True, positive=True) for i in range(L + 1)]
# a[0] = 0

# def X(i, A_flag, k = 0):
#     if i == -1: 
#         return (1 if A_flag else 0)
#     elif i == 0: 
#         return (a[0] if A_flag else 1)
#     return X(i-2, A_flag) + (k if k else a[i])*X(i-1, A_flag)
# def A(i, k=0): 
#     return X(i, True, k)
# def B(i, k=0): 
#     return X(i, False, k)

# for K in range(4,5):
#     for L in range(5, 6):
#         # print(f"A({K})/B({K}) = {A(K)}/{B(K)}")
#         # print(f"A({K}, k)/B({K}, k) = {A(K,k)}/{B(K,k)}")
#         # print(f"A({L})/B({L}) = {A(L)}/{B(L)}")
#         zero = A(K)*B(L)*B(K+1, k) + A(K+1,k)*B(K)*B(L) - 2*A(L)*B(K)*B(K+1,k)
#         # print("0 =", zero.simplify())
#         k_solved = sympy.solve(zero, k)
#         # print(k_solved)
#         print(f"K: {K}, L: {L}, k = {k_solved[0].simplify()}")
#         # print(a[5])
#         # print(k_solved[0].collect(a[5]))
#         num = sympy.fraction(k_solved[0])
#         # a5_coeff = num[0].collect(a[5])
#         constant = num[0].coeff(a[5],0)
#         a5_coeff = num[0].coeff(a[5],1)
#         denominator = num[1]
#         print(f"k =\n  a5 * [{a5_coeff}] \n  + [{constant}] \n  / [{denominator}]")
#         print(f"Equation: [{a5_coeff}] * a5  +  [{denominator}] * k  =  [{constant}]")
#         lam = sympy.lambdify(a[1:], denominator)
#         print(lam(1,2,3,4,0,0))
#         a5_solved = sympy.solve(zero, a[5])
#         print(a5_solved)
#         # # print(k_solved[0].apart())
#         # print(k_solved[0].coeff(a[5],1))
#         # b3 = sympy.symbols("b3")
#         # k_solved_2 = k_solved[0].subs(a[3], a[1]*b3)
#         # print(k_solved_2.simplify())

# #Try a different method
# A_Km1, A_K, A_Lm2, A_Lm1 = sympy.symbols("A_Km1, A_K, A_Lm2, A_Lm1")
# B_Km1, B_K, B_Lm2, B_Lm1 = sympy.symbols("B_Km1, B_K, B_Lm2, B_Lm1")
# a_L, k = sympy.symbols("a_L, k")
# zero = A_K*(B_Lm2 + B_Lm1*a_L)*(B_Km1 + B_K*k) \
#      + (A_Km1 + A_K*k)*B_K*(B_Lm2 + B_Lm1*a_L) \
#      - 2*(A_Lm2 + A_Lm1*a_L)*B_K*(B_Km1 + B_K*k)
# zero = zero.expand()
# print()
# print("NEXT TEST")
# print(zero)
# a_k_power_matrix = [[0, 0], [0, 0]]
# a_k_power_matrix_names = [["F", "E"], ["D", "B"]]
# for a_L_power in range(0, 2):
#     for k_power in range(0, 2):
#         a_k_power_matrix[a_L_power][k_power] = zero.coeff(a_L, a_L_power).coeff(k, k_power)
#         print(f"{a_k_power_matrix_names[a_L_power][k_power]} coeff:  a_L**{a_L_power} * k**{k_power}  *  {a_k_power_matrix[a_L_power][k_power]}")
# ((Fc, Ec), (Dc, Bc)) = a_k_power_matrix
# right = Dc*Ec - Bc*Fc
# print("right", right.simplify())
# exit()

# high = 10**10
# B_limit = 10**4
# for a1 in range(100,high):
#     A1, B1 = 1, a1
#     if B1 > B_limit:
#         break
#     for a2 in range(1, high):
#         A2, B2 = a2, 1 + a2*B1
#         if B2 > B_limit:
#             break
#         for a3 in range(1,high):
#             A3, B3 = A1 + a3*A2, B1 + a3*B2
#             if B3 > B_limit:
#                 break
#             for a4 in range(1, high):
#                 A4, B4 = A2 + a4*A3, B2 + a4*A3
#                 if B4 > B_limit:
#                     break
#                 #Now we should be able to solve directly for a5


# # exit()

def continued_fraction(A, B):
    cf = []
    while B != 0:
        i = A//B
        A, B = B, A - i*B
        cf.append(i)
    return cf

def generate_convergents(cf, A_actual, B_actual):
    A_m2, A_m1 = 1, cf[0]
    B_m2, B_m1 = 0, 1
    yield (A_m1,B_m1), f"c({0})" #Yield back the 0th convergent
    for index, term in enumerate(cf[1:]):
        index += 1
        #Calculate A_n and B_n
        A = term*A_m1 + A_m2
        B = term*B_m1 + B_m2
        #Test to see if we have any better semiconvergents
        A_best, B_best = A_m1, B_m1
        m = 0
        while True:
            m += 1
            A_m = A_m2 + m*A_m1
            B_m = B_m2 + m*B_m1
            #Have reached A & B, no more semiconvergents
            if B_m >= B:
                break
            #Test if the semiconvergent is better than best found so far
            left = B_best*abs(A_actual*B_m - A_m*B_actual)
            right = B_m*abs(A_actual*B_best - A_best*B_actual)
            if left < right:
                A_best, B_best = A_m, B_m
                yield (A_m, B_m), f"s({index},{m})" #Semiconvergent
            elif left == right:
                if A_best == A_m1:
                    yield (A_m, B_m), f"c-s({index},{m}) ambiguous"
                else:
                    yield (A_m, B_m), f"s-s({index},{m}) ambiguous"
            #Test if the semiconvergent is as good as one of the convergents
            left = B*abs(A_actual*B_m - A_m*B_actual)
            right = B_m*abs(A_actual*B - A*B_actual)
            if left == right:
                yield (A_m, B_m), f"s({index})-c ambiguous"
        #yield convergent
        yield (A,B), f"c({index})" #Convergent
        #Setup next iteration
        A_m2, A_m1 = A_m1, A
        B_m2, B_m1 = B_m1, B

def generate_A_B_from_cf(cf):
    A_m2, A_m1 = 1, cf[0]
    B_m2, B_m1 = 0, 1
    for term in cf[1:]:
        A = term*A_m1 + A_m2
        B = term*B_m1 + B_m2
        A_m2, A_m1 = A_m1, A
        B_m2, B_m1 = B_m1, B
    return (A,B)

def run_test(A, B, print_level = 0):
    #Print level 0 == nothing, 1 == only when ambiguous, 2 == all convergents & semiconvergents & erros
    if math.gcd(A,B) > 1:
        if print_level == 2: print(f"{A}/{B}: gcd: {math.gcd(A,B)}")
        return False
    cf = continued_fraction(A,B)
    previous_string = ""
    is_ambiguous = False
    for (A_aprox, B_aprox), type in generate_convergents(cf, A, B):
        current_string = f"{A_aprox}/{B_aprox} {type}"
        #Calculate the +/- 
        A_scaled = A_aprox*(B//B_aprox)
        delta = abs(A - A_scaled)
        if "ambiguous" in type:
            is_ambiguous = True
            if print_level == 1: print(f"{A}/{B}: {cf} --- {previous_string} --- {current_string} --- +/-{delta}")
            pass
        if print_level == 2: print(f"{A}/{B}: {cf} --- {current_string}")
        previous_string = current_string
        A_previous, B_previous = A_aprox, B_aprox
    return is_ambiguous

def run_test_from_cf(cf, print_level = 0):
    A, B = generate_A_B_from_cf(cf)
    return run_test(A,B, print_level=print_level)


#Here is the new idea. We know that the convergent and the semi convergent share an average
#That average is A_L/B_L, where L is the ambiguous number
#A_L/B_L = (B_K1k*A_K + B_K*A_K1k) / (2*B_K1k*B_K)
# Where X_K1k is evaluation at K+1 with semiconvergent k

def recursive_parameter_k(i = 1, A_im1 = 1, A_i = 0, B_im1 = 0, B_i = 1, print_level = 0):
    count = 0
    if i == 1:
        k_min = int(math.ceil(A_max_ratio/2))
        a_min = A_max_ratio
    else:
        k_min = 1
        a_min = 1
    k_max = int(B_max/2/B_i**2 - B_im1/B_i)
    #Suppose the maximum value of a is at most the maximum value of k, but I think it is actually less
    for k in range(k_min, k_max + 1):
        #Assuming k, calcualte L, text if applicable
        A_ip1 = A_im1 + A_i*k
        B_ip1 = B_im1 + B_i*k
        A_L = B_ip1*A_i + B_i*A_ip1
        B_L = 2*B_ip1*B_i
        fast_set.add((A_L, B_L))
        count += 1
        is_ambiguous = run_test(A_L, B_L, print_level=print_level)
        if is_ambiguous == False:
            raise Exception("not actually ambiguous")
        elif B_L > B_max:
            raise Exception("B_L too large")
        # elif A_L == 1 and B_L >= B_max/2:
        #     #Edge case exception
        #     print(f"Exact ratio edge case {A_L}/{B_L} reducing count by 1.")
        #     fast_set.remove((A_L, B_L))
        #     fast_removed.add((A_L, B_L))
        #     count -= 1
        elif A_L >= B_L/A_max_ratio:
            if A_L == 1 and B_L == A_max_ratio:
                #Edge case exception
                # print(f"Exact ratio edge case {A_L}/{B_L} reducing count by 1.")
                fast_set.remove((A_L, B_L))
                fast_removed.add((A_L, B_L))
                count -= 1
            else:
                raise Exception("A_L too large")
        #Use k as a to not double count things
        if k >= a_min:
            count += recursive_parameter_k(i+1, A_i, A_ip1, B_i, B_ip1)
    return count

def recursive_parameter_k_faster(i = 1, A_im1 = 1, A_i = 0, B_im1 = 0, B_i = 1, print_level = 0):
    if i == 1:
        k_min = int(math.ceil(A_max_ratio/2))
        a_min = A_max_ratio
        count = -1 #Account for the 1/A_max_ratio
    else:
        k_min = 1
        a_min = 1
        count = 0
    k_max = int(B_max/2/B_i**2 - B_im1/B_i)
    #Directly count based on the values of k allowed
    count += k_max + 1 - k_min
    #Now iterate through the allowable "a"s
    #Suppose the maximum value of a is at most the maximum value of k, but I think it is actually less
    for a in range(a_min, k_max + 1):
        #Assuming k, calcualte L, text if applicable
        A_ip1 = A_im1 + A_i*a
        B_ip1 = B_im1 + B_i*a
        #Use k as a to not double count things
        result = recursive_parameter_k_faster(i+1, A_i, A_ip1, B_i, B_ip1)
        if result == 0:
            break
        count += result
    return count

#Set constants for the test
A_max_ratio = 100
B_max = 10**8

# brute_set = set()
# # # Test the two methods aganist each other
# count_brute = 0
# for B in range(1, B_max + 1):
#     if B%100 == 0:
#         print(B)
#     for A in range(1, int(math.ceil(B/A_max_ratio))):
#         result = run_test(A, B, print_level=0)
#         count_brute += result
#         if result:
#             brute_set.add((A, B))

fast_set = set()
fast_removed = set()
#Test the faster method
# count_fast = recursive_parameter_k(print_level = 0)
#Test the even faster method
count_faster = recursive_parameter_k_faster(print_level=0)

print()
# union_set = brute_set.intersection(fast_set)
# brute_unique = brute_set ^ union_set
# fast_unique = fast_set ^ union_set
# print(f"BRUTE: count: {count_brute}, set: {len(brute_set)}, unique: {len(brute_unique)} {brute_unique}")
# print(f"FAST: count: {count_fast}")#, set: {len(fast_set)}, unique: {len(fast_unique)} {fast_unique}")
# print(f"   removed: {len(fast_removed)} {fast_removed}")
print(f"FASTER: count: {count_faster}")

