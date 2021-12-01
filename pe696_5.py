#Project Euler Problem #696 Try 5, date 20210508
#CONTAINS: check_tower(T, sum_verified=False, allow_pair=True) - FAST method for determining if a given tower works 
import itertools
from pe696_3 import fit_tower
import time
import numpy as np

#Make a lookup table for storing previous towers that were checked
lookup = {tuple():True}
def check_tower(T, sum_verified=False, allow_pair=True):
    #Faster function to check if a tower is allowable
    #Return in base case
    if not T:
        return True
    #Verify the sum if needed
    if not sum_verified:
        if allow_pair:
            #Don't allow pairs unless r=2
            r = sum(T)%3
            if r == 1:
                return False
            if r == 3:
                allow_pair == False
        elif sum(T)%3 != 0:
            #If pairs not allowed, return all bad sums
            return False
    #Check if there are zeros on the end, filter out
    if T[0] == 0:
        return check_tower(T[1:], sum_verified=True, allow_pair=allow_pair)
    if T[-1] == 0:
        return check_tower(T[:-1], sum_verified=True, allow_pair=allow_pair)
    #Lookup to see if the tower has been found before
    if T in lookup:
        return lookup[T]
    if (rT := T[::-1]) in lookup:
        return lookup[rT]
    #Iterate through sub-problems to check
    #Remove a pair, if applicable
    if allow_pair:
        for i in range(len(T)):
            if T[i] >= 2:
                nT = T[:i] + (T[i] - 2,) + T[i+1:]
                flag = check_tower(nT, sum_verified=True, allow_pair=False)
                lookup[nT] = flag
                if flag:
                    return True
    #Remove a chow
    for i in range(len(T)):
        if T[i] >= 3:
            nT = T[:i] + (T[i] - 3,) + T[i+1:]
            flag = check_tower(nT, sum_verified=True, allow_pair=allow_pair)
            lookup[nT] = flag
            if flag:
                return True
    #Remove a pung
    for i in range(len(T) - 2):
        if T[i]>=1 and T[i+1]>=1 and T[i+2]>=1:
            nT = T[:i] + (T[i]-1, T[i+1]-1, T[i+2]-1) + T[i+3:]
            flag = check_tower(nT, sum_verified=True, allow_pair=allow_pair)
            lookup[nT] = flag
            if flag:
                return True
    return False

#TODO - Generate Caps for the end to make different lengths
#Idea for making the zero_list


#GOAL: Generate the number of possible towers for each length of tower n and each relevant sum of tower s
#SUB PROBLEM: Solve the goal, ignoring pairs

def join(T):
    return "".join([str(x) for x in T])

bridges = {(0,0,0,0):"Z", (1,1,1,0):"w", (0,1,1,1):"e", (2,2,2,0):"W", (1,2,2,1):"m", (0,2,2,2):"E", (2,3,3,1):"L", (1,3,3,2):"R", (2,4,4,2):"M"}
#bridges = {bridge:join(bridge) for bridge in bridges}
#print(bridges)
def block_graph(block_len):
    #Make a graph of all the blocks and how they fit together
    graph = {v:{w:[] for w in bridges.values()} for v in bridges.values()}
    for block in itertools.product(range(1,5), repeat=block_len):
        for left in bridges:
            for right in bridges:
                #Custom subtraction formula
                new_block = (block[0]-left[2], block[1]-left[3]) + block[2:block_len-2] + (block[block_len-2]-right[0], block[block_len-1]-right[1])
                if new_block[0]<0 or new_block[1]<0 or new_block[block_len-2]<0 or new_block[block_len-1]<0:
                    continue
                flag = check_tower(new_block, allow_pair=False)
                if flag:
                    graph[bridges[left]][bridges[right]].append(join(block))
    return graph

caps = [[]] + [itertools.product(range(1,5), repeat=i) for i in range(1,4)]
caps = {x:join(x) for cap in caps for x in cap}
#print(caps)
def cap_graph(block_len):
    cap_graph = {l:{cap:[] for cap in caps.values()} for l in bridges.values()}
    for block in itertools.product(range(1,5), repeat=block_len):
        for left in bridges:
            for cap in caps:
                #Custom concatination formula
                new_block = (block[0]-left[2], block[1]-left[3]) + block[2:] + cap
                if new_block[0]<0 or new_block[1]<0:
                    continue
                flag = check_tower(new_block, allow_pair=False)
                if flag:
                    cap_graph[bridges[left]][caps[cap]].append(join(block))
    """
    for l in cap_graph:
        #print()
        d = {r:len(cap_graph[l][r]) for r in cap_graph[l]}
        print(l,":", sum(d.values()))
    """
    return cap_graph

def add_level(gc,count):
    new_count = {k:0 for k in gc}
    for l in count:
        for r in gc[l]:
            new_count[r] += count[l]*gc[l][r]
    return new_count

def Z_kX(gc, k, start_counts={"Z":1}):
    #Iterate through the graph counts, k number of times to get a count of all the ways to combine blocks together k times
    counts = {key:start_counts[key] for key in start_counts}
    for _ in range(k):
        counts = add_level(gc, counts)
    return counts



def main():
    g = block_graph(4)
    gc ={l:{r:len(g[l][r]) for r in g[l]} for l in g}
    for key in g:
        print(key,":",gc[key],sum(gc[key].values()))

    #Find count Z-kX-Z
    k = 1
    #Brute force it
    s = 0
    c = 0
    for block in itertools.product(range(1,5), repeat=(4*k)):
        c+= 1
        if c%100000==0:
            print("{:,} of {:,}".format(c,4**(4*k)))
        s += check_tower(block,allow_pair=False)
    print("brute Z-X-X-Z", s)
    print("fast Z-X-X-Z", Z_kX(gc,k)["Z"])

    cap_graph(4)

def main2():
    g = block_graph(4)
    gc ={l:{r:len(g[l][r]) for r in g[l]} for l in g}
    print("Previous", sum([sum(gc[key].values()) for key in gc]))

    cg = cap_graph(4)
    cgc = {l:{r:len(cg[l][r]) for r in cg[l]} for l in cg}
    print("Previous Cap Graph", sum([sum(cgc[key].values()) for key in cgc]))

#main()
#main2()