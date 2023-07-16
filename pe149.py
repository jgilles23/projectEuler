import numpy as np

side_length = 2000
N = side_length**2
S = np.full(N+1, 0)

for k in range(1,min(56, N+1)):
    S[k] = ((100003 - 200003*k + 300007*k**3)%1000000 - 500000)
for k in range(56, N + 1):
    S[k] = ((S[k-24] + S[k-55])%1000000 - 500000)

print("Test:", S[10], S[10] == -393027)
print("Test:", S[100], S[100] == 86613)

def find_max_sum(A):
    # Find the maximum sum in the sequence A
    rolling_sum = 0
    max_sum = 0
    for a in A:
        rolling_sum += a
        if rolling_sum <= 0:
            rolling_sum = 0
        elif rolling_sum > max_sum:
            max_sum = rolling_sum
    return max_sum

def brute_force_find_max_sum(A):
    max_sum = 0
    for i in range(A.shape[0]):
        for j in range(i, A.shape[0]):
            s = sum(A[i:j+1])
            if s > max_sum:
                max_sum = s
    return max_sum

# A = S[1:1001]
# print("{:,}".format(find_max_sum(A)))
# print("{:,}".format(brute_force_find_max_sum(A)))

max_sum = 0
def test(s):
    global max_sum
    if s > max_sum:
        max_sum = s
        print("New max {:,}".format(max_sum))

# Re-arrange into a square
square = S[1:].reshape((side_length, side_length))
# Test the horizontals & verticals
for i in range(side_length):
    test(find_max_sum(square[i,:]))
    test(find_max_sum(square[:,i]))
# Test the diagonals
anti_square = np.fliplr(square)
for i in range(-side_length+1, side_length):
    test(find_max_sum(square.diagonal(i)))
    test(find_max_sum(anti_square.diagonal(i)))

print("ans", max_sum)