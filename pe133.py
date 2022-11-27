import sympy

def R(k):
    return int("1"*k)

def R2(k):
    x = 0
    for _ in range(k):
        x = x*10 + 1
    return x

def check(a, b):
    m = a % b
    if m == 0:
        print("divides")
    else:
        print("does not divide")

def repeat_length(n):
    #GCD of n and 10 is 1
    if n%5 == 0:
        return 0
    #Make the lookup table
    table = [n*i for i in range(10)]
    table.sort(key = lambda x: str(x)[-1])
    #Run the loop
    rolling_sum = table[1]
    ones_count = 1
    while rolling_sum != 1:
        previous_rolling_sum = rolling_sum
        rolling_sum = rolling_sum // 10
        a = table[(11 - rolling_sum%10)%10]
        rolling_sum += a
        ones_count += 1
        # print("sum was", previous_rolling_sum, "plus", a, "sum is", rolling_sum, "with ones count", ones_count)
    # print(n, ":", "ones count", ones_count)
    return ones_count

N = 100_000
prime_sum = 2 + 3 + 5

for p in sympy.primerange(7, N):
    r = repeat_length(p)
    works = True
    for k in sympy.factorint(r, limit=6).keys():
        if not (k == 2 or k == 5):
            works = False
            break
    if not works:
        prime_sum += p
    else: print("works", p)
print("ANS", prime_sum)
