#PE217
import math

def brute(length):
    balanced_sum = 0
    for i in range(1, 10**length):
        s = str(i)
        k_2 = int(math.ceil(len(s)/2))
        left = sum(int(c) for c in s[:k_2])
        right = sum(int(c) for c in s[len(s)-k_2:])
        if left == right:
            # print(i)
            balanced_sum += i
    return balanced_sum

def brute_half(length, digit_sum, allow_leading_zero, print_flag = False):
    if print_flag:
        print(f"Brute half, length: {length}, digit_sum: {digit_sum}, allow_leading_zero: {allow_leading_zero}")
    if allow_leading_zero:
        min_i = 0
    else:
        min_i = 10**(length - 1)
    count_ = 0
    sum_ = 0
    for i in range(min_i, 10**length):
        i_sigit_sum = sum(int(c) for c in str(i))
        if i_sigit_sum == digit_sum:
            count_ += 1
            sum_ += i
            if print_flag: print(f"   {i}")
    return count_, sum_

#Retry the half builder, we may make this a recursive calling thing to make it easier?
count_lookup = {}
sum_lookup = {}
#Indexed by (length, digit_sum, allow_leading_zero)
def get_count_and_sum(length, digit_sum, allow_leading_zero):
    #Calculate the number of ways that a particular digit sum can be made and the sum of all of those ways
    #Buildup the answer recursively with a sum lookup table
    key = (length, digit_sum, allow_leading_zero)
    if key in count_lookup:
        return count_lookup[key], sum_lookup[key]
    if length == 0:
        #Base case
        return int(digit_sum == 0), 0
    count_ = 0
    sum_ = 0
    if allow_leading_zero:
        min_digit = 0
    else:
        min_digit = 1
    for digit in range(min_digit, 10):
        previous_count, previous_sum = get_count_and_sum(length - 1, digit_sum - digit, allow_leading_zero=True)
        count_ += previous_count
        sum_ += previous_sum + digit*10**(length - 1)*previous_count
    #Save the calculated values
    count_lookup[key] = count_
    sum_lookup[key] = sum_
    return count_, sum_

def get_balanced_sum(length):
    overall_sum = 45 #For length 1
    for k in range(2,length + 1):
        for digit_sum in range(1, 9*(k//2) + 1):
            count_left, sum_left = get_count_and_sum(k//2, digit_sum, allow_leading_zero=False)
            count_right, sum_right = get_count_and_sum(k//2, digit_sum, allow_leading_zero=True)
            if k % 2 == 1:
                count_middle, sum_middle = 10, 45
                k_odd = 1
            else:
                count_middle, sum_middle = 1, 0
                k_odd = 0
            left = sum_left * 10**(k//2 + k_odd) * count_middle*count_right
            middle = sum_middle * 10**(k//2) * count_left*count_right
            right = sum_right * count_left*count_middle
            s = left + middle + right
            # print(f"k: {k}, digit_sum: {digit_sum}, ({sum_left}*10^{k//2 + k_odd} + 45*{k_odd} + {sum_right}) * ({count_left} * {1 + 9*k_odd} * {count_right}) = {s}")
            overall_sum += s
    return overall_sum

length = 47
# print("brute", brute(length) % (3**15))
sum_ = get_balanced_sum(length)
print(sum_)
print("ans", sum_ % (3**15))

# length = 5
# allow_leading_zero = True
# for digit_sum in [20]: #range(0,10):
#     count_, sum_ = get_count_and_sum(length, digit_sum, allow_leading_zero)
#     if length <= 5:
#         brute_count, brute_sum = brute_half(length, digit_sum, allow_leading_zero, print_flag = False)
#     else:
#         brute_count, brute_sum = "NA", "NA"
#     print(f"digit_sum: {digit_sum}, count: {count_}, sum: {sum_}   |   brute_count: {brute_count}, brute_sum: {brute_sum} | {count_ == brute_count and sum_ == brute_sum}")


'''

#Some sort of half builder, where on the last set, we assert that the sides must be equal
counts_by_digit_sums = [[1]] #indexed by a
sums_by_digit_sums = [[0]] #indexed by a
reverse_sums_by_digit_sums = [[0]] #indexed by a

for i in range(1, n//2 + 1):
    prev_len = len(counts_by_digit_sums[i-1])
    new_counts = [0]*(prev_len + 9)
    new_sums = [0]*(prev_len + 9)
    new_reverse = [0]*(prev_len + 9)
    for a, (count_, sum_, reverse_) in enumerate(zip(counts_by_digit_sums[i-1], sums_by_digit_sums[i-1], reverse_sums_by_digit_sums[i-1])):
        for d in range(0,10):
            #Last digit added to the front cannot be zero
            new_counts[a + d] += counts_by_digit_sums[i-1][a]
            new_sums[a + d] += sums_by_digit_sums[i-1][a] + d*10**(i-1)
            new_reverse[a + d] += reverse_sums_by_digit_sums[i-1][a]*10 + d
    counts_by_digit_sums.append(new_counts)
    sums_by_digit_sums.append(new_sums)
    reverse_sums_by_digit_sums.append(new_reverse)

for i in range(len(counts_by_digit_sums)):
    print(f"i: {i}\n  counts: {counts_by_digit_sums[i]}\n  sums:   {sums_by_digit_sums[i]}\n revers: {reverse_sums_by_digit_sums[i]}")

exit()

balanced_sum = 0
for k in range(1,n):
    for a, (count_, sum_) in enumerate(zip(counts_by_digit_sums[k//2], sums_by_digit_sums[k//2])):
        #Where a is the sum of the digits, count_ is the number of instances of that sum, sum_ is the sum of the numbers with that sum of the digits
        if k % 2 == 0:
            #k even
            balanced_sum = (sum_*10**k//2 + sum)

'''