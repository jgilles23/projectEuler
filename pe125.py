N = 10**8

squares = []
for i in range(0, int((N/1.9)**0.5 + 1)):
    squares.append(i**2)

def is_palindrome(n):
    n_str = str(n)
    a = len(n_str)//2
    left = n_str[:a]
    right = n_str[len(n_str)-a:][::-1]
    return left == right

full_sum = 0
for i in range(1,len(squares)):
    for j in range(i+2 , len(squares)):
        n = sum(squares[i:j])
        if n >= N:
            break
        flag = is_palindrome(n)
        if flag:
            full_sum += n
            print(n, ":", i, squares[i], "|", j-1, squares[j-1])

print("ANS", full_sum)