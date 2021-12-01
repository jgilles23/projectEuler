#Project Euler #103
import math
import itertools

def breakdown(x, min=0):
    #print("x", x, "min", min)
    if min < x//2:
        for a in range(min+1, int(math.ceil(x/2))):
            for b in breakdown(x-a, a):
                yield [a] + [k for k in b]
    yield [x]

c = 0
for y in breakdown(2):
    c += 1
    print(y)
print("count", c)

def is_special_sum_set(x):
    sum_check = [False]*(sum(x)+1)
    for r in range(1, len(sum_check)):
        for options in itertools.combinations(x, r=r):
            s = sum(options)
            if sum_check[s] == False:
                sum_check[s] = True
            else:
                return False
    return True

def next_sum_set(x):
    m = len(x)//2
    y = [x[m] + k for k in [0] + x]
    return y

flag = is_special_sum_set([11, 18, 19, 20, 22, 25])
print(flag)

given_sum_set = [11, 18, 19, 20, 22, 25]
base_7_sum_set = next_sum_set(given_sum_set)
print(base_7_sum_set, sum(base_7_sum_set))
print(is_special_sum_set(next_sum_set(given_sum_set)))