#Copied code for pi generation so that I didn't need to type 200 numbers into a string
def pi_digits():
    """Generator that yields digits of pi."""
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4 * q + r - t < n * t:
            yield n
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr

# Usage
digits = pi_digits()
pi_digits = ""
for _ in range(250):
    pi_digits += str(next(digits))

A = pi_digits[1:101]
B = pi_digits[101:201]
print("A:", A)
print("B:", B)

if False:
    A = str(1415926535)
    B = str(8979323846)

def n_generator(i):
    return (127 + 19*i) * 7**i

max_i = 17
max_n = n_generator(max_i)
max_m = max_n - 1
print(f"Max i: {max_i}, Max n: {max_n}, Max m: {max_m:,}")

F = [len(A), len(B)]
while F[-1] <= max_m:
    F.append(F[-1] + F[-2])
print(f"Length of F: {len(F):,}, Last element of F: {F[-1]:,}")

def reduce_position_and_index(F_index, m):
    if m >= F[F_index]:
        raise Exception("m must be less than F[F_index]")
    elif F_index <= 1:
        raise Exception("F_index must be greater than 1")
    a = F[F_index - 2]
    #See which side we are on
    if m < a:
        return F_index - 2, m
    else:
        return F_index - 1, m - a

def get_digit(m):
    F_index = 2
    while F[F_index] <= m:
        F_index += 1
    while F_index > 1:
        F_index, m = reduce_position_and_index(F_index, m)
    if F_index == 0:
        return A[m]
    else:
        return B[m]

ans = 0
for i in range(0, max_i + 1):
    d = get_digit(n_generator(i) - 1)
    print(f"i: {i}, n: {n_generator(i)}, digit: {d}")
    ans += 10**i * int(d)
print("ans:", ans)

