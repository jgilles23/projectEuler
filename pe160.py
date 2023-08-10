from __future__ import annotations
import math


def reduce(x, m):
    while (x % 10) == 0:
        x = x // 10
    return x % (10**m)

def mult(a,b,m):
    if a % 5 == 0 or b % 5 == 0:
        raise Exception("Cannot safetly multiply multiples of 5.")
    return reduce(reduce(a, m) * reduce(b, m), m)

class Shifter:

    def __init__(self, max_n, m):
        self.two_debt_target = -int(math.log(max_n)/math.log(5))
        self.two_debt = 0
        self.m = m
        # Reduced modulus value, includes NO multiples of 5
        # May have a two debt that needs to be resolved
        self.r = 1
    
    def mult_shifter(self, B: Shifter):
        self.r = reduce(self.r * B.r, self.m)
        self.two_debt += B.two_debt
    
    def mult_int(self, b):
        while b % 5 == 0:
            b = b // 5
            self.two_debt += 1
        while self.two_debt >= self.two_debt_target and b % 2 == 0:
            b = b // 2
            self.two_debt -= 1
        self.r = reduce(self.r * reduce(b, self.m), self.m)
    
    def resolve_two_debt(self):
        while self.two_debt < 0:
            self.r = reduce(self.r * 2, self.m)
            self.two_debt += 1
        if self.two_debt > 0:
            raise Exception("Two debt has not been resolved: {}".format(self.two_debt))
    
    def __repr__(self):
        return "{}({})".format(self.r, self.two_debt)
    
    def copy(self):
        X = Shifter(1, self.m)
        X.two_debt_target = self.two_debt_target
        X.two_debt = self.two_debt
        X.r = self.r
        return 


def slow_f(n, m):
    r = 1
    two_debt = 0
    two_debt_target = -int(math.log(n)/math.log(5))
    for i in range(1,n+1):
        while i % 5 == 0:
            i  = i // 5
            two_debt += 1
        while two_debt >= two_debt_target and i % 2 == 0:
            i = i // 2
            two_debt -= 1
        r = mult(r, i, m)
    while two_debt < 0:
        r = mult(r, 2, m)
        two_debt += 1
    if two_debt > 0:
        raise Exception("Did not exaust two debt: {}".format(two_debt))
    return r

def slow_f2(n, m):
    R = Shifter(n, m)
    for i in range(2, n+1):
        R.mult_int(i)
    R.resolve_two_debt()
    return R.r

def power_10(R:Shifter, e, m):
    # raise n to the power of 10**e
    if e == 0:
        return R
    R_10 = Shifter(1, m)
    for _ in range(10):
        R_10.mult_shifter(R)
    return power_10(R_10, e-1, m)

def concurrent_compare(n, m):
    r_full = 1
    for i in range(1, n+1):
        r_full *= i
        fn = slow_f(i, m)
        if fn != reduce(r_full, m):
            print(i, fn, r_full)

def product_non_25(n, m):
    #Take the m reduced modulus product of all of the values up to and including n
    #Product of the values that do not include the factors of 2 or 5
    #Eliminates about 40% of the sums
    r = 1
    for i in range(3, n+1, 2):
        if i % 5 == 0:
            continue
        r = mult(r, i, m)
    return r

def brute_factorial_non_25(n,m):
    product = 1
    for i in range(1, n+1):
        if i % 2 != 0 and i % 5 != 0:
            product *= i
    return product

# print(product_non_25(237, 8))
# print(brute_factorial_non_25(237,8))
# Validated

def slow_power(base, exponent, m):
    if base % 5 == 0 or base > 10**m:
        raise Exception("input not in the correct format: {}".format(base))
    result = 1
    for i in range(exponent):
        result = mult(result, base, m)
    return result


def power(base, exponent, m):
    #Raise r^p digital modulus m
    #Assume that r is in digital modulus format with no factors of 5 included
    #Quick type check on r
    if base % 5 == 0 or base > 10**m:
        raise Exception("input not in the correct format: {}".format(base))
    result = 1
    base_stepped = base
    exponent_binary_reverse = list(bin(exponent))[2:][::-1]
    for binary_digit in exponent_binary_reverse:
        if binary_digit == "1":
            # = base for first pass
            result = mult(result, base_stepped, m)
        #Increase the base
        base_stepped = mult(base_stepped,base_stepped, m)
    return result

