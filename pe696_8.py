#Attempt #8 at solving PE #696
import itertools

reducer = {}

def check(triple):
    if triple == False:
        return False
    for v in triple[1:]:
        if v < 0:
            return False
    return triple

def sub(triple, other):
    t = (triple[0], triple[1] - other[0], triple[2] - other[1], triple[3] - other[2])
    return check(t)

def take_down(triple):
    #If called on false, return false
    if triple == False:
        return False
    #Check if this is a tuple of tuples:
    if not(triple[0]=="n" or triple[0]=="y"):
        ret = []
        for t in triple:
            ret.append(take_down(t))
        return tuple(ret)
    #Return in base case
    if triple[1:] == (0,0,0):
        return triple
    #Shift on ending zeros
    if triple[2:] == (0,0):
        return (triple[0], 0, triple[1], triple[2])
    #Extract
    pre, a, b, c = triple
    if pre=="n":
        if a==0:
            if b >= 3:
                return sub(triple, (0,3,0))
            elif b==0 and c >= 3:
                return sub(triple, (0,0,3))
            elif b==1 and c==4:
                return sub(triple, (0,0,3))
            pass
        elif a==1:
            return sub(triple,(1,1,1))
        elif a==2:
            return sub(triple, (2,2,2))
        else: #a=3 or 4
            return sub(triple, (3,0,0))
        #look through bs
        if b > c:
            return sub(triple, (0,3,0))
    #No reduction was found
    elif pre=="y":
        if a==1:
            return sub(triple, (1,1,1))
        elif a==4 and b<=1:
            return sub(triple, (1,1,1))
        elif a==4 and b==2:
            return (sub(triple,(3,0,0)), sub(("n",)+triple[1:], (2,0,0)))
    return triple

def fully_reduce(triple):
    old_triple = tuple()
    while old_triple != triple:
        old_triple = triple
        triple = take_down(triple)
    return triple

'''
#Generate all triples
for t in itertools.product(range(0,5), repeat=3):
    triple = ("n",) + t
    reduced_triple = fully_reduce(triple)
    reducer[triple] = reduced_triple
    if triple == reduced_triple:
        print(triple, "-> Same", reduced_triple)
    else:
        print(triple, "->", reduced_triple)

for t in itertools.product(range(0,5), repeat=3):
    triple = ("y",) + t
    reduced_triple = fully_reduce(triple)
    if triple == reduced_triple:
        print(triple, "-> Same", reduced_triple)
    else:
        print(triple, "->", reduced_triple)
'''


def simple_reduce(triple):
    #Test instances
    pre, t1, t2, t3 = triple
    if t1 == 0:
        return triple
    if t1 == 1:
        return sub(triple, (1,1,1))
    elif t1 == 2:
        new = sub(triple, (2,2,2))
    elif t1 == 3:
        new = sub(triple, (3,0,0))
    elif t1 == 4:
        new = sub(triple, (4,1,1))
    if pre == "n":
        return new
    #pre == "y"
    if t1 == 2:
        new = [new, sub(("n",t1,t2,t3), (2,0,0))]
    elif t1 == 3:
        new = [new, sub(("n",t1,t2,t3), (3,1,1))]
    elif t1 == 4:
        new = [new, sub(("n",t1,t2,t3), (4,2,2))]
    #Unpack the result
    new = [x for x in new if x]
    if not new:
        return False
    if len(new) == 1:
        return new[0]
    return new

reducer = {}
#Generate all triples
for t in itertools.product(range(0,5), repeat=3):
    for pre in ["n", "y"]:
        triple = (pre,) + t
        reduced_triple = simple_reduce(triple)
        reducer[triple] = reduced_triple
        if triple == reduced_triple:
            print(triple, "-> Same", reduced_triple)
        else:
            print(triple, "->", reduced_triple)
print(reducer)


expander = {}
for t in itertools.product(range(0,5), repeat = 2):
    for pre in ["n", "y"]:
        triple = (pre,0) + t
        expanded = {post: simple_reduce((pre,)+t+(post,)) for post in range(0,5)}
        if not any(expanded):
            expanded = False
        expander[triple] = expanded
        print(triple, "->", expanded)
print(expander)