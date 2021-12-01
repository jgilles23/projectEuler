#PE 696 Attempt #4
#Try to make sub-blocks on this one
from pe696_3 import fit_tower
import itertools

def make_block_graph(block_len):
    #Make a block graph of blocks of size block_len
    blocks = list(itertools.product(range(5),repeat=block_len))
    towers = []
    print(len(blocks))
    for i,block in enumerate(blocks):
        if i%10000==0: print(i//10000)
        if fit_tower(block):
            towers.append((block[0]*10+block[1], block[2]*10+block[3], block[4]*10+block[5]))
    graph = {}
    for tower in towers:
        left,middle,right = tower
        if middle not in graph:
            graph[middle] = {}
        if left not in graph[middle]:
            graph[middle][left] = []
        graph[middle][left].append(right)
    return graph


def add_tuple(X,T,i):
    #Add tuple X, to tuple T at position i -- assumes values out of range are 0
    X = list(X)
    T = list(T)
    if i < 0:
        T = [0]*abs(i) + T
        i = 0
    if i + len(X) >= len(T):
        T = T + [0]*(i + len(X) - len(T))
    for j in range(len(X)):
        T[i+j] += X[j]
        if T[i+j] > 4:
            return False
    return tuple(T)

right_extensions = [(0,0,0,0), (0,1,1,1), (0,2,2,2), (1,1,1,0), (1,2,2,1), (1,3,3,2), (2,2,2,0), (2,3,3,1), (2,4,4,2)]
left_extensions = [tuple(x[::-1]) for x in right_extensions]
#print(right_extensions, left_extensions)

def block_graph(block_len):
    #Make a block graph of blocks of size block_len
    blocks = list(itertools.product(range(5),repeat=block_len))
    ##blocks = blocks[0::len(blocks)//2]
    count = 0
    graph = {}
    for i,block in enumerate(blocks):
        if i%10==0: print("{:,} of {:,}".format(i,len(blocks)))
        for R in right_extensions:
            with_right = add_tuple(R, block, block_len-2)
            if with_right == False:
                continue
            for L in left_extensions:
                tower = add_tuple(L, with_right, -2)
                if tower == False:
                    continue
                if fit_tower(tower, pair_allowed=False):
                    #print(block,":",tower)
                    count += 1
                    if block not in graph:
                        graph[block] = {}
                    if L not in graph[block]:
                        graph[block][L] = set()
                    graph[block][L].add(R)
    print(count)
    return graph


def main():
    g = block_graph(4)
    for k in g:
        print("".join([str(x) for x in k]),":")
        for l in g[k]:
            print("  ","".join([str(x) for x in l]),":",["".join([str(x) for x in r]) for r in g[k][l]])

#main()