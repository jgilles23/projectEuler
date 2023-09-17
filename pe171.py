import math
import itertools

power = 20 #Maximum number of digits in the resultant number
modulus = 9

brute_n_answers = set()
brute_count_totals = dict()

def brute_f(n):
    total = sum([int(x)**2 for x in str(n)])
    sqrt = int(total**0.5)
    if sqrt**2 == total:
        # Some checks to find issues
        brute_n_answers.add(n)
        counts = [0 for _ in range(10)]
        for v in [int(x) for x in str(n).rjust(power, "0")]:
            counts[v] += 1
        counts = tuple(counts)
        if counts in brute_count_totals:
            brute_count_totals[counts] = brute_count_totals[counts] + n % 10**modulus
        else:
            brute_count_totals[counts] = n % 10**modulus
        # Return answer
        return n
    return 0
    
def brute_all_n():
    total = 0
    for n in range(1, 10**power):
        total += brute_f(n)
    return total % 10**modulus


def sum_modulus_digits(stream):
    counts = [0 for _ in range(10)]
    for v in stream:
        counts[v] += 1
    combinations = math.factorial(power) // math.prod([math.factorial(c) for c in counts])
    digit_sum = combinations * sum([c*k for k,c in enumerate(counts)]) // power % 10**modulus
    total = 0
    for position in range(min(modulus,power)):
        total += digit_sum * 10**position
    total = total % 10**modulus
    # Test
    # fast_counts_total[tuple(counts)] = total 
    return total

# fast_n_answers = set()
# fast_counts_total = dict()

def recurse_add_digit(total=0, last_digit=9, stream=[]):
    global end_total
    if len(stream) == power:
        sqrt = int(total**0.5)
        if sqrt**2 == total:
            #Valid solution
            # Test
            # for permutation in itertools.permutations(stream):
            #     fast_n_answers.add(int("".join([str(x) for x in permutation])))
            # Find the number of combinations for the number
            sub_total = sum_modulus_digits(stream)
            # print(total, stream, sum_modulus_digits(stream))
            end_total += sub_total
        return
    for digit in range(last_digit, -1, -1):
        recurse_add_digit(total + digit**2, digit, stream + [digit])

end_total = 0
recurse_add_digit()
print("ans", end_total % 10**modulus)
if power <= 6:
    print("bru", brute_all_n())

# for n in brute_n_answers:
#     if n not in fast_n_answers:
#         print("In brute but not fast:", n)
# for n in fast_n_answers:
#     if n not in brute_n_answers:
#         print("In fast but not brute:", n)

# for counts in brute_count_totals:
#     if counts not in fast_counts_total:
#         print("In brute but not fast:", counts)
#     else:
#         if brute_count_totals[counts] != fast_counts_total[counts]:
#             print("counts", counts, "brute", brute_count_totals[counts], "fast", fast_counts_total[counts])
# for counts in fast_counts_total:
#     if counts not in brute_count_totals:
#         print("In fast but not brute", counts, fast_counts_total[counts])

# 142989533
# 142989277