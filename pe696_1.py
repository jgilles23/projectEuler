#Preoject Euler 691 - Try again
import itertools

def to_group(X):
    X_sort = sorted(X)
    last_item = None
    group = []
    for item in X_sort:
        if item == last_item:
            group[-1] += 1
        else:
            group.append(1)
            last_item = item
    group.sort()
    return tuple(group)

def print_partition(P, s=0, t=0):
    print("GROUP COUNTS s={:}, t={:}".format(s,t))
    sm = 0
    for key in P:
        print("  ",key,":",P[key])
        sm += P[key]
    print("   total: {:,}".format(sm))

def brute_group_counts(s, t, verbose=True):
    a = itertools.product(range(s),repeat=t)
    groups = [to_group(x) for x in a]
    counts = {}
    for g in groups:
        if g in counts:
            counts[g] += 1
        else:
            counts[g] = 1
    if verbose:
        print_partition(counts,s,t)        
    return counts

def parition(s, t):
    #Paritions t groups of cards, applying s suits
    if s==1 and t==1:
        return {(1,):1}
    #Paritions where s == t - 1
    lower_P = parition(t-1, t-1)
    #Scale up s by 1 each iteration until equal to input s
    for new_s in range(t, max(t,s)+1):
        for g in lower_P:
            #e.g new_s=5 (1,1,2):10 <- 5*10/(5-3)
            lower_P[g] = lower_P[g]*new_s//(new_s - len(g))
    #Scale up t by 1
    P = {}
    for g in lower_P:
        #Add 1 to existing groups
        for i in range(len(g)):
            new_g = g[:i] + (g[i]+1,) + g[i+1:]
            new_g = tuple(sorted(new_g))
            if new_g in P:
                P[new_g] += lower_P[g]
            else:
                P[new_g] = lower_P[g]
        #Add 1 to the end of the group
        new_g = (1,) + g
        #e.g. new_s = 7 (1,1,2):210 <- 210*(7-3)
        new_count = lower_P[g]*(new_s - len(g))
        if new_g in P:
            P[new_g] += new_count
        else:
            P[new_g] = new_count
    #Cutoff where s < t
    if s < t:
        raise Exception("Method not ready for s < t")
    return P

        



s = 5 #Number of suits to choose from
t = 3 #Number of like objects to use

#print("Slow method")
#brute_group_counts(s,t)

print("Fast method")
q = parition(s,t)
print_partition(q,s,t)



    
