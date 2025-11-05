import math
k = 30.403243784
f = lambda x: math.floor(2**(k - x**2)) * 10**-9

N = 10000
u = -1
seen_before = set()
seen_multiple = set()
for i in range(1, N + 1):
    u = f(u)
    if u in seen_before:
        seen_multiple.add(u)
    else:
        seen_before.add(u)
ans = 0
for a in seen_multiple:
    ans += a
print(ans)
print(round(ans,9))