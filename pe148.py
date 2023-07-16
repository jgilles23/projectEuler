import numpy as np
import math
N = 7**3

def brute_force(N, print_flag=False):
    A = np.full(1, 1)
    if print_flag: print("[#]")
    count_total = 1
    count_non_divisable = 1
    for n in range(1, N):
        B = np.full(A.shape[0] + 1, 0)
        B[0:-1] = A
        B[1:] += A
        A = B%7
        count_total += A.shape[0]
        count_non_divisable += sum(A != 0)
        if print_flag:
            s = str(A).replace(" ", "").replace("\n", "")
            for c in ["1", "2", "3", "4", "5", "6"]:
                s = s.replace(c, " ")
            s = s.replace(" ", "#").replace("0", " ")
            print(s[:200])
    print("{:,} of {:,} are NOT divisible in {:,} rows".format(count_non_divisable, count_total, N))
    return(count_non_divisable, count_total)

# brute_force(N, False)

# Q = ["{:,}".format(7**e) for e in range(20)]
# print(Q)

#What we need to do is count the number of structures

#We will call a #, a 0th order strucutre. We will call a 7x7 triangle a 2nd order strucutre
#A 49x49 which is made of of 7x7 first order strucutres a second order strucutre
#Continue the pattern
def structure_count_recursive(order):
    if order == 0:
        return 1
    return 28*structure_count_recursive(order - 1)

# print("********************************************************")

E = int(math.log(N)/math.log(7)) + 2
# print("E", E)
# powers = [7**e for e in range(E)]
# structure_pixle_count = [28**e for e in range(E)]

# print(powers)

# print(structure_count_recursive(2))
# brute_force(7**2, False)

# So we will know how many full nth order strucutres are avaliable by the cutoff
# Then will need to determine how many n-1 order structures there are that are full
# Then we will need to determine n-2 order strucutres.
# Should be able to do this recursivly

#Determine the base
# order = 0
# while N > powers[order]:
#     order += 1
# order -= 1
# base = powers[order]
# count = N//base
# number_sub_structures = sub_strucutre_count[count - 1]
# print(base, count, number_sub_structures)

sub_strucutre_count = [0, 1, 3, 6, 10, 15, 21, 28]

# Start by counting full structures, then count partial strucutres
def count_full_and_partial(n):
    # print("current n:", n)
    # Start by calculating full structures
    # Determine the order of the complete structure that is smaller than N
    order = int(math.log(n)/math.log(7))
    complete_rows = n//7**order
    complete_pixle_count = sub_strucutre_count[complete_rows]*28**(order)
    # Now look at partial rows
    partial_row = int(math.ceil(n/7**order))
    if partial_row == complete_rows:
        #Count is complete - there are no partial rows
        return complete_pixle_count
    #Here there are partial rows
    # print("new n:", n - complete_rows*7**order)
    partial_pixle_count = partial_row*count_full_and_partial(n - complete_rows*7**order)
    total_pixle_count = complete_pixle_count + partial_pixle_count
    return total_pixle_count
    

N = 10**9

# brute_force(N, False)
p = count_full_and_partial(N)
print("{:,}".format(p))
print("ans", p)