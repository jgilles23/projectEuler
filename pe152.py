import sympy
import math
import itertools

# N = 45
# A = [sympy.Rational(1)/sympy.Rational(x**2) for x in range(2,N+1)]
# print(A)
# s = sum(A)
# print(s)
# numerator, denominator = sympy.fraction(s)
# print(sympy.fraction(s))
# # Numerators of the combined fraction
# B = [denominator/x**2 for x in range(2,N+1)]
# print(B)
# print(denominator/2)

N = 80

# A = [x**2 for x in range(2,N+1)]
# lcm = math.lcm(*A)
# print("lcm:", lcm)
# numerators = [(lcm//x**2) for x in range(2, N+1)]
# print("numerators:", numerators)
# print("target:", lcm//2)

usable_integers = [x for x in range(N+1)]
usable_integers[1] = 0
print(usable_integers)
primes = list(sympy.primerange(2,N+1))
print(primes)

def test_combination(combination, primary_divisor):
    lcm = math.lcm(*combination)
    sum_numerators = sum((lcm**2//x**2) for x in combination)
    return sum_numerators % primary_divisor**2 == 0

def test_partner_combinations(partners, primary_divisor):
    print("Testing partners:", partners)
    # Test to what combinations of partners are able to form a diviable sequence
    used_in_successful_combination = {x:False for x in partners}
    successful_combinations = {} #key: combination, value: sum of inverse squares
    for r in range(2, len(partners) + 1):
        for combination in itertools.combinations(partners, r):
            if test_combination(combination, primary_divisor):
                s = 0
                for c in combination:
                    used_in_successful_combination[c] = True
                    s += 1/c**2
                print("    pass:", combination, "sum:", s)
    return used_in_successful_combination

for i in range(N, 1, -1):
    #Don't look at non-perfect powers and non-primes
    prime_factors = sympy.ntheory.primefactors(i)
    if len(prime_factors) > 1:
        continue
    #For perfect powers test partners
    partners = [i*x for x in range(1, N//i + 1) if usable_integers[i*x] != 0 ]
    if len(partners) <= 1:
        usable_integers[i] = 0
        print("Eliminate: {}, possible partners already eliminated".format(i))
        continue
    #Test the combinations of partners
    if len(partners) < 10:
        used_in_successful_combination = test_partner_combinations(partners, prime_factors[0])
        for j in used_in_successful_combination:
            if used_in_successful_combination[j] == False:
                usable_integers[j] = 0
                print("Eliminate: {}, not used in a combination".format(j))
    else:
        print("partners:", partners)

print("Useable integers:", usable_integers)
usable_integers = [c for c in usable_integers if c > 0]
print("Useable integers:", usable_integers)
print("    count:", len(usable_integers))

#Calculate inverse and forward and backward sums
inverse_integers = [1/c**2 for c in usable_integers]
s = 0
forward_cumulative = []
for x in inverse_integers:
    s += x
    forward_cumulative.append(s)
s = 0
backward_cumulative = []
for x in inverse_integers[::-1]:
    s += x
    backward_cumulative.append(s)
backward_cumulative = backward_cumulative[::-1] + [0]

print("inverse", inverse_integers)
print("forward", forward_cumulative)
print("backward", backward_cumulative)

error = 10**-9

def recursive_step(previous_sum=0, i=0):
    #Recursively iterate through each possible combination of the value being in or out of the sum
    #Test i too large
    if i >= len(usable_integers):
        # Reached the end of the avaliable integers with no solution
        return False
    solutions = []
    n = usable_integers[i]
    v = inverse_integers[i]
    # i is part of the sum
    s = previous_sum + v
    if s > 0.5 + error:
        # Too big, end the search
        pass
    elif s > 0.5 - error:
        # Found a result, end the search
        solutions.append([n])
    elif s + backward_cumulative[i+1] < 0.5 - error:
        # Will never reach the result
        pass
    else:
        # Made it through call recursive on the next entry
        ret = recursive_step(s, i + 1)
        if ret != False:
            for sol in ret:
                solutions.append([n] + sol)
    # test i is not part of the sum
    ret = recursive_step(previous_sum, i + 1)
    if ret != False:
        for sol in ret:
            solutions.append(sol)
    return solutions

q = recursive_step()
print(q)
print("ans", len(q))