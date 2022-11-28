N = 50*10**6
test_N = 1155

counts = [0]*N

for x in range(3, 5*(N+1)//4 + 1):
    if x%(2**13) == 0:
        print(x)
    for d in range(x//5 + 1, x//2 + 1):
        if x - 2*d <= 0:
            continue
        n  = (x - d)*(5*d - x)
        if n >= N:
            break
        if n <= 0:
            continue
        counts[n] += 1
        # if n == 1155: print("xyz", (x, x-d, x-2*d), "d", d, "n", n, "x limit", 5*(test_N+1)//4 + 1, "d limit", x//2 + 1)
# print(counts)
a = sum([c == 1 for c in counts])
print("ANS", a)
print(counts[1155:1155+10])