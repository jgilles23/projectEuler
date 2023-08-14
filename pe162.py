import numpy as np

def brute(L):
    G = np.full((2,2,2), 0)
    count = 0
    for n in range(1*16**(L-1), 16**L):
        n_hex = hex(n)[2:]
        count += 1
        G[int("0" in n_hex), int("1" in n_hex), int("a" in n_hex)] += 1
    return G[1,1,1]

class Matrix:
    def __init__(self) -> None:
        self.g = [[[0,0], [0,0]], [[0,0], [0,0]]]
    def set(self, pos, v):
        a,b,c = pos
        self.g[a][b][c] = v
    def get(self, pos):
        a,b,c = pos
        return self.g[a][b][c]
    def sum(self, flags):
        a,b,c = flags
        #Sum along axis where true
        s = 0
        for i in range(0, a+1):
            for j in range(0, b+1):
                for k in range(0, c+1):
                    s += self.get((i,j,k))
        return s

def fast(L):
    #Establish G matrix
    G = np.full((2,2,2), 0, dtype=np.uint64)
    #(0>=1, 1>=1, A>=1)
    #Fill out G
    G[0,0,0] = 13**L
    G[0,0,1] = 14**L - G[0,0,:].sum()
    G[0,1,0] = 14**L - G[0,:,0].sum()
    G[1,0,0] = 13*14**(L-1) - G[:,0,0].sum()
    #Next level of G
    G[0,1,1] = 15**L - G[0,:,:].sum()
    G[1,0,1] = 14*15**(L-1) - G[:,0,:].sum()
    G[1,1,0] = 14*15**(L-1) - G[:,:,0].sum()
    #Final level of G
    G[1,1,1] = 15*16**(L-1) - G[:,:,:].sum()
    return G[1,1,1]

def fast2(L):
    G = Matrix()
    #Initial
    G.set((0,0,0), 13**L)
    #Next layer
    G.set((0,0,1), 14**L - G.sum((0,0,1)))
    G.set((0,1,0), 14**L - G.sum((0,1,0)))
    G.set((1,0,0), 13*14**(L-1) - G.sum((1,0,0)))
    #Next layer
    G.set((0,1,1), 15**L - G.sum((0,1,1)))
    G.set((1,0,1), 14*15**(L-1) - G.sum((1,0,1)))
    G.set((1,1,0), 14*15**(L-1) - G.sum((1,1,0)))
    #Final
    G.set((1,1,1), 15*16**(L-1) - G.sum((1,1,1)))
    return G.get((1,1,1))


L_max = 16
count = 0
slow_count = 0
for L in range(3, L_max+1):
    # r = fast(L)
    # count += int(r)
    # print(L, "fast", r)
    r_slow = fast2(L)
    slow_count += r_slow
    print(L, "scnd", r_slow)
print("fast", count)
print("scnd", slow_count)
#Convert to hex
count_hex = hex(slow_count)[2:].upper()
print("ans", count_hex)