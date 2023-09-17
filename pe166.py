# import numpy as np

# A = np.full((4, 4), 0)

# Fill the 3x3 with things less than 12
# Fill both edges
# Test diagonal
# Fill the corner
# Test diagonal

# pointer = 0

# count = 0
# while pointer < 9:
#     if pointer == 0:
#         count += 1
#     p_row, p_col = pointer//3, pointer%3
#     # Increment at pointer
#     A[p_row, p_col] += 1
#     if A[p_row, p_col] > 9:
#         A[p_row, p_col] = 0
#         pointer += 1
#     elif np.sum(A[p_row, :]) > 12:
#         A[p_row, p_col] = 0
#         pointer += 1
#     elif np.sum(A[:, p_col]) > 12:
#         A[p_row, p_col] = 0
#         pointer += 1
#     else:
#         pointer = 0
# print(count)

# three = []
# for a in range(10):
#     for b in range(10):
#         for c in range(10):
#             if (d := 12 - a - b - c) >= 0:
#                 three.append((a, b, c, d))
# print(len(three))

# count = 0
# for A in three:
#     for B in three:
#         #Prelim test each column & main diagonal & anti diagonal
#         if  A[0] + B[0] > 12 or \
#             A[1] + B[1] > 12 or \
#             A[2] + B[2] > 12 or \
#             A[3] + B[3] > 12 or \
#             A[0] + B[1] > 12 or \
#             A[3] + B[2] > 12:
#             continue
#         for C in three:
#             #Each colum and main diagonal
#             if  (m := 12 - A[0] - B[0] - C[0]) < 0 or \
#                 (n := 12 - A[1] - B[1] - C[1]) < 0 or \
#                 (o := 12 - A[2] - B[2] - C[2]) < 0 or \
#                 (p := 12 - A[0] - B[1] - C[2]) < 0: #main diagonal
#                 continue
#             # Bottom row & anti diagonal
#             if  m + n + o + p != 12 or \
#                 A[3] + B[2] + C[1] + m != 12:
#                 continue
#             count += 1
# print(count)

# USLESS, JUST HAS TO BE A MAGIC SQUARE OF 4x4 is what we are looking for

# Construct a list of 4 x 1 arrays with thier respective sums
sum_to_lines = {total: {} for total in range(0, 9*4 + 1)}
for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                item = sum_to_lines[a + b + c + d]
                if a not in item:
                    item[a] = {b: {c: d}}
                elif b not in item[a]:
                    item[a][b] = {c: d}
                else:
                    item[a][b][c] = d
# for total in range(0, 9*4 + 1):
#     print("TOTAL", total)
#     for a in sum_to_lines[total]:
#         print("    ", a, sum_to_lines[total][a])

# count = 0
# for total in sum_to_lines:
#     print("total:", total)
#     item = sum_to_lines[total]
#     for a in item:
#         for b in item[a]:
#             for e in item[a]:
#                  for f in item[a].keys() & item[e].keys() & item[a].keys():
#                      for c in item[a][b]:
#                          d = total - a - b - c
#                          for g in item[e][f].keys() & item[c].keys():
#                              h = total - e - f - g
#                              for k in item[a][f].keys() & item[c][g].keys():
#                                 p = total - a - f - k
#                                 l = total - d - h - p
#                                 o = total - c - g - k
#                                 for i in item[a][e]:
#                                     m = total - a - e - i
#                                     j = total - i - k - l
#                                     n = total - m - o - p
#                                     if j >= 0 and n >= 0 and b + f + j + n == total and m + j + g + d == total:
#                                         # if total == 12 and a==6 and b==3:
#                                         #     print("total:", total)
#                                         #     print(np.array([[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]]))
#                                         count += 1
# print(count)

# 802819
# 10776106

count = 0
for total in sum_to_lines:
    print("total:", total)
    item = sum_to_lines[total]
    for a in item:
        for b in item[a]:
            for c in item[a][b]:
                d = item[a][b][c]:
                for f in item[a].keys() & item[b].keys():
                    for g in item[f].keys() & item[c].keys():
                        for h in item[f][g].keys() & item[d].keys():
                            if (e := item[f][g][h]) in item[a]
                                for k in item[a][f].keys() & item[c][g].keys():
                                    for l in item[k].keys() & item[d][h].keys():
                                        for i in item[k][l].keys() & item[a][e].keys():
                                            if (j =: item[k][l][i]) in item[b][f]:
                                                if (p := item[a][f][k]) == item[d][h][l]
                                                    if (m := item[d][g][j]) == item[a][e][i]
                                                        if (n := item[b][f][j])
                                                            for o in item:
                                                                count += 1
