D = 20 #Number of digits

counts = {"000":1}

for d in range(1, D + 1):
    m = 0 if d < D else 1
    new_counts = dict()
    for key in counts:
        # Pop the right most digit, add a digit to the left
        s = sum([int(x) for x in key[:2]])
        for digit in range(m, 10 - s):
            new_key = str(digit) + key[:2]
            if new_key in new_counts:
                new_counts[new_key] += counts[key]
            else:
                new_counts[new_key] = counts[key]
    counts = new_counts

total = 0
for key in counts:
    total += counts[key]

# print(counts)

print("ans", total)

def brute(D):
    count = 0
    for n in range(10**(D-1), 10**D):
        s = str(n)
        c = False
        for i in range(len(s)):
            if sum([int(x) for x in s[i:i+3]]) > 9:
                c = True
                break
        if c == True:
            continue
        count += 1
    return count

if D <= 5:
    print("bru", brute(D))