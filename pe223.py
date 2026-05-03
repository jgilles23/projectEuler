#a^2 + b^2 = c^2 + 1
#This likely forms a diophantine equation
#a^2 + b^2 - c^2 + 1 = 0
#T congruent to -1 mod p | has 2 solutions if p congruent to 1 mod 4, 0 solutions if p congruent to 3 mod 4, and 1 solution if p = 2
#Based on the number of solutions of this equation, we can determine the number of ways those combine
#Via the chinese remainder theorm, to calcualte the number of solutions of the overall interger equations
#Without having to actually solve those equations

import math

import sympy


def brute_force(c):
    count = 0
    a_max = math.isqrt((c**2 + 1)//2)
    for a in range(1, a_max+1):
        b_implied = math.isqrt(c**2 + 1 - a**2)
        if a + b_implied <= c+1:
            continue
        if a**2 + b_implied**2 == c**2 + 1:
            count += 1
    return count

def CRT_solution_count(prime_factor_dict):
    solution_count = 1
    for p, multiplicity in prime_factor_dict.items():
        if multiplicity == 0:
            continue
        value = p**multiplicity
        if value%4 == 1:
            solution_count *= 2
        elif value == 2:
            solution_count *= 1
        else:
            solution_count *= 0
    return solution_count - 2

def fast_CRT_solution_count(prime_factor_dict):
    #For each prime factor, 
    solution_count = 2**len(prime_factor_dict)
    if 2 in prime_factor_dict:
        if prime_factor_dict[2] >= 2:
            raise ValueError(f"ERROR: prime factor 2 has multiplicity {prime_factor_dict[2]}, which is not allowed")
            return 0
        else:
            solution_count //= 2
    return solution_count - 2

def better_fast_CRT(prime_factor_dict):
    solution_counts = [1]
    for p, multiplicity in prime_factor_dict.items():
        if p == 2:
            continue
        if multiplicity % 2 == 1:
            solution_counts = [x*2*((multiplicity+1)//2) for x in solution_counts]
        else:
            solution_counts = [x for x in solution_counts] + [x*2*(multiplicity//2 - 1) for x in solution_counts]
    solution_counts = [x - 2 if x > 2 else 0 for x in solution_counts]
    return sum(solution_counts)

def recursive_removal(prime_factor_dict):
    solution_count = CRT_solution_count(prime_factor_dict)
    for p, multiplicity in prime_factor_dict.items():
        if multiplicity >= 2:
            prime_factor_dict_copy = prime_factor_dict.copy()
            prime_factor_dict_copy[p] = multiplicity - 2
            solution_count += recursive_removal(prime_factor_dict_copy)
    return solution_count

def CRT_brute_solver(modulus):
    solution_count = 0
    for a in range(1, modulus+1):
        if (a**2 + 1) % modulus == 0:
            solution_count += 1
    return solution_count

def CRT_smart_solver(modulus):
    prime_factor_dict = sympy.factorint(modulus)
    if 2 in prime_factor_dict:
        return 2**(len(prime_factor_dict)-1)
    else:
        return 2**len(prime_factor_dict)
    
def CRT_factor_solver(factor_multiplicity):
    if factor_multiplicity[0][0] == 2:
        return 2**(len(factor_multiplicity)-1)
    else:
        return 2**len(factor_multiplicity)

def single_eval(c):
    solution_count = 0
    right = c**2 + 1
    for i in range(1, math.isqrt(right)+1):
        if right % i**2 == 0:
            delta = CRT_smart_solver(right//i**2)
            if delta == 1:
                solution_count += 1
            else:
                solution_count += delta//2
    #Remove the double counting of the trivial solution where a=1, b=c
    solution_count -= 1
    #Need to provide reductions of the space based on squared similifications
    return solution_count

def recursive_square_removal(factor_multiplicity, index=0):
    if index >= len(factor_multiplicity):
        yield factor_multiplicity
    else:
        #Else, iterate through avaible multiplicities
        for multiplicity in range(factor_multiplicity[index][1], -1, -2):
            factor_multiplicity_copy = factor_multiplicity.copy()
            if multiplicity == 0:
                factor_multiplicity_copy.pop(index)
                new_index = index
            else:
                factor_multiplicity_copy[index] = (factor_multiplicity_copy[index][0], multiplicity)
                new_index = index + 1
            yield from recursive_square_removal(factor_multiplicity_copy, new_index)

def single_eval_2(c):
    solution_count = 0
    right = c**2 + 1
    factor_multiplicity = list(sympy.factorint(right).items())
    for fm in recursive_square_removal(factor_multiplicity):
        delta = CRT_factor_solver(fm)
        if delta == 1:
            solution_count += 1
        else:
            solution_count += delta//2
    #Remove the double counting of the trivial solution where a=1, b=c
    solution_count -= 1
    #Need to provide reductions of the space based on squared similifications
    return solution_count

N = 100
for c in range(2, N):
    if c % 100 == 0:
        print(f"Comparing for c: {c}")
    brute_force_count = brute_force(c)
    single_eval_count = single_eval_2(c)
    if brute_force_count != single_eval_count:
        print(f"c: {c}, brute_force: {brute_force_count}, single_eval: {single_eval_count}")
print(f"Comparison complete for c in range({2},{N})")

# for factor_multiplicity in recursive_square_removal(list(sympy.factorint(2 * 3**5 * 5**4 * 13).items())):
#     print(factor_multiplicity, CRT_factor_solver(factor_multiplicity))

N = 25_000
ans = 0
for c in range(2, N+1):
    single_eval_count = single_eval_2(c)
    ans += single_eval_count
    if c % 10_000 == 0:
        print(f"c: {c}, single_eval: {single_eval_count}, ans: {ans}")
        
print(f"Complete for c in range({2},{N+1})")
print(f"Final answer: {ans}")

for c in range(2, 25_000_000 + 1):
    if c % 100_000 == 0:
        print(f"Comparing for c: {c}")
    sympy.factorint(c)
print("Done with factorization")