def quick_factorial_non_25(n, m):
    if n > 10**m:
        tail = product_non_25(10**m, m)
        product = power(tail, n // 10**m, m)
        last = product_non_25(n % 10**m, m)
        product = mult(product, last, m)
        return product
    else:
        return product_non_25(n, m)

# n = 2375
# m = 5
# print("quick", quick_factorial_non_25(n, m))
# print("brute", str(brute_factorial_non_25(n, m))[-m:])
# Validated quick factorial non 25
    

def brute_factorial_divide_25(n, m):
    product = 1
    two_count = 0
    five_count = 0
    for i in range(1, n+1):
        while i % 2 == 0:
            i = i // 2
            two_count += 1
        while i % 5 == 0:
            i = i // 5
            five_count += 1
        product = mult(product, i, m)
    return two_count, five_count, product

def partial_product(n, dividend, m):
    # Return the partial product and count of the number of occurances of the divident up to and including n
    n_new = n // dividend
    dividend_count = n - (n // dividend)
    product = quick_factorial_non_25(n_new, m)
    return n_new, dividend_count, product

def two_partial_product(n, m):
    #factorial of n digital modulus m, excluding all factors of 2 & 5
    sub_n, two_count, product = partial_product(n, 1, m)
    # print(sub_n, two_count, product)
    while sub_n % 2 == 0:
        sub_n, sub_two_count, sub_product = partial_product(sub_n, 2, m)
        two_count += sub_two_count
        product = mult(product, sub_product, m)
    return two_count, product

def count_factors(n, factor):
    count = 0
    while n > 0:
        n = n // factor
        count += n
    return count

def brute_factorial(n,m):
    product = 1
    for i in range(1, n+1):
        product *= i
    return reduce(product, m)

def full_product2(n, m):
    # n is required to be a power of 2
    product = 1
    for five_exponent in range(0, int(math.log(n)/math.log(5)) + 1):
        for two_exponent in range(0, int(math.log(n)/math.log(2)) + 1):
            sub_n = n // 2**two_exponent // 5**five_exponent
            sub_product = quick_factorial_non_25(sub_n, m)
            product = mult(product, sub_product, m)
    two_count = count_factors(n, 2)
    five_count = count_factors(n, 5)
    #Now equalize the two and five count and multiply out by the remaining two count
    two_count -= five_count
    two_product = power(2, two_count, m)
    product = mult(product, two_product, m)
    return product


# m = 4
# n = 10000
# print(brute_factorial(n, m))
# print(full_product2(n, m))
# # full product 2 validated



m = 5 #Number of digits to investigate
E = 12 #10**6 is the n to investigate

ans = full_product2(10**E, m)
print("ans", ans)

exit()


# def full_product(n, m):
#     #Here is where we iterate through the fives and get the five count
#     two_count, product = two_partial_product(n, m)
#     five_count = 0
#     while n % 5 == 0:
#         five_count += n // 5
#         n = n // 5
#         sub_two_count, sub_product = two_partial_product(n, m)
#         two_count += sub_two_count
#         product = mult(product, sub_product, m)
#     #Print some things
#     print("two_count: {:,}, five_count: {:,}, product: {:,}".format(two_count, five_count, product))
#     #Equalize the two and five count
#     two_count -= five_count
#     two_product = power(2, two_count, m)
#     product = mult(product, two_product, m)
#     print("full product: {}".format(product))
#     return product

base = 124337
exponent = 100
print(slow_power(base,exponent,m))
print(power(base,exponent,m))

n_max = 10**E
product = 1

partial = product_non_25(n_max, m)
partial = power(partial, n_max//10**m, m)
product = mult(product, partial)

two_count = n_max - (n_max // 2)
n_max = n_max // 2
partial = product_non_25(n_max, m)
partial = power(partial, n_max//10**m, m)
product = mult(product, partial)

exit()

# print(slow_f(10**E, m))
print(slow_f2(10**E, m))

# W = Shifter(1, m)
# X = Shifter(1, m)
# X.mult_int(12832)
# X.resolve_two_debt()
# print("X", X)
# for i in range(10000):
#     W.mult_shifter(X)
# W.resolve_two_debt()
# print("W", W)

# A = power_10(X, 4, m)
# print("A", A)

# exit()

R_end = Shifter(10**E, m)
for i in range(1, 10**m):
    # Skip items with trailing zeros
    if i % 10 == 0:
        continue
    R_end.mult_int(i)
R_end.resolve_two_debt()
print("R_end", R_end)

# Iterate from right to left raising each item to the appropriate power
R = Shifter(10**E, m)
for left_digits in range(E - m, 0, -1):
    Q = power_10(R_end, left_digits, m)
    R.mult_shifter(Q)

# Iterate through the final left digit
for i in range(1, 10**m):
    R.mult_int(i)

#Resolve any balance of twos debt
R.resolve_two_debt()


print(R)
print("ans", R.r)


