import math
import sympy
from itertools import combinations

def evaluate_brute(bounces):
    depth = (bounces+3)//2
    solution_count = 0
    if depth%2 == 0:
        width = 0
    else:
        width = 3
    while width <= depth:
        g = math.gcd(width, depth)
        if g == 1:
            solution_count += 1
        else:
            numerator = width//g
            denominator = depth//g
            if numerator%2 == denominator%2:
                pass
            else:
                if numerator*2 < depth and denominator*2 < depth:
                    pass
                else:
                    solution_count += 1
        width += 6
    print(f"BRUTE: bounces: {bounces}, depth: {depth}, solution_count: {solution_count*2}")
    return solution_count*2

def count_in_range(start, spacing, limit):
    if start >= limit:
        return 0
    return (limit - start)//spacing + 1

def evaluate_odd(bounces, printFlag=False):
    depth = (bounces+3)//2
    if depth%2 == 0:
        if printFlag:
            print(f"ODD : bounces: {bounces}, depth: {depth}, cannot evaluate, depth is even")
        return
    factors = sympy.primefactors(depth)
    if 3 in factors:
        if printFlag:
            print(f"ODD : bounces: {bounces}, depth: {depth}, factors: {factors}, cannot evaluate, factors include 3")
        return
    solution_count = (depth - 3)//6 + 1
    if printFlag:
        print(f"solution_count: {solution_count}")
    # width = 3
    # intersect_5 = 0
    # while width <= depth:
    #     if math.gcd(width, depth) != 1:
    #         solution_count -= 1
    #         if width%5 == 0:
    #             intersect_5 += 1
    #     width += 6
    # print(f"intersect_5: {intersect_5}")
    for i_start in range(0, len(factors)):
        for i_end in range(i_start, len(factors)):
            sign = (-1)**(i_end - i_start + 1)
            p = math.prod(factors[i_start:i_end+1])
            count = count_in_range(3*p, 3*p*2, depth)
            solution_count += sign*count
            if printFlag:
                print(f"[{i_start}:{i_end}] sign: {sign}, count: {count}, factors: {factors[i_start:i_end+1]}, solution_count: {solution_count*2}")
    if printFlag:
        print(f"ODD : bounces: {bounces}, depth: {depth}, factors: {factors}, solution_count: {solution_count*2}")
    return solution_count*2

def factor_groups(factors):
    for length in range(1, len(factors)+1):
        for group in combinations(factors, length):
            sign = (-1)**length
            p = math.prod(group)
            yield (sign, p, group)

def multi_evaluation(bounces, indicate_return=False, brute_check=True):
    #This function will either perform a brute force check and compare to a faster approach if avaliable, or it will just perform the faster check
    depth = (bounces+3)//2
    factors = sympy.primefactors(depth)
    if depth%2 == 0:
        mode = "even"
    elif 3 in factors:
        mode = "odd_3"
    else:
        mode = "odd_no_3"
    #If indicate return, return without evaluation
    if indicate_return:
        return mode
    #Run the brute evaluation if requested
    if brute_check:
        #Record the types of each solution
        baseline = 0
        divisor_dict = {}
        for _, p, _ in factor_groups(factors):
            divisor_dict[p] = 0
        solution_count = 0
        if depth%2 == 0:
            width = 0
        else:
            width = 3
        while width <= depth:
            baseline += 1
            g = math.gcd(width, depth)
            if g == 1:
                solution_count += 1
            else:
                numerator = width//g
                denominator = depth//g
                if numerator%2 == denominator%2:
                    check_flag = False
                    for p in divisor_dict.keys():
                        if width%p == 0:
                            divisor_dict[p] += 1
                            check_flag += 1
                    if not check_flag:
                        print(f"ERROR: width: {width}, depth: {depth}, numerator: {numerator}, denominator: {denominator}, divisor_dict: {divisor_dict}")
                    if check_flag % 2 == 0 and check_flag > 0:
                        print(f"ERROR: width: {width}, depth: {depth}, numerator: {numerator}, denominator: {denominator}, divisor_dict: {divisor_dict}")
                    pass
                else:
                    if numerator*2 < depth and denominator*2 < depth:
                        check_flag = False
                        for p in divisor_dict.keys():
                            if width%p == 0:
                                divisor_dict[p] += 1
                                check_flag += 1
                        if not check_flag:
                            print(f"ERROR: width: {width}, depth: {depth}, numerator: {numerator}, denominator: {denominator}, divisor_dict: {divisor_dict}")
                        if check_flag % 2 == 0 and check_flag > 0:
                            print(f"ERROR: width: {width}, depth: {depth}, numerator: {numerator}, denominator: {denominator}, divisor_dict: {divisor_dict}")
                        pass
                    else:
                        solution_count += 1
            width += 6
        print(f"BRUTE: bounces: {bounces}, depth: {depth}, solution_count: {solution_count*2}, divisor_dict: {divisor_dict}")
    #Fast solution
    if mode == "odd_no_3":
        solution_count = (depth - 3)//6 + 1
        if brute_check:
            print(f"baseline: {baseline}, solution_count: {solution_count}")
        for sign, p, factor_subset in factor_groups(factors):
            count = count_in_range(3*p, 3*p*2, depth)
            solution_count += sign*count
            if brute_check:
                print(f"brute_check: {divisor_dict[p]}, sign: {sign}, count: {count}, factors: {factor_subset}, solution_count: {solution_count}")
        print(f"ODD_NO_3 : bounces: {bounces}, depth: {depth}, factors: {factors}, solution_count: {solution_count*2}")

evaluate_brute(1000001)
evaluate_odd(1000001)
print("----------------------------------")
q = 200027
for i in range(0,8,2):
    if multi_evaluation(q+i, indicate_return=True) is "odd_no_3":
        multi_evaluation(q+i, brute_check=True)

print("----------------------------------")
multi_evaluation(12017639147, brute_check=False)