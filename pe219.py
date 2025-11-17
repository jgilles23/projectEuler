#PE219

#ENDED UP SOLVING THIS IN AN EXCEL SHEET

'''
1000
0100
0010
0001

I can establish an upper bound quite easily,
What I need to establish is a lower bound of the cost
(0, 110. 111) to set of size 6
    assume that all remaining entries are just zeros?
    10X is all that's avaliable
        So we could take set size 3 get the cost minimum and assume everything else starts with 10
    How could this be combined with other items
(01, 10)
    00X avaliable
    11X avaliable
    Can we always take the smallest incremental step in cost?

Does adding 1 to the length always add MORE cost than the previous addition of 1 to the length?
    Hypothesis: yes
    C(0) = 0
    C(1) = 1
    C(2) = 5
    C(3) = 

It never gets less expensive if the set is bigger
So we can always take the next smallest incremental step!

0X
1Y

Use dynamic programming
C(n) = (1x + C(x)) + (4y + C(y))
n = x + y, x >= 1, y >= 1
C(1) = 0
C(2) = 5
    0 1
C(3) = 11
    (2, 1) -> (1*2 + 5) + (4*1 + 0) = 7 + 4 = 11 #
        01 00 1 is 11
    (1, 2) -> (1*1 + 0) + (4*2 + 5) = 1 + 8 + 5 = 14
C(4) = 18
    (3, 1) -> (3 + 11) + (4  + 0) = 18 #
        001 000 01 1
    (2, 2) -> (2 + 5) + (8 + 5) = 20
C(5) = 26
    (4, 1) -> (4 + 18) + (4 + 0) = 26 #
        0001 0000 001 01 1
    (3, 2) -> (3 + 11) + (8 + 5) = 27
C(6) = 
    (5, 1) -> (5 + 26) + (4 + 0) = 35
        00001 00000 0001 001 01 1
    (4, 2) -> (4 + 18) + (8 + 5) = 35
        0001 0000 001 01 10 11
    (3, 3) -> (3 + 11) + (12 + 11) = 37

Needs to be a slightly better way to do the drill down

Binary search algorythm:
    best x = n//2
    step = n//2
    Repeat:
        step = min(step//2, 1)
        Test: best x - step
        Test: best x + step
        Pick best of (best x, + step, - step)
        if step = 1: that is the best overall
        otherwise: best x = the best of those 3
'''

cost_lookup_brute = {1:0, 2:5}

def cost(n):
    if n in cost_lookup_brute:
         return cost_lookup_brute[n]
    best_cost = n << 10
    best_x = 0
    for x in range(1, n):
         y = n - x
         c = (1*x + cost(x)) + (4*y + cost(y))
         if c < best_cost:
              best_cost = c
              best_x = x
    cost_lookup_brute[n] = best_cost
    # print(f"n: {n}, cost: {best_cost}, balance: ({best_x}, {n - best_x})")
    return best_cost

cost_lookup = {1:0, 2:5}

def C(n, x):
     y = n - x
     return (1*x + ternary_cost(x)) + (4*y + ternary_cost(y))

def ternary_cost(n):
    #n >= 3
    if n in cost_lookup:
        return cost_lookup[n]
    #Perform a ternary search
    low_x, high_x = 1, n - 1
    while high_x - low_x > 1:
        step = max((high_x - low_x)//3, 1)
        mid_low_x = low_x + step
        mid_high_x = high_x - step
        if C(n, mid_low_x) < C(n, mid_high_x):
            high_x = mid_high_x
        else:
            low_x = mid_low_x
    c = min(C(n, low_x), C(n, high_x))
    cost_lookup[n] = c
    return c     

def buildup_cost(n):
    costs = [0]*(n+1)
    costs[2] = 5
    previous_x = 1
    for i in range(3, n + 1):
        cost_low_i = (1*previous_x + costs[previous_x]) + (4*(i - previous_x) + costs[i - previous_x])
        cost_high_i = (1*(previous_x+1) + costs[previous_x+1]) + (4*(i - previous_x-1) + costs[i - previous_x-1])
        if cost_low_i <= cost_high_i:
            costs[i] = cost_low_i
        else:
            costs[i] = cost_high_i
            previous_x += 1
        # print(f"size: {i}, cost: {costs[i]}, x: {previous_x}, y: {i - previous_x}")
    # print(costs)
    delta_costs = [b - a for b,a in zip(costs[1:], costs[:-1])]
    # print(delta_costs)
    return costs[n]

import numpy as np
def buildup_cost_np(n):
    costs = np.full(n+1, 0)
    xs = np.full(n+1, 0)
    costs[2] = 5
    previous_x = 1
    for i in range(3, n + 1):
        cost_low_i = (1*previous_x + costs[previous_x]) + (4*(i - previous_x) + costs[i - previous_x])
        cost_high_i = (1*(previous_x+1) + costs[previous_x+1]) + (4*(i - previous_x-1) + costs[i - previous_x-1])
        if cost_low_i <= cost_high_i:
            costs[i] = cost_low_i
        else:
            costs[i] = cost_high_i
            previous_x += 1
        xs[i] = previous_x
        print(f"size: {i}, cost: {costs[i]}, x: {previous_x}, y: {i - previous_x}")
    # # print(costs)
    # delta_costs = [b - a for b,a in zip(costs[1:], costs[:-1])]
    # # print(delta_costs)
    # frac = xs/np.arange(n+1)
    # avg = np.mean(frac[3:])
    # frac_delta = frac - avg
    # print(frac_delta)
    return costs[n]

# for n in range(3, 100):
#      print(f"n: {n}, brute: {cost(n)}, ternary: {ternary_cost(n)}, buildup: {buildup_cost(n)}, np: {buildup_cost_np(n)}")
# print()

print("ans", buildup_cost_np(513))
