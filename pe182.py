# %%
import math

def encrypt(m, e, n):
    c = pow(m, e, n)
    return c

def find_d(e, phi):
    d = pow(e, -1, phi)
    return d

def decrypt(c, e, n, phi):
    d = find_d(e, phi)
    m = pow(c, d, n)
    return m

def find_unconcealed(p, q, e, cutoff = 10**10):
    unconcealed_list = []
    n = p*q
    phi = (p-1)*(q-1)
    for m in range(0, n):
        c = encrypt(m, e, n)
        if c == m:
            unconcealed_list.append(m)
            if len(unconcealed_list) > cutoff:
                # print("cutoff at m =", m)
                return unconcealed_list
    return unconcealed_list

def find_minimum_e(p,q):
    minimum_count = 10**10
    minimim_sum = 0
    n = p*q
    phi = (p-1)*(q-1)
    for e in range(2, phi):
        if math.gcd(e,phi) != 1:
            continue
        unconcealed_list = find_unconcealed(p, q, e, cutoff=minimum_count)
        unconcealed_count = len(unconcealed_list)
        if unconcealed_count == minimum_count:
            print("minimum_count:", unconcealed_count, "e:", e, unconcealed_list)
            minimim_sum += e
        elif unconcealed_count < minimum_count:
            print("RESET")
            print("minimum_count:", unconcealed_count, "e:", e, unconcealed_list)
            minimim_sum = e
            minimum_count = unconcealed_count
    return e

p = 1009
q = 3643
print(find_minimum_e(p, q))

# %%
import numpy as np
import math

p = 1009
q = 3643
n = p*q
phi = (p-1)*(q-1)

minimum_count = 10**10
minimum_sum = 0
e_power_max = int(math.log2(phi))
M_base = np.arange(0,n, dtype=np.int64)
M_power = np.full((n, e_power_max), 0, dtype=np.int64)
M_power[:, 0] = M_base
bit_masks = np.full(e_power_max, 0)
bit_masks[0] = 1
for power in range(1, e_power_max):
    M_power[:, power] = M_power[:, power - 1]**2 % n
    bit_masks[power] = bit_masks[power - 1] << 1
for e in range(2, phi):
    if math.gcd(e,phi) != 1:
        continue
    product = 1
    for i, bit_mask in enumerate(bit_masks):
        if bit_mask & e > 0:
            product = (product * M_power[:, i]) % n
    unconcealed_count = np.sum(product == M_base)
    if unconcealed_count == minimum_count:
        print("minimum_count:", unconcealed_count, "e:", e)
        # print(find_unconcealed(p, q, e))
        minimim_sum += e
    elif unconcealed_count < minimum_count:
        print("RESET")
        print("minimum_count:", unconcealed_count, "e:", e)
        minimim_sum = e
        minimum_count = unconcealed_count
    else:
        # print("Did not work", e, "count", unconcealed_count, find_unconcealed(p,q,e))
        pass


# %%
# Guess the answer
import math

p = 1009
q = 3643
n = p*q
phi = (p-1)*(q-1)

ordered_misses = []
for e in range(2, phi):
    pass

# %% Try by finding cycles
p = 1009
q = 3643
n = p*q
phi = (p-1)*(q-1)

m = 2
results = [m]
power = 1
while True:
    power += 1
    new_result = results[-1]*m % 100
    if new_result in results:
        print(m)
        break
    results.append(new_result)

# %%
#Try again
import sympy
import numpy as np

p = 1009
q = 3643
n = p*q
phi = (p-1)*(q-1)

e_counts = np.full(phi, 0)

found_repeat_points = dict()
used_repeat_points = dict()
for m in range(2, n):
    if m % 1000000 == 0:
        print("m: {:,}".format(m))
    for x in found_repeat_points:
        if pow(m, x, n) == m:
            #Check if any divisors are better
            for divisor in found_repeat_points[x]:
                if pow(m, divisor, n) == m:
                    # print("Found a smaller answer", "m: {}, x: {}, divisor: {}".format(m, x, divisor))
                    e_counts[1::divisor] += 1
                    # if divisor in used_repeat_points:
                    #     used_repeat_points[divisor] += 1
                    # else:
                    #     used_repeat_points[divisor] = 1
                    # break
            # else:
            #     used_repeat_points[x] += 1
            break
    else:
        current = m
        for e in range(2, phi):
            current = current*m % n
            if current == m:
                break
        else:
            print("Never got a break")
        print("NEW m:", m, "repeat at e:", e)
        # e_counts[1::divisor] += 1
        # used_repeat_points[e] = 1
        found_repeat_points[e] = sympy.divisors(e)[1:-1]
# print("used repeat points:", used_repeat_points)
total = 0
for e in range(2, phi):
    if math.gcd(e, phi) != 1:
        continue
    print("e: {}, intersects: {}")

# %%
## Try again, hopefully this time with fewer errors
import sympy
import numpy as np

p = 1009
q = 3643
n = p*q
phi = (p-1)*(q-1)

e_unconcealed_counts = np.full(n, 0)
phi_divisors = sympy.divisors(phi) + [phi]
phi_divisors_count = [0 for _ in phi_divisors]
for m in range(0, n):
    #Print occasionally
    if m % 200000 == 0:
        print("m: {:,}".format(m))
    # Calculate a new common divisor
    for i, divisor in enumerate(phi_divisors):
        if pow(m, 1 + divisor, n) == m:
            phi_divisors_count[i] += 1
            e_unconcealed_counts[1::divisor] += 1
            break
    else:
        print("found no divisors for m:", m)
print(phi_divisors)
print(phi_divisors_count)
# %%
#Create a summation of the above
import math

min_count = 10**10
total = 0
for e in range(2, phi):
    if math.gcd(e, phi) != 1:
        continue
    if e_unconcealed_counts[e] == min_count:
        #Found a minimum
        total += e
    elif e_unconcealed_counts[e] < min_count:
        min_count = e_unconcealed_counts[e]
        total = e
print("ans", total)
#399788195976
# %%
