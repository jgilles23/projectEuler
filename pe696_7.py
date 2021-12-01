#Project Euler 696 Try #6
#CONTAINS:
#Determine the characteristic endings of a block
import itertools

#Make a lookup table for storing previous towers that were checked
lookup = {tuple():True}
def check_tower(T, remainder=None, verified=False):
    '''Faster function to check if a tower is allowable
    If remainder =  None: pair is allowed but not required
                    0: pair is NOT allowed
                    2: pair is REQUIRED
    '''
    #Verify sum as required
    if not verified:
        r = sum(T)%3
        if r == 1:
            #A remainder of 1 is never allowed
            return False
        elif remainder is None:
            #Allow any non-1 remainder
            remainder = r
        elif remainder != r:
            #Allow only the supplied remainder
            return False
    #Base case
    if not T:
        return True
    #Check if there are zeros on the end, filter out
    if T[0] == 0:
        return check_tower(T[1:], verified=True, remainder=remainder)
    if T[-1] == 0:
        return check_tower(T[:-1], verified=True, remainder=remainder)
    #Split the tower at zeros
    if 0 in T:
        i = T.index(0)
        if check_tower(T[:i],remainder) and check_tower(T[i+1:],remainder):
            lookup[T] = True
            return True
    #Lookup to see if the tower has been found before
    if T in lookup:
        return lookup[T]
    if (rT := T[::-1]) in lookup: #See if reverse has been found
        return lookup[rT]
    #Iterate through sub-problems to check
    #Remove a pair first, where applicable
    if remainder == 2:
        for i in range(len(T)):
            if T[i] >= 2:
                nT = T[:i] + (T[i] - 2,) + T[i+1:]
                if check_tower(nT, verified=True, remainder=0):
                    lookup[T] = True
                    return True
        #Could not remove a pair so failure (since when a pair can be removed it must be removed)
        lookup[T] = False
        return False
    #Assume remainder is 0 from here on
    #Remove a pung
    for i in range(len(T) - 2):
        if T[i]>=1 and T[i+1]>=1 and T[i+2]>=1:
            nT = T[:i] + (T[i]-1, T[i+1]-1, T[i+2]-1) + T[i+3:]
            if check_tower(nT, verified=True, remainder=0):
                lookup[T] = True
                return True
    #If any of the numbers are <=2 a pung removal would be required
    if any([x<=2 for x in T]):
        #Therefore, when a chow is not found, failure
        lookup[T] = False
        return False
    #Remove a chow
    for i in range(len(T)):
        if T[i] >= 3:
            nT = T[:i] + (T[i] - 3,) + T[i+1:]
            if check_tower(nT, verified=True, remainder=0):
                lookup[T] = True
                return True
    #All checks failed, the tower is not possible
    lookup[T] = False
    return False

lefts = [{}, {}, {}]
for left in itertools.product(range(0,5), repeat=2):
    for i in range(3):
        lefts[i][left] = set()
    for block in itertools.product(range(1,5), repeat=4):
        for right in itertools.product(range(0,5), repeat=2):
            tower = left + block + right
            if check_tower(tower):
                lefts[sum(tower)%3][left].add(block + right)

def get_links(lefts0):
    links = {left:(len(lefts0[left])>0) for left in lefts0}
    for left in lefts0:
        for second in lefts0:
            if left >= second:
                continue
            x = lefts0[left].symmetric_difference(lefts0[second])
            if not x:
                links[second] = left
    for key in links:
        print(key,":",links[key])
    return links

#print(lefts[0])
get_links(lefts[2])
