
L = 50

# m_red = 3
# count = [0]

# def recurse(l, m, red, count, level):
#     if red == True:
#         if l < m:
#             # print(" -"*level, "red", "NO count")
#             return
#         for n in range(m, l+1):
#             # print(" -"*level, "red", n)
#             recurse(l-n, m, False, count, level+1)
#     else:
#         #All grey count
#         # print(" -"*level, "gre", "COUNT all grey", l)
#         count[0] += 1
#         for n in range(1, l-m+1):
#             # print(" -"*level, "gre", n)
#             recurse(l-n, m, True, count, level+1)

# recurse(L, m_red, True, count, 1)
# print(count)
# recurse(L, m_red, False, count, 1)
# print(count)


red_start = [0, 0, 0]
grey_start = [1, 1, 1]

for l in range(3, L+1):
    red_start.append(red_start[l-1] + grey_start[l-3])
    grey_start.append(red_start[l-1] + grey_start[l-1])
    # print(l, ":", red_start[l], grey_start[l], red_start[l] + grey_start[l])
print(L, ":", red_start[L] + grey_start[L])

# count = [0]
# def recurse2(l, m, place_red, count, level):
#     # l is remaining length to divide
#     # m is minimum length of division for red
#     # place_red: true for red, false for grey
#     if place_red:
#         #place a red
#         if l < m:
#             # print(" -"*level, "red", "NO count")
#             return
#         if l == m:
#             # print(" -"*level, "red", "COUNT")
#             count[0] += 1
#             return
#         for n in range(m, l+1):
#             # print(" -"*level, "red", n)
#             recurse2(l - n, n, False, count, level+1)
#     else:
#         if l <= m:
#             # print(" -"*level, "gre", "COUNT")
#             count[0] += 1
#             return
#         #End with all grey
#         count[0] += 1
#         # print(" -"*level, "gre", "ALL COUNT")
#         for n in range(1, l+1):
#             # print(" -"*level, "gre", n)
#             recurse2(l - n, m, True, count, level+1)

# recurse2(L, m_red, True, count, 1)
# print(count)
# recurse2(L, m_red, False, count, 1)
# print(count)

    