import numpy as np
# Palindromic number is the sum of consecutivite squares
N = 10**8
squares = np.arange(int(N**0.5), dtype=np.uint32)**2

# def square_sum(n, palindrome_sum):
#     for i, a in enumerate(squares):
#         #Skip 0
#         if a == 0:
#             continue
#         # Check if the sum of two conseq squares is too large
#         q = a + squares[i+1]
#         if q == n:
#             print("Found:", n, "sum", palindrome_sum + n)
#             if (n >= N):
#                 raise Exception("n too large")
#             return palindrome_sum + n
#         if q > n:
#             return palindrome_sum
#         # Iterate through additional numbers
#         for b in squares[i+2:]:
#             q += b
#             if q > n:
#                 break
#             if q == n:
#                 print("Found:", n, "sum", palindrome_sum + n)
#                 if (n >= N):
#                     raise Exception("n too large")
#                 return palindrome_sum + n
#     return palindrome_sum


# palindrome_sum = 0

# print("sqrt(N) = ", int(np.sqrt(N)))
# # Single digit palindrome
# for i in range(1,10):
#     palindrome_sum = square_sum(i, palindrome_sum)
# #More than one digit palindromes
# for half_palindrome in range(1, int(np.sqrt(N))):
#     half_palindrome_string = str(half_palindrome)
#     #Produce the palindromes of even length
#     even_palindrome = int(half_palindrome_string + half_palindrome_string[::-1])
#     palindrome_sum = square_sum(even_palindrome, palindrome_sum)
#     #Check not too large for odd palindromes
#     if even_palindrome*10 >= N:
#         break
#     #Produce the palindromes of odd length
#     for i in range(10):
#         odd_palindrome = int(half_palindrome_string + str(i) + half_palindrome_string[::-1])
#         palindrome_sum = square_sum(odd_palindrome, palindrome_sum)

# print("ans", palindrome_sum)

# Try a potentially faster way
def is_palindrome(n):
    n_str = str(n)
    h = len(n_str)//2
    return n_str[:h] == n_str[-1:-h-1:-1]

S = 0
valid_palindromes = set()

for i, a in enumerate(squares):
    if a == 0:
        continue
    if a + squares[i+1] >= N:
        break
    q = a
    for b in squares[i+1:]:
        q += b
        if q >= N:
            break
        if is_palindrome(q):
            if q in valid_palindromes:
                continue
            valid_palindromes.add(q)
            S += q
            print("Found:", q, "sum", S)

print("ans", S)
