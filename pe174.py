import math

max_n = 15
max_t = 1_000_000

N = [0 for _ in range(max_n + 1)]
for u in range(1, max_t//4 + 1):
    count = 0
    # u = r*k; r = y + k
    for k in range(1, int(math.ceil(u**0.5))):
        count += u == k * (u//k)
    if count <= max_n:
        N[count] += 1

print(N)
print(sum(N[1:11]))


# def brute():
#     N = [0 for _ in range(max_n + 1)]
#     for t in range(1, max_t+1):
#         count = 0
#         if t%2 == 0:
#             start = 2
#         else:
#             start = 1
#         for t0 in range(start, int(t**0.5), 2):
#             t1 = t//t0
#             if t == t0*t1:
#                 x = (t0 + t1)/2
#                 y = (t1 - t0)/2
#                 if x%2 == y%2:
#                     count += 1
#         if count <= max_n:
#             N[count] += 1
#     return N

# N = brute()
# print(N)