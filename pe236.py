import math
import sympy
import random

random.seed(23)


c = [[5248, 640],
     [1312, 1888],
     [2624, 3776],
     [5760, 3776],
     [3936, 5664]]

q = math.lcm(*[c[i][1]//math.gcd(c[i][0], c[i][1]) for i in range(5)])
print(q)
print(1475/q)
print(sympy.factorint(5248), sympy.factorint(640))

"""
            b_A =     b_A' * gb_A * db_A     n = n' * gn_A     b_B
----------------------------------------  *  -------------  =  ------
c _ A = f * g_A = f * g_A' * gb_A * gn_A     d = d' * db_A     c_B = f * g_B
        x         x    1                     d = d_k * k            x

b_A' * n' = b_B     |     g_A' * d' = g_B
"""

#Find d_k = lcm(d'...) for all d'=g_B s.t. d = d_k * k
d_k = 1
for n in range(5):
    c_A, c_B = c[n][0], c[n][1]
    f = math.gcd(c_A, c_B)
    g_B = c_B // f
    d_k = math.lcm(d_k, g_B)
print(f"d = d_k[{d_k}] * k; d_k = {sympy.factorint(d_k)}")

n = 0
c_A, c_B = c[n][0], c[n][1] 
f = math.gcd(c_A, c_B)
g_A, g_B = c_A // f, c_B // f
g_A_p = 1 #Because gcd(g_A, g_B) = 1
for gb_A in sympy.divisors(g_A):
    d_p = g_B
    db_A_k = d_k // d_p # db_A = db_A_k * k
    gn_A = g_A // gb_A
    #Test that the spoilage of A is less than the count of the product
    # b_A' * db_A[db_A_k * k] <= f * g_A'[1] * gn_A
    b_A_p, k = 1, 1
    s = f"b_A'[{b_A_p}] * db_A_k[{db_A_k}] * k[{k}] <= f[{f}] * g_A'[1] * gn_A[{gn_A}]"
    s += f" | {b_A_p * db_A_k * k} <= {f * 1 * gn_A}"
    if b_A_p * db_A_k * k > f * 1 * gn_A:
        print(f"Failed A test for n={n}. {s}")
    else:
        print(f"Passed A test for n={n}. {s}")

print()
print("-------------------")
print()

c = {'a': [5248, 1312, 2624, 5760, 3936],
     'b': [640, 1888, 3776, 3776, 5664]}
c_A_sum = sum(c['a'])
c_B_sum = sum(c['b'])

count = [0]*5

def reduce(numerator, denominator):
    #Return new numerator, new denominator, and common facotor
    f = math.gcd(numerator, denominator)
    return numerator // f, denominator // f, f

def calc_b_A_k(i, n, d):
    #Let b_A = b_A' * g_A_b * d_b
    #    b_A = k    * b_A_k
    c_A, c_B = c['a'][i], c['b'][i]
    #Check that we have valid denominators
    if True and c_A * d % c_B != 0:
        #Denominator does not work
        raise Exception("Denominator does not work")
    g_A, g_B, f = reduce(c_A, c_B)
    g_A_b, n_p, g_A_n = reduce(g_A, n)
    d_b = d // g_B
    b_A_k = g_A_b * d_b
    b_B_k = n_p
    max_k = min(c_A // b_A_k, c_B // b_B_k)
    max_k = int(max_k)
    return b_A_k, b_B_k, max_k

def iterate_product(i, n, d):
    #Get out the c values
    c_A, c_B = c['a'][i], c['b'][i]
    #Check that we have valid denominators
    if True and c_A * d % c_B != 0:
        #Denominator does not work
        raise Exception("Denominator does not work")
    """
    b_A = b_A' * g_A_b * d_b     n = n' * g_A_n      b_B
    ------------------------  *  --------------  =  -------------
    c_A = f * g_A_b * g_A_n      d = d_b * g_B       c_B = f * g_B
    """
    g_A, g_B, f = reduce(c_A, c_B)
    g_A_b, n_p, g_A_n = reduce(g_A, n)
    d_b = d // g_B
    #Iterate through possible b_A'
    b_A_p = 1
    while True:
        b_A = b_A_p * g_A_b * d_b
        if b_A > c_A:
            break
        b_B = b_A_p * n_p
        if b_B > c_B:
            break
        #Check that we actually have a valid solution
        if True:
            b_B_check = b_A * n
            c_B_check = c_A * d
            b_B_check, c_B_check,_ = reduce(b_B_check, c_B_check)
            b_B_actual, c_B_actual, _ = reduce(b_B, c_B)
            if b_B_check != b_B_actual or c_B_check != c_B_actual:
                raise Exception("Invalid solution found")
        #Found a valid result
        yield b_A, b_B
        #Iterate
        b_A_p += 1

solutions = set()
expected_duration = 23065
i_test = 0
c_A, c_B = c['a'][i_test], c['b'][i_test]
for b_A in range(1, c_A+1):
    for b_B in range(1, c_B+1):
        n , d, _ = reduce(b_B * c_A, c_B * b_A)
        if n <= d:
            continue
        if d % d_k != 0:
            #Not valid because d must be divisible by d_k
            continue
        count[0] += 1
        if (n,d) in solutions:
            continue
        # if d != 1475 or n != 1476:
        #     continue
        #Now test the next level down
        for b_A_1, b_B_1 in iterate_product(1, n, d):
            count[1] += 1

            for b_A_2, b_B_2 in iterate_product(2, n, d):
                count[2] += 1

                for b_A_3, b_B_3 in iterate_product(3, n, d):
                    count[3] += 1

                    # for b_A_4, b_B_4 in iterate_product(4, n, d):
                    #     count[4] += 1
                    #     b_A_sum = b_A + b_A_1 + b_A_2 + b_A_3 + b_A_4
                    #     b_B_sum = b_B + b_B_1 + b_B_2 + b_B_3 + b_B_4
                    #     if random.randint(0, 1_000_000) == 0:
                    #         print(f"Solution m={n}/{d}, 0:{b_A}/{c_A}, 1:{b_A_1}/{c['a'][1]}, 2:{b_A_2}/{c['a'][2]}, 3:{b_A_3}/{c['a'][3]}, 4:{b_A_4}/{c['a'][4]} | count: {count}")
                    #     if b_A_sum * c_B_sum * d == b_B_sum * c_A_sum * n:
                    #         print(f"******** FOUND ONE! Solution m={n}/{d}, 0:{b_A}/{c_A}, 1:{b_A_1}/{c['a'][1]}, 2:{b_A_2}/{c['a'][2]}, 3:{b_A_3}/{c['a'][3]}, 4:{b_A_4}/{c['a'][4]} | count: {count}")
                    #         continue
                    
                    if random.randint(0, 5_000_000) == 0:
                        print(f"Solution m={n}/{d}, 0:{b_A}/{c_A}, 1:{b_A_1}/{c['a'][1]}, 2:{b_A_2}/{c['a'][2]}, 3:{b_A_3}/{c['a'][3]} | count: {count} | {expected_duration}")

                    #Direct solve for b_A_4, and b_B_4
                    b_A_sum3 = b_A + b_A_1 + b_A_2 + b_A_3
                    b_B_sum3 = b_B + b_B_1 + b_B_2 + b_B_3
                    c_A_4, c_B_4 = c['a'][4], c['b'][4]
                    R = n * c_A_sum * b_B_sum3 - d * c_B_sum * b_A_sum3
                    Q = d * c_A_4
                    b_A_4_numerator = Q*R
                    b_A_4_denominator = Q*d*c_B_sum - n*c_A_sum*n*c_B_4
                    if b_A_4_numerator % b_A_4_denominator != 0:
                        #No solution for b_A_4, so skip
                        continue
                    b_A_4 = b_A_4_numerator // b_A_4_denominator
                    if b_A_4 < 0:
                        continue #Cannot be negitive
                    b_B_4_numerator = b_A_4 * n * c_B_4
                    b_B_4_denominator = c_A_4 * d
                    if b_B_4_numerator % b_B_4_denominator != 0:
                        #No solution for b_B_4, so skip
                        continue
                    b_B_4 = b_B_4_numerator // b_B_4_denominator
                    if b_B_4 < 0:
                        continue #Cannot be negitive
                    count[4] += 1
                    sol = (n,d)
                    if sol not in solutions:
                        print(f"******** FOUND ONE! Solution m={n}/{d}, 0:{b_A}/{c_A}, 1:{b_A_1}/{c['a'][1]}, 2:{b_A_2}/{c['a'][2]}, 3:{b_A_3}/{c['a'][3]}, 4:{b_A_4}/{c['a'][4]} | count: {count}")
                        solutions.add(sol)
                        print(solutions)

print(count)
print(solutions)
print(len(solutions))
biggest_val = 0
biggest_sol = None
for sol in solutions:
    n, d = sol
    if n/d > biggest_val:
        biggest_val = n/d
        biggest_sol = sol
print(f"Biggest solution: m={biggest_sol[0]}/{biggest_sol[1]} = {biggest_val}")


#******** FOUND ONE! Solution m=1476/1475, 0:2065/5248, 1:1200/1312, 2:1450/2624, 3:2750/5760, 4:575/3936 | count: [18000, 360, 37394, 1720100, 270055566]
#FOUND 14 {(1353, 1180), (861, 590), (1066, 885), (1722, 1475), (492, 295), (1476, 1475), (3321, 3245), (369, 295), (451, 295), (902, 885), (574, 295), (328, 295), (697, 590), (1599, 1180)}
#574/295 incorrect