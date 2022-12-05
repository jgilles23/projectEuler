import math
# x = -1

# a = (1+5**0.5)*x/2
# b = (1-5**0.5)*x/2
# A = (1/(1-a) - 1/(1-b))/5**0.5
# print(A)

# A = 2/5**0.5*(1/(2-x+5**0.5*x) - 1/(2-x-5**0.5*x))
# print(A)

# A = x/(1 - x - x**2)
# print(A)

N = 15

count = 0
a = 0
while count < N:
    a += 1
    k2 = 5*a**2 + 4
    k = int(round(math.sqrt(5*a**2 + 4)))
    if k**2 == k2:
        count += 1
        b = (a + k)//2
        A = a*b
        print("#", count, ":", a, b, A)

print("ANS", A)