sum_r_max = 0

for a in range(3,1001):
    left = 2
    right = 2
    n = 1
    r_max = 0
    while left > 1 or right > 1:
        left = pow(a-1, n, a**2)
        right = pow(a+1, n, a**2)
        combined = (left + right)%(a**2)
        if combined > r_max:
            r_max = combined
        # print(n, ":", left, right, left+right)
        n += 1
    sum_r_max += r_max
    print(a, ":", "r_max", r_max)
print("ANS", sum_r_max)
