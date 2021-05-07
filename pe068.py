#Solve project euler problem 68
#Date 20210503

#Define a gon = [...]

def sub_check(g,s,a,b,c):
    if g[a]==0 or g[b]==0 or g[c]==0:
        #may be a solution?
        return 2
    elif s == g[a] + g[b] + g[c]:
        #Solution confirmed
        return 1
    else:
        #No solution
        return 0

def gon_sum(g):
    return g[0] + g[1] + g[2]

def check(g):
    s = gon_sum(g)
    #print("s",s,"returns",sub_check(g,s,2,3,4),sub_check(g,s,3,5,6),sub_check(g,s,5,7,8),sub_check(g,s,1,7,9))
    ans = sub_check(g,s,2,3,4)*sub_check(g,s,3,5,6)*sub_check(g,s,5,7,8)*sub_check(g,s,1,7,9)
    return ans

def iterate(g,i,options):
    if check(g) == 0:
        return False
    if i == 10:
        return [tuple(g)]
    solns = []
    for j,val in enumerate(options):
        new_g = [x for x in g]
        new_g[i] = val
        new_options = options[:j] + options[j+1:]
        if i <= 0:
            print(i, val)
        new_solns = iterate(new_g, i+1, new_options)
        if new_solns == False:
            pass
        else:
            solns.extend(new_solns)
    if not solns:
        return False
    else:
        return solns

def stringify(g):
    triple_inds = [[0,1,2],[4,2,3],[6,3,5],[8,5,7],[9,7,1]]
    outer_inds = [x[0] for x in triple_inds]
    #find position of the smallest outer value in the outer_inds list
    outers = [g[i] for i in outer_inds]
    min_triple_ind = outers.index(min(outers))
    #create tripples
    triples = [[g[i] for i in trip] for trip in triple_inds]
    #re-arrange triples
    triples = triples[min_triple_ind:] + triples[:min_triple_ind]
    print(triples)
    s = "".join(["".join([str(y) for y in x]) for x in triples])
    return s

    

start = [0]*10
start[0] = 10
options = list(range(9,0,-1))

gons = iterate(start,1,options)
digits = [int(stringify(g)) for g in gons]
for g,d in zip(gons,digits):
    print("sum",gon_sum(g),"g",g,"str",d)

print("ans",max(digits))

    