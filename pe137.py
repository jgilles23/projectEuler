def F(n):
    s5 = 5**0.5
    return 1/s5*(((1+s5)/2)**n - ((1-s5)/2)**n)

for n in range(10):
    print(F(n))