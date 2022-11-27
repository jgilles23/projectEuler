# def R(k):
#     return int("1"*k)

N = 10**6

biggest_so_far = 0

n = N + 1
while True:
    n += 2
    #GCD of n and 10 is 1
    if n%5 == 0:
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
    if ones_count > biggest_so_far:
        biggest_so_far = ones_count + 1000
        print(n, ":", "ones count", ones_count)
    if ones_count >= n:
        print("BIGGER", n, ":", "ones count", ones_count)
    if ones_count > N:
        break