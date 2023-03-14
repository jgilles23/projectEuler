N = 10**8

def is_palindrome(n):
    s = str(n)
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

squares = [x**2 for x in range(0,int(N**0.5))]

palindrome_sum = 0

for start in range(1, len(squares)-1):
    length = 1
    n = squares[start] + squares[start + length]
    while n < N and start + length + 1 < len(squares):
        if (is_palindrome(n)):
            print(n, ": start", start, "length", length, "sum", palindrome_sum)
            palindrome_sum += int(n)
            if palindrome_sum < 0:
                print(palindrome_sum, "NEGATIVE")
                exit()
        length += 1
        n += squares[start+length]
print(palindrome_sum)