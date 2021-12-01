#Project Euler #696, Try #6
#CONTAINS:
#Attempt to re-make _5 for creating block graphs, but using tables this time

import itertools
from typing import final
from pe696_5 import check_tower as old_check_tower
import time

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



class Table:
    #Class for more easily manipulating towers and tracking thier sums vs. lengths
    def __init__(self,X=None):
        """Class for manipulating towers based on their sums and lengths
        Inputs:
            X = Starting tuple
        """
        self.d = {}
        if X == (0,0,0,0):
            self.d[0] = {0:1}
        elif X:
            self.iadd_tuple(X)
    
    def __getitem__(self, *args, **kwargs):
        return self.d.__getitem__(*args, **kwargs)
    
    def __repr__(self):
        st = self.d.__repr__()
        st = "<" + st[1:-1] + ">"
        return st
    
    #def __add__(self,X): NOT USED, only iadd is used for now to modify in place
    
    def iadd_tuple(self,X):
        s = sum(X)
        l = len(X)
        if s not in self.d:
            self.d[s] = {}
        if l not in self.d[s]:
            self.d[s][l] = 1
        else:
            self.d[s][l] += 1
    
    def idel_tuple(self,X):
        s = sum(X)
        l = len(X)
        self.d[s][l] -= 1
    
    def iadd_table(self,X):
        for s in X.d:
            for l in X[s]:
                if s not in self.d:
                    self.d[s] = {}
                if l not in self.d[s]:
                    self.d[s][l] = X[s][l]
                else:
                    self.d[s][l] += X[s][l]
    
    def iadd_product(self, tally, graph):
        """Iterate the tally to the next level using the graph and add the result to self (Table) modify self in place
        """
        for left in tally.d:
            for right in graph[left]:
                self.iadd_table(tally[left].mult(graph[left][right]))
    
    def add_table(self,other):
        new = Table()
        new.d = {s:{l:self.d[s][l] for l in self.d[s]} for s in self.d}
        new.iadd_table(other)
        return new
    
    def mult(self,other):
        new = Table()
        for self_s in self.d:
            for self_l in self.d[self_s]:
                for other_s in other.d:
                    for other_l in other.d[other_s]:
                        new_s = self_s + other_s
                        new_l = self_l + other_l
                        if new_s not in new.d:
                            new.d[new_s] = {}
                        if new_l not in new.d[new_s]:
                            new.d[new_s][new_l] = 0
                        new.d[new_s][new_l] += self.d[self_s][self_l] * other.d[other_s][other_l]
        return new
    
    def sum(self):
        total = 0
        for s in self.d:
            total += sum(self.d[s].values())
        return total
    
    def flush(self, max_sum):
        for s in list(self.d.keys()):
            if s > max_sum:
                del self.d[s]
    
    def compare(self,other,return_exception=False):
        #Really bad compare function
        try:
            for s in self.d:
                for l in self.d[s]:
                    if self.d[s][l] != other.d[s][l]:
                        if return_exception:
                            return "Value mis-match: s:{:} l:{:} sum0:{:} sum1:{:}".format(s,l,self.d[s][l], other.d[s][l])
                        else:
                            return False
            for s in other.d:
                for l in other.d[s]:
                    if self.d[s][l] != other.d[s][l]:
                        if return_exception:
                            return "Value: mis-match: s:{:} l:{:} sum0:{:} sum1:{:}".format(s,l,self.d[s][l], other.d[s][l])
                        else:
                            return False
            return True
        except:
            if return_exception:
                return "Index mis-match: s:{:} l:{:}".format(s,l,self.d[s][l], other.d[s][l])
            else:
                return False
    
    def trips(self):
        for s in self.d:
            for l in self.d[s]:
                yield (s,l,self.d[s][l])
    #__rmul__ = __mul__
    #__radd__ = __add__
    #__iter__ to use "in" 

class Graph:
    #Class for holding a graph of the possible stats and connections
    def __init__(self, lefts, middles, rights, composition_function,remainder=0):
        self.d = {left:{right:Table() for right in rights} for left in lefts} #Contans tables summarizing the graphed values
        self.d_expanded = {left:{right:[] for right in rights} for left in lefts} #Contains the actual items in the count
        self.lefts = lefts
        self.rights = rights
        #Compose the graph of Table Class
        for middle in middles:
            for left in self.lefts:
                for right in self.rights:
                    new_tower = composition_function(left,middle,right)
                    if any([x<0 or x>4 for x in new_tower]):
                        continue
                    flag = check_tower(new_tower, remainder)
                    #print(new_tower, flag)
                    if flag:
                        self.d[left][right].iadd_tuple(middle)
                        self.d_expanded[left][right].append(middle)
    
    def __getitem__(self, *args, **kwargs):
        return self.d.__getitem__(*args, **kwargs)
    
    def __repr__(self):
        st = ""
        for left in self.d:
            st += "\n"
            st += str(left) + " : " + str(self[left]) + "\n"
        return st
    
    def remove(self,left,block,right):
        """Remove an item from the graph"""
        if block in  self.d_expanded[left][right]:
            self.d[left][right].idel_tuple(block)
            self.d_expanded[left][right].remove(block)
    
    def sum(self):
        total = 0
        for left in self.d:
            total += sum([table.sum() for table in self.d[left].values()])
        return total
    
    def product(self, other):
        """Outputs a dict of all the items generated by combining all the possible combinations of two graphs
        (left bridge, block0, (mid bridge omitted), block1, right bridge)"""
        tracking = {}
        for left in self.d:
            for mid in self[left]:
                for block0 in self.d_expanded[left][mid]:
                    for right in other[mid]:
                        for block1 in other.d_expanded[mid][right]:
                            #Add item, track duplicates
                            item = (left, block0, block1, right)
                            if item in tracking:
                                raise Exception("Found duplication issue inside product.")
                            else:
                                tracking[item] = mid
        return tracking
                                


