L = 50

C = [1, 1, 2, 4]

for a in range(len(C), L+1):
    C.append(C[a-1] + C[a-2] + C[a-3] + C[a-4])
print(L,":", C[L])

