#PE 696 Attempt 3
#CONTAINS: fit_tower(tower, pair_allowed=True) - SLOW method for determining if a tower arrangement works
#Use the "tower" method this time
import itertools
from pe696 import brute_iterate_group
import statistics

def fit_tower(tower, pair_allowed=True):
    #Attempts to fit a pair, pungs, and chows in a tower orientation
    #Base case
    s = sum(tower)
    if s == 0:
        return True
    if s%3 == 1:
        return False
    if s%3 == 2 and pair_allowed == False:
        return False
    #Iterate through the possibilities until a tower is found
    for i in range(len(tower)):
        if tower[i] == 0:
            continue
        #Fit a pair
        if tower[i] >= 2 and sum(tower)%3 == 2: 
            #A pair is still required based on the sum
            new_tower = tower[:i] + (tower[i]-2, ) + tower[i+1:]
            if fit_tower(new_tower):
                return True
        #Fit a Chow
        if tower[i] >= 3:
            new_tower = tower[:i] + (tower[i]-3, ) + tower[i+1:]
            if fit_tower(new_tower):
                return True
        #Fit a Pung
        if i <= len(tower) - 3 and tower[i] >= 1 and tower[i+1] >= 1 and tower[i+2] >= 1:
            #Each space for the pung is greater than 1 and i will not exceed and break the script
            new_tower = tower[:i] + (tower[i]-1, tower[i+1]-1, tower[i+2]-1) + tower[i+3:]
            if fit_tower(new_tower):
                return True
    #Did not find any solutions
    return False
        

def brute_make_towers(n, t):
    #Make towers give suits and t triples + 1 pair
    target = 3*t + 2
    towers = itertools.product(range(5), repeat=n)
    results = []
    for tower in towers:
        if sum(tower) != target:
            continue
        if fit_tower(tower) == False:
            continue
        #Passed all the tests, a valid result
        results.append(tower)
    return results

def iterate_sub_tower(tower, remaining, n=10**12):
    if remaining == 0:
        return [tower]
    if len(tower) >= n:
        return []
    ret = []
    for j in range(1,min(remaining+1, 5)):
        new_tower = tower + (j,)
        ret += iterate_sub_tower(new_tower, remaining - j)
    return ret

def sub_tower(total):
    #Produces all possible "continuous" towers (aka not broken up by 0s) given a total for the sub_tower
    if total%3 == 1:
        return []
    ret = []
    if total%3 == 2:
        #Pair is required to be in the subtotal
        for t in range(2,total+1,3):
            ret += iterate_sub_tower(tuple(),t)
    #Iterate through the triples
    for t in range(3,total+1,3):
        ret += iterate_sub_tower(tuple(),t)
    #Determine which returns are acceptable
    new_ret = {}
    for r in ret:
        if fit_tower(r):
            if sum(r) in new_ret:
                new_ret[sum(r)].append(r)
            else:
                new_ret[sum(r)] = [r]
    return new_ret

def add_at(x,t,i):
    #Add x to the value of tuple t at position i
    return t[:i] + (t[i]+x,) + t[i+1:]

def generate_sub_towers(t):
    #Generate all of the sub towers that include up to 1 pair and t triples
    total = 3*t + 2
    towers = set([(2,),(3,),(1,1,1)])
    check_towers = {t for t in towers}
    new_check_towers = set()
    #Function for checking and adding
    def check(tower):
        if tower in towers:
            return
        towers.add(tower)
        new_check_towers.add(tower)
    #Function for making a new tuple and checking it
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
                return
        check(tuple(T))
    while len(check_towers) > 0:
        avg_len = statistics.mean([len(tower) for tower in check_towers])
        print("Checking {:,} towers (avg len {:.3}): ".format(len(check_towers), avg_len), end="", flush=True)
        #Iterate through all the towers in the current check
        k = 0
        for tower in check_towers:
            if k%10000==0: print(k//10000,end="-",flush=True)
            k += 1
            #If sum too large to add a pair, skip
            if sum(tower) > total - 2:
                continue
            #Add a pair
            if sum(tower)%3 != 2:
                for i in range(-1, len(tower)+1):
                    add_tuple((2,), tower, i)
            #if sum too large to add a tripple, skip
            if sum(tower) > total - 3:
                continue
            #Add a chow
            for i in range(-1, len(tower)+1):
                add_tuple((3,), tower, i)
            #Add a pung
            for i in range(-3,len(tower)+1):
                add_tuple((1,1,1), tower, i)
        print("")
        #print(new_check_towers)
        check_towers = new_check_towers
        new_check_towers = set()
    return towers
    


'''
n = 8
t = 2
s = 1
#Origional brute
q = brute_iterate_group([],n,s,t)
print("org brute (n={:}, s={:}, t={:}) winning hands: {:,}".format(n, s,t,len(q)))

q = brute_make_towers(n,t)
print("new brute (n={:}, s={:}, t={:}) winning hands: {:,}".format(n, s,t,len(q)))
'''


def main():
    t = 3

    if t <= 3:
        print("Brute")
        brute_q = sub_tower(3*t + 2)
        for key in brute_q:
            print(key, ":", brute_q[key])
        print(sum([len(brute_q[key]) for key in brute_q]))

    print("Generate")
    q = generate_sub_towers(t)
    print(len(q))

#main()