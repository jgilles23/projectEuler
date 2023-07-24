import sympy
import math

max_count = 18
one_numerator = 1
one_denominator = 1
distinct_values = [set() for _ in range(max_count + 1)]
distinct_values[1] = {(one_numerator, one_denominator)}

def recursive_find(capaciator_count):
    # If already found the distinct values, return them
    if len(distinct_values[capaciator_count]) > 0:
        return distinct_values[capaciator_count]
    #Otherwise calculate the distinct values needed
    for small_count in range(1, capaciator_count//2 + 1):
        big_count = capaciator_count - small_count
        for a in recursive_find(small_count):
            for b in recursive_find(big_count):
                # print("count: {}, a: {}, b: {}".format(capaciator_count, a, b))
                #Combine the capacitance options
                #Combine in parallel
                # C = (an*bd + bn*ad)/(ad*bd)
                n,d = (a[0]*b[1] + b[0]*a[1], a[1]*b[1])
                g = math.gcd(n,d)
                distinct_values[capaciator_count].add((n//g, d//g))
                #Combine in series
                # C = (od/on + d/n)^-1 = (d*on+od*n / on*n)^-1 = on*n / (d*on + od*n)
                # = bn*an / (ad*bn + bd*an)
                n,d = (b[0]*a[0], a[1]*b[0] + b[1]*a[0])
                g = math.gcd(n,d)
                distinct_values[capaciator_count].add((n//g, d//g))
    return distinct_values[capaciator_count]

recursive_find(max_count)
combined_values = set().union(*distinct_values)
# print(distinct_values)
# print(combined_values)
print("ans", len(combined_values))

exit()

def add_layer(numerator=one_numerator, denominator=one_denominator, capaciator_count=1):
    global max_count, distinct_values, one_numerator, one_denominator
    global distinct_values
    # Add to list of distinct values additonal capacitiences found
    # Input capacitance
    # Count of capacitors used
    # simplify the fraction
    g = math.gcd(numerator, denominator)
    numerator = numerator//g
    denominator = denominator//g
    numerator_denominator = (numerator, denominator)
    if numerator_denominator in distinct_values:
        return
    else:
        distinct_values.add(numerator_denominator)
    #Return if there are already 18 count
    if capaciator_count >= max_count:
        return
    # Add capaciator in parallel
    # C = (n*od + on*d)/(d*od)
    add_layer(numerator*one_denominator + one_numerator*denominator, denominator*one_denominator, capaciator_count+1)
    # C = (od/on + d/n)^-1 = (d*on+od*n / on*n)^-1 = on*n / (d*on + od*n)
    # Add capacitor in series
    add_layer(one_numerator*numerator, denominator*one_numerator + one_denominator*numerator, capaciator_count+1)

add_layer()
print(list(distinct_values)[::1000])
# print(distinct_values)
print("ans", len(distinct_values))

print((one_numerator*18, one_denominator) in distinct_values)