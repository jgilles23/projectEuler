import numpy as np
import itertools
import random
import time

# random.seed("giraffe")
bitmask_checks = 10**4
min_digit = 0
lookup_size_power = 5
lookup_size = 10**lookup_size_power
digit_bitmasks = np.full(lookup_size, 0)
full_bitmask = 2**10 - 1 - min_digit*1 #MODIFIED
start = time.time()
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
print("Created bitmask lookup.", time.time() - start)

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

def brute_bitmask(n):
    digits = [int(d) for d in str(n)]
    mask = 0
    for d in digits:
        digit_mask = 1 << d
        if digit_mask & mask > 0:
            return -1
        mask += digit_mask
    return mask

start = time.time()
for _ in range(bitmask_checks):
    r = random.randint(0, lookup_size**2)
    fast = get_bitmask(r)
    brute = brute_bitmask(r)
    if fast != brute:
        raise Exception("bitmasking error")

print("Passed bitmask checks.", time.time() - start)


# Create the lookup class for integers
class Lookup:
    def __init__(self, a, max_length):
        #Provide maximum length as number of digits to create the lookup table up to
        #Provide the a value on which the table is built
        self.max_length = max_length
        self.a = a
        self.a_mask = get_bitmask(a)
        # Establish lookup table
        # [length]{x_max}{y_mask}(x,y) <- Save only the HIGHEST y for a particular combo
        self.t = [dict() for _ in range(self.max_length + 1)]
        # Initialize the table
        for x in range(10):
            self.file_and_add_digit(1, x)
    
    def file_and_add_digit(self, x_length, x):
        # x has repeat digits, do not continue, that x will never be used
        x_mask = get_bitmask(x)
        if x_mask == -1 or (x_mask & self.a_mask > 0):
            return
        # Determine the value of y and associated masks
        y = x*self.a
        y_mask = get_bitmask(y)
        # file y that doesn't have repeat digits
        if y_mask != -1 and x >= 10**(x_length-1):
            self.add_value(x_length, x_mask, y_mask, x, y)
        # Exit if at full length
        if x_length == self.max_length:
            return
        # Exit if the end of the y value has repeat digits
        y_end_mask = get_bitmask(y % 10**x_length)
        if y_end_mask == -1:
            return
        # Add digits to the front of x and call next level of iteration
        for digit in range(10):
            new_x = digit*10**(x_length) + x
            self.file_and_add_digit(x_length+1, new_x)

    def add_value(self, x_length, x_mask, y_mask, x, y):
        # Add a value to the lookup
        if x_mask in self.t[x_length]:
            if y_mask in self.t[x_length][x_mask]:
                old_xy = self.t[x_length][x_mask][y_mask]
                if y > old_xy[1]:
                    self.t[x_length][x_mask][y_mask] = (x,y)
            else:
                self.t[x_length][x_mask][y_mask] = (x,y)
        else:
            self.t[x_length][x_mask] = {y_mask:(x,y)}
    
    def yield_options_from_xmask(self, x_length, x_mask, y_mask_options):
        #Given x_mask, and the maximum mask of y_options
        #Yield through a list of y_mask options with associated [(x,y)]
        for y_mask in self.t[x_length][x_mask]:
            if y_mask_options | y_mask != y_mask_options:
                continue
            yield y_mask, self.t[x_length][x_mask][y_mask]
    
    def yield_options(self, x_length, x_mask_remaining, y_mask_remaining):
        for x_mask in self.t[x_length]:
            # Look at only x_mask that fit into the remaining masks
            if x_mask | x_mask_remaining != x_mask_remaining:
                continue
            for y_mask in self.t[x_length][x_mask]:
                # Look at only y_mask that fit into the remaining masks
                if y_mask | y_mask_remaining != y_mask_remaining:
                    continue
                # Yield x_mask, y_mask, (x,y)
                x, y = self.t[x_length][x_mask][y_mask]
                yield x_mask, y_mask, x, y


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



# x_length = 8
# for x_mask in lookup.t[x_length]:
#     print(x_mask, "{:>12}".format(bin(x_mask)), ":", lookup.t[x_length][x_mask])

# Now we need to figure out a way to iterate through the possible x -> y values
def recursive_search(a, x_mask_remaining, y_mask_remaining, max_x_length, x_values, y_values):
    if len(x_values) > 0 and x_values[0] == 9854:
        pass
    #Check if solution found
    if x_mask_remaining == 0:
        if y_mask_remaining == 0:
            #Solution found
            # print(x_values, y_values)
            update_max(y_values, a)
        return
    if y_mask_remaining == 0:
        return
    for x_length in range(max_length, 0, -1):
        for x_mask, y_mask, x, y in lookup.yield_options(x_length, x_mask_remaining, y_mask_remaining):
            # x Values should be strictly decreasing
            if len(x_values) > 0 and x > x_values[-1]:
                continue
            # Iterate again on the remaining values
            recursive_search(a, x_mask_remaining ^ x_mask, y_mask_remaining ^ y_mask, x_length, x_values + [x], y_values + [y])

max_length = 8 - min_digit
full_mask = (2**10 - 1) ^ 1*min_digit #Final -1 to exclude 0

for a in range(2, 100):
    if get_bitmask(a) == -1:
        continue
    print("a: {:}".format(a))
    lookup = Lookup(a, max_length)
    recursive_search(a, full_mask ^ get_bitmask(a), full_mask, max_length, [], [])

print("ans", max_concat_product)

# 9857164023