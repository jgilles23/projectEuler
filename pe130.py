# def R(k):
#     return int("1"*k)
import sympy

N = 25

composite_sum = 0
composite_count = 0

n = 7
while True:
    n += 2
    #GCD of n and 10 is 1
    if n%5 == 0:
        continue
    #Ensure that n isn't prime
    if sympy.isprime(n):
        continue
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
    if (n-1) % ones_count == 0:
        composite_count += 1
        composite_sum += n
        print("#", composite_count, "Found composite", n, ":", "ones count", ones_count, "composite count")
        if composite_count >= N:
            break
print("ANS", composite_sum)