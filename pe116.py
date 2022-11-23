L = 50

R = [1]*2
for a in range(2, L+1):
    R.append(R[a-1] + R[a-2])
print("R", R)

G = [1]*3
for a in range(3,L+1):
    G.append(G[a-1] + G[a-3])
print("G", G)

B = [1]*4
for a in range(4, L+1):
    B.append(B[a-1] + B[a-4])
print("B", B)

print(L, ":", R[L] + G[L] + B[L] - 3)