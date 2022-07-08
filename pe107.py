import numpy as np

W = []
with open("p107_network.txt") as file:
    for line in file:
        L = []
        for x in line[:-1].split(","):
            if x == "-":
                L.append(0)
            else:
                L.append(int(x))
        W.append(L)

# W = [
#     [0,16,12,21,0,0,0],
#     [16,0,0,17,20,0,0],
#     [12,0,0,28,0,31,0],
#     [21,17,28,0,18,19,23],
#     [0,20,0,18,0,0,11],
#     [0,0,31,19,0,0,27],
#     [0,0,0,23,11,27,0]
#     ]

W = np.array(W)



def is_complete(N, current=0, visited=None, verbose=False):
    if visited is None:
        visited = set([0])
    if verbose: print("visiting", current, "visited count",len(visited))
    #Check is a network N is complete from node n
    if len(visited) == N.shape[0]:
        return True
    #iterate
    for i in range(N.shape[0]):
        if (N[current,i] != 0) and (i not in visited):
            visited.add(i)
            if is_complete(N, i, visited):
                return True
    return False

# print(is_complete(W))

def order(N):
    edges = []
    for i in range(N.shape[0]):
        for j in range(i, N.shape[0]):
            if N[i,j] != 0:
                edges.append((N[i,j], (i,j)))
    edges.sort(reverse=True)
    return edges

edges = order(W)
edges_cum_weight = [0]
for w, (a,b) in edges:
    edges_cum_weight.append(edges_cum_weight[-1] + w)
reduction_avaliable = [np.sum(W) - 2*x for x in edges_cum_weight]
# print(reduction_avaliable)
# exit()
best_weight = [10**10]
print("num edges", len(edges))
print("total weight", np.sum(W))

def reduce(N, e, weight, level=0):
    if weight - best_weight[0] > reduction_avaliable[e]:
        return
    #Remove an edge
    for i in range(e,len(edges)):
        if level <= 100: print(" >"*level, i, edges[i])
        M = N.copy()
        # print(weight, np.sum(M))
        w, (a,b) = edges[i]
        # print(w, (a,b))
        M[a,b] = 0
        M[b,a] = 0
        if is_complete(M):
            # print(" >"*level, "complete")
            reduce(M, i+1, weight-2*w, level=level+1)
        else:
            # print(" >"*level, "not complete")
            # print(M)
            if weight < best_weight[0]:
                print("FOUND BEST", weight, (np.sum(W) - weight)/2)
                best_weight[0] = weight

reduce(W, e=0, weight=np.sum(W))
print("SAVINGS", (np.sum(W) - best_weight[0])//2)

#Doesn't actuallly finish running, but the most recently reported result is correct