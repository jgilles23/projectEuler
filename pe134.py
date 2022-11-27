import sympy

N = 10**6

# num = 19
# den = 23

# table = [den*i for i in range(10)]
# table.sort(key = lambda x: str(x)[-1])
# print(table)

# target = num % 10
# plu = table[target]
# print("num", num, "target", target, "plu", plu)

# plu = (plu//10)%10
# num = num//10
# target = num%10
# plu = table[target - plu]
# print("num", num, "target", target, "plu", plu)

# exit()


p2 = 5 
n_sum = 0
for i, p in enumerate(sympy.primerange(6, N*11//10)):
    p1 = p2
    p2 = p
    if (p1 > N):
        break
    # print(p1, p2)
    delta = 10**len(str(p1))
    n = delta + p1
    while n % p2 != 0:
        n += delta
    n_sum += n
    if i%1024 == 0: print(p1, p2, ":", n)

print("ANS", n_sum)
