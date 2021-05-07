#Project Euler #74 date 20210503
import math

N = 10**6

#Setup a quick factorial lookup
fact_list = [int(math.factorial(x)) for x in range(10)]

def sum_fact_dig(n):
    return sum([fact_list[int(i)] for i in str(n)])

print(sum_fact_dig(363601))

terms_to_repeat = {1:1, 2:1, 145:1, 
169:3, 363601:3, 1454:3, 
871:2, 45361:2,
872:2, 45362:2}

def find_repeat(n):
    if n in terms_to_repeat:
        return terms_to_repeat[n]
    next_n = sum_fact_dig(n)
    if next_n == n:
        terms_to_repeat[n] = 1
        return 1
    num_terms = find_repeat(next_n)
    terms_to_repeat[n] = num_terms + 1
    return num_terms + 1

count = 0
for n in range(N):
    if n not in terms_to_repeat:
        find_repeat(n)
    if terms_to_repeat[n] == 60:
        count += 1

print("ans",count)