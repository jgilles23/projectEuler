import sympy
import math

N = 150000

# A_list = []

# p = 0
# while True:
#     p += 1
#     min_A = p*(p+1)*(p + (p^2  +1))
#     if len(A_list) > N and min_A > A_list[N - 1]:
#         break
#     st = p**2 + 1
#     for s in sympy.divisors(st):
#         t = st//s
#         if s >= t:
#             #must be that s < t => p < q < r
#             break
#         A = p*(p+s)*(p+t)
#         if len(A_list) > N - 1:
#             if A > A_list[N - 1]:
#                 break
#             A_list.append(A)
#             A_list.sort()
#         else:
#             A_list.append(A)
#         if s == 1 and p%2000 == 0:
#             print(f"p: {p}, A: {A}, (s: {s}, t: {t}), (p: {p}, q: -{p+s}, r: -{p+t})", end="")
#             print(f", {N}th entry: {A_list[N-1] if len(A_list) > N else "N/A"}, List length: {len(A_list)}, Last entry: {A_list[-1]}")
# A_list.sort()
# print("ans", A_list[N-1])
# print(len(A_list), len(set(A_list)))


def get_A_options(p):
    A_options = []
    st = p**2 + 1
    for s in sympy.divisors(st):
        t = st//s
        if s > t:
            break
        A = p*(p + s)*(p + t)
        A_options.append(A)
    return A_options

def get_min_A(p):
    s = math.sqrt(p**2 + 1)
    t = (p**2 + 1)/s
    return p*(p + s)*(p + t)

A_list_2 = []
p = 0
while len(A_list_2) < N:
    p += 1
    A_list_2 += get_A_options(p)
# List is large enough
print("End game.")
A_list_2.sort()
target = A_list_2[N - 1]
#Make sure everything is big enough
while get_min_A(p) <= target:
    p += 1
    A_list_2 += get_A_options(p)
print("Final sort.")
A_list_2.sort()
ans = A_list_2[N - 1]
print("ans", ans)

