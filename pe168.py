
def brute_test(n):
    n_str = str(n)
    n_rotate = int(n_str[-1] + n_str[:-1])
    div = n_rotate // n
    return div * n == n_rotate

def brute(low, high):
    total = 0
    for n in range(low+1, high):
        if brute_test(n):
            total += n
    print(total)

high_exp = 100

total = 0
for d in range(1,high_exp):
    ten_d = 10**d
    for a in range(1,10):
        for b in range(1,10):
            if (a*(ten_d - b)) % (10*b - 1) == 0:
                x = (a*(ten_d - b)) // (10*b - 1)
                n = 10*x + a
                n_rot = a*ten_d + x
                if n <= n_rot and n >= ten_d:
                    # print("d: {}, a: {}, b: {}, n: {}".format(d,a,b,n))
                    total += n % 10**5
                    if brute_test(n) != True:
                        pass

print("ans", total % 10**5)
# brute(10, 10**high_exp)

98326