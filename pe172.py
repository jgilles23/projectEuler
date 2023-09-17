import math

power = 18

def brute():
    brute_total = 0
    for n in range(10**(power - 1),10**power):
        counts = [0 for _ in range(10)]
        for x in str(n):
            counts[int(x)] += 1
            if counts[int(x)] > 3:
                break
        else:
            brute_total += 1
    return brute_total

total = 0
def recurse_counter(power_remaining, counts):
    if power_remaining < 0:
        return
    if power_remaining - 3*(10 - len(counts)) > 0:
        return
    if len(counts) >= 10:
        if power_remaining != 0:
            raise Exception
        #Completed a count, figure out the number of numbers
        combinations = math.factorial(power) // math.prod([math.factorial(c) for c in counts])
        sub_total = combinations - combinations*counts[0]//(power)
        global total
        total += sub_total
        # print(counts, sub_total)
        return
    for i in range(4):
        recurse_counter(power_remaining - i, counts + [i])


recurse_counter(power, [])
print("ans", total)
if power < 7:
    print("bru", brute())

# 261536427365127066
# 261536427365127067
# 227485267000992000