class Tally:
    def __init__(self,d=None):
        if not d:
            self.d = {}
        else:
            self.d = d
    
    def __getitem__(self,*args,**kwargs):
        return self.d.__getitem__(*args, **kwargs)

    def __repr__(self):
        return self.d.__repr__()
    
    def iadd(self, other):
        #Add a Tally to this tally
        for key in other.d:
            if key not in self.d:
                self.d[key] = other.d[key]
            else:
                self.d[key].iadd_table(other.d[key])
    
    def iterate(self, graph):
        """Iterate the Tally in place by adding another level in the Tally using the Graph object. Returns a new Tally object"""
        new = Tally()
        for left in self.d:
            for right in graph[left]:
                if not right in new.d:
                    new.d[right] = Table()
                new[right].iadd_table(self.d[left].mult(graph[left][right]))
        return new 
    
    def sum(self):
        return sum([self.d[key].sum() for key in self.d])


def brute_towers(min_sum=1, max_sum=1000, min_length=1, max_length=None, require_pair=False, allow_pair=True, return_tuples=False):
    if not max_length:
        raise Exception("brute_towers requires max_length parameter to be specified")
    if require_pair and not allow_pair:
        raise Exception("brute_towers: If a pair is required (input: require_pair=True) then pairs must be allowed (input: allow_pair=True (default))")
    if return_tuples:
        tuples = []
    #Determine what the remainder value should be
    if require_pair:
        remainder = 2
    elif allow_pair:
        remainder = None
    else:
        remainder = 0
    count = 0
    table = Table()
    printed = False
    for length in range(min_length,max_length+1):
        max_value = min(max_sum - length + 1, 4)
        for tower in itertools.product(range(1,max_value+1), repeat=length):
            s = sum(tower)
            if require_pair and s%3 != 2:
                continue
            if s >= min_sum and s <= max_sum:
                if check_tower(tower, remainder=remainder):
                    count += 1
                    table.iadd_tuple(tower)
                    if return_tuples:
                        tuples.append(tower)
                    if count%1000 == 0: 
                        print(count//1000, end="-", flush=True)
                        printed = True
    if printed:
        print("")
    if return_tuples:
        return table, tuples
    else:
        return table

print("Generating Graphs:")

block_len = 4
Z = (0,0,0,0)
bridges = {(0,0,0,0):"Z", (1,1,1,0):"w", (0,1,1,1):"e", (2,2,2,0):"W", (1,2,2,1):"m", (0,2,2,2):"E", (2,3,3,1):"L", (1,3,3,2):"R", (2,4,4,2):"M"}
bridges = [k for k in bridges]
blocks = list(itertools.product(range(1,5), repeat=block_len))
caps = [itertools.product(range(1,5), repeat=i) for i in range(1,4)]
caps = [x for cap in caps for x in cap]

func = lambda left, middle, right: (middle[0]-left[2], middle[1]-left[3]) + middle[2:block_len-2] + (middle[block_len-2]-right[0], middle[block_len-1]-right[1])
block_graph = Graph(lefts=bridges, middles=blocks, rights=bridges, composition_function=func, remainder=0)
#print("Z-Z",block_graph[Z][Z])
print("   block_graph generated: size", block_graph.sum())
"""
block_graph_2 = Graph(lefts=bridges, middles=blocks, rights=bridges, composition_function=func, remainder=2)
print("   block_graph_2 generated: size", block_graph_2.sum())
"""


def func(left, middle, right):
    if len(middle) == 1:
        return (middle[0] - left[2], 0 - left[3])
    else:
        return (middle[0] - left[2], middle[1] - left[3]) + middle[2:]
cap_graph = Graph(lefts=bridges, middles=caps, rights=[Z], composition_function=func, remainder=0)
print("   cap_graph generated: size", cap_graph.sum())
"""
cap_graph_2 = Graph(lefts=bridges, middles=caps, rights=[Z], composition_function=func, remainder=2)
print("   cap_graph_2 generated: size", cap_graph_2.sum())
"""

"""
#Need to prove that the combinations of block graphs and cap graphs are unique, otherwise will get problems with double counting
def intersect(items0, items1):
    set0 = set(items0.keys())
    set1 = set(items1.keys())
    intersection = set0.intersection(set1)
    duplicates = {}
    for I in intersection:
        duplicates[I] = [items0[I], items1[I]]
    return duplicates
#Find all of the double counts
items0 = block_graph.product(cap_graph_2)
items1 = block_graph_2.product(cap_graph)
duplicates = intersect(items0, items1)
#for item in duplicates:
#    if item[0]==Z and item[3]==Z and sum(item[1]+item[2])==11 and len(item[1]+item[2])==6:
#        print(item,":",d[item])
#Remove the double counts from cap_graph_2
for d in duplicates:
    #d is of the form (left, block0, block1, right):[mid0, mid1]
    cap_graph_2.remove(duplicates[d][0], d[2], d[3]) #(mid1, block1, right)
print("   cap_graph_2 clashes removed: size", cap_graph_2.sum())
"""

#Iterativly generate tables for higher sums (and longer sequences)
def generate_table(t):
    #Generate a table up to the sum of 3*t (still ignoring the double)
    max_length = 3*t
    final_table_0 = Table()
    final_table_2 = Table()
    tally_0 = Tally({Z:Table(Z)})
    tally_2 = Tally()
    L = 0
    while L < max_length:
        if t>5: 
            print(L,"of",max_length)
        #NON-PAIR plus non-pair caps = 0
        final_table_0.iadd_product(tally_0, cap_graph)
        #NON-PAIR plus pair caps = 2
        #final_table_2.iadd_product(tally_0, cap_graph_2)
        #PAIR plus non-pair caps = 2
        #final_table_2.iadd_product(tally_2, cap_graph)
        L += 3
        if L >= max_length:
            break
        #Create the next set of tallies for the next iteration
        #PAIR plus non-pair = 2
        #tally_2 = tally_2.iterate(block_graph)
        #NON-PAIR plus pair = 2
        #tally_2.iadd(tally_0.iterate(block_graph_2))
        #NON-PAIR plus non-pair = 0
        tally_0 = tally_0.iterate(block_graph)
        #Add the tallies that have ended to the final tables
        final_table_0.iadd_table(tally_0[Z])
        #final_table_2.iadd_table(tally_2[Z])
        L += 1
    #Remove sums that are too large
    final_table_0.flush(max_sum=max_length)
    #final_table_2.flush(max_sum=max_length)
    #final_table_combined = final_table_0.add_table(final_table_2)
    #Return the generated tables
    return final_table_0#, final_table_2, final_table_combined

print("")
t = 5
table_0 = generate_table(t)
#print("Final Table:", str(table_0))
print("new   method table total:", table_0.sum())
if True: #Check answer via brute force
    brute_table = brute_towers(min_sum=1, max_sum=3*t, min_length=1, max_length=3*t, allow_pair=False)
    #print("Brute Table:", str(brute_table.d))
    print("brute method table total:", brute_table.sum())
    print("Are the tables the same?",table_0.compare(brute_table, return_exception=True))

exit()

s = 11
l = 6
print("new method", table_2[s][l])
b_table, b_tuples = brute_towers(min_sum=s, max_sum=s, min_length=l, max_length=l, require_pair=True, return_tuples=True)
print("brute method", b_table.sum())
#print(b_tuples)

print("Try this manually")
#Two ways for the error to occur: when adding a 2_cap to a 0_block or when adding a 0_cap to a 2_block. Need to test both
manual_towers = []
for right in block_graph[Z]:
    for block in block_graph.d_expanded[Z][right]:
        for cap in cap_graph_2.d_expanded[right][Z]:
            tower = block + cap
            if sum(tower) == s and len(tower) == l:
                manual_towers.append(tower)
            if tower == (1, 1, 4, 1, 1, 3):
                print("first", tower, right)
for right in block_graph_2[Z]:
    for block in block_graph_2.d_expanded[Z][right]:
        for cap in cap_graph.d_expanded[right][Z]:
            tower = block + cap
            if sum(tower) == s and len(tower) == l:
                manual_towers.append(tower)
            if tower == (1, 1, 4, 1, 1, 3):
                print("second", tower, right)
#We are double counting something. But what are we double counting?
duplicates = []
for i in range(len(manual_towers)-1):
    if manual_towers[i] in manual_towers[i+1:]:
        duplicates.append(manual_towers[i])
print("duplicates",duplicates)


exit()

#METHOD FOR CHECKING ITEMS RELATED TO ADDING PAIRS TO THE GRAPH
print("\nPAIR CHECKING")
count = 0
for tower in block_graph.d_expanded[Z][Z]:
    count += sum([x<=2 for x in tower])
print("Count by adding pairs", count)
print("Count by brute force", brute_towers(min_length=4, max_length=4, require_pair=True).sum())
