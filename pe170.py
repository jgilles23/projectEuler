import numpy as np
import itertools

min_digit = 0
lookup_size_power = 5
lookup_size = 10**lookup_size_power
digit_bitmasks = np.full(lookup_size, 0)
full_bitmask = 2**10 - 1 - min_digit*1 #MODIFIED
# -1 indicates a number that has digits repeated
for n in range(lookup_size):
    mask = 0
    for d_str in str(n):
        d_mask = 1 << int(d_str)
        if mask & d_mask:
            digit_bitmasks[n] = -1
            break
        mask += d_mask
    else:
        digit_bitmasks[n] = mask

def get_bitmask(n):
    # Return the bitmask of a number by breakdown where required
    # Only works on n < lookup_size**2; otherwise will throw an error 
    if n >= lookup_size:
        n_lower = n % lookup_size
        if n_lower < 10**(lookup_size_power - 2):
            #First two digits are a zero
            return -1
        part0 = digit_bitmasks[n_lower] #Lower
        part1 = digit_bitmasks[n // lookup_size] #Higher
        if part0 & part1:
            return -1
        else:
            if n_lower < 10**(lookup_size_power - 1):
                #First digit of part 0 is a zero
                combined = part0 | part1
                if combined & 1:
                    return -1
                else:
                    return combined | 1
            return part0 | part1
    else:
        return digit_bitmasks[n]

def find_products(a, stream, max_subset_size, max_subset_value=10**10, digit_bitmask=0, values=[], depth=0, max_depth=1000):
    #Chop stream from size 1 to max_subset_size or remainder of the stream keeping below max_subset_value, and checking aganist the digit_bitmask to date
    if len(stream) == 0:
        if digit_bitmask == full_bitmask:
            return [values]
        else:
            return []
    elif stream[0] == "0":
        return []
    elif depth > max_depth:
        return []
    results = []
    for length in range(1, min(len(stream), max_subset_size) + 1):
        n = int("".join(stream[:length]))
        if n > max_subset_value:
            continue
        n_bitmask = get_bitmask(a*n)
        if n_bitmask & digit_bitmask:
            continue
        r = find_products(a, stream[length:], length, n, n_bitmask | digit_bitmask, values + [a*n], depth=depth+1, max_depth=max_depth)
        if r:
            results.extend(r)
    return results

max_concat_product = 0
max_concat_product_values = []
max_concat_product_a = 0
first_char = lambda n: str(n)[0]

def update_max(values, a):
    # Input list of values update the max
    global max_concat_product
    global max_concat_product_values
    global max_concat_product_a
    sorted_values = sorted(values, key = first_char, reverse=True)
    y = int("".join([str(v) for v in sorted_values]))
    if y > max_concat_product:
        max_concat_product = y
        max_concat_product_values = values
        max_concat_product_a = a
        print("new max: {}, multiplied values: {}  |  a: {}, pre-values: {}".format(y, sorted_values, a, [x//a for x in sorted_values]))

# exit()

digits = [str(x) for x in range(min_digit, 10)]
for a in [x for x in digits if int(x) > 1]: #a cannot be 0 or 1
    digits_less_a = [x for x in digits if x != a]
    for b in [x for x in digits_less_a if int(x) > 0]: #b cannot be 0
        print(a,b)
        digits_less_ab = [x for x in digits_less_a if x != b]
        for combination in itertools.permutations(digits_less_ab):
            r = find_products(int(a), [b, *combination], len(digits) - 2)
            for values in r:
                update_max(values, int(a))

digits = [str(x) for x in range(min_digit, 10)]
for a0 in [x for x in digits if int(x) > 0]: #a0 cannot be 0
    digits_less_a0 = [x for x in digits if x != a0]
    for a1 in [x for x in digits_less_a0 if int(x) > 0]:
        digits_less_a = [x for x in digits if x != a1]
        a = 10*int(a0) + int(a1)
        for b in [x for x in digits_less_a if int(x) > 0]: #b cannot be 0
            print(a,b)
            digits_less_ab = [x for x in digits_less_a if x != b]
            for combination in itertools.permutations(digits_less_ab):
                r = find_products(int(a), [b, *combination], len(digits) - 2, max_depth=1)
                for values in r:
                    update_max(values, int(a))

print("ans", max_concat_product)

# 9786105234
# 9857164023