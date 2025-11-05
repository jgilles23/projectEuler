#PE201
import numpy as np

'''
Given a target n
Lets say we have 6 numbers: a, b, c, d, e, f
There are only 3 types of answers that we care about: combination of none, combination of exactly 1, combination of more than 1
0 + 0 = 0
0 + 1 = 1
0 + 2 = 2
1 + 1 = 2
1 + 2 = 2
2 + 2 = 2

Say n = 37
numbers: 1, 4, 9, 16, 25, 36
    (3,0) = (14) + (0) = (14)
    (2,1) = (5, 10, 13) + (16, 25, 36) = 9 things
        (2,0) = (5) + (0) = (5)
        (1,1) = (1, 4) + (9) = (10, 13)
    (1,2) = 

Look at it differntly:
Keep list of k = [0, 50]
Where each list is a np array of the full length 
    each one shifted right by n and added one up in the list    
    
'''

k_target = 50
N = 100
max_sum = sum([n**2 for n in range(N - k_target + 1, N + 1)])


counts = np.full((k_target + 1, max_sum + 1), 0, dtype=np.int8)
for n in range(1, N + 1):
    counts[0,0] = 1
    counts[1:, n**2:] += counts[:-1, :-n**2]
    #Reduce the counts
    counts[counts > 2] = 2
    print(f"After n = {n}, n^2 = {n**2}")
    # print(counts)
#Sum the final answer
greater_than_2_count = np.sum(counts[k_target, :] >= 2)
exactly_one_count = np.sum(counts[k_target, :] == 1)
print(f"Exactly 1: {exactly_one_count}, Greater than 2: {greater_than_2_count}")
print(min(counts[k_target, :]), max(counts[k_target, :]))
ans = np.sum(np.where(counts[k_target, :] == 1))
print("ans", ans)
#680 is incorrect