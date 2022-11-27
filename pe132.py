import sympy

# 10**9 = 2**9 * 5**9
# R(10**9) = (10**1 + 1)*(10**2 + 1)*(10**4 + 1)*(10**8 + 1)*(10**16 + 1)

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

N = 10**9
P = 40
prime_count = 0
prime_sum = 0
for n in sympy.primerange(7, N):
    r = repeat_length(n)
    if r == 0:
        continue
    if N%r == 0:
        prime_count += 1
        prime_sum += n
        print("#", prime_count, ":", "n", n, "r", r)
        if prime_count >= P:
            break

print("ANS", prime_sum)

# check(R2(62500), 62501)

