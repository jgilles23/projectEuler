"""
Looking for binary truth tables T that satisft an odd relationship
Oh, I did not understand. There are 2^(2^6) or 64 truth tables to deal with, thats a lot more, we we need to be smarter about this

T(a,b,c,d,f,e) AND T(b,c,d,e,f, a XOR(b AND c)) == 0
    we are combining two rows of the truth table here and saying that one but not both of the rows of said table can be 1
    Each position in the truth table links to one other position in the table; unclear if the mapping is one to one bidirectional or not; I would guess it is not bi-directional


"""
import numpy as np

def secondTableInput(firstTableInput):
    a,b,c,d,e,f = [firstTableInput>>i&1 for i in range(5,-1,-1)]
    R = b<<5 | c<<4 | d<<3 | e<<2 | f<<1 | (a ^ (b & c))
    return R

mapping = [-1]*64
for i in range(64):
    j = secondTableInput(i)
    # print(i, ":", secondTableInput(i))
    mapping[i] = j
# print(mapping)

loops = []
visited = [0]*64
for currentLoc in range(64):
    newLoop = [currentLoc]
    nextLoc = mapping[currentLoc]
    while visited[nextLoc] != 1:
        visited[currentLoc] = 1
        currentLoc = nextLoc
        newLoop += [currentLoc]
        nextLoc = mapping[currentLoc]
    if len(newLoop) > 1:
        loops.append(newLoop + [nextLoc])

for i, loop in enumerate(loops):
    print(i, ":", loop)

"""
There is exactly one to one mapping from firstinput to second input, meaning there are 32 pairs of inputs
Within each pair of inputs T can be true for one, the other, neither, but not both; 3 out of the 4 possibilities for each pair yields a possible table
And all of them have to work at the same time
Oh wait, we are going to be creating loops of numbers

Ok, now that we have the loops established, what we know is that no two adjacent locations on the loop can both be True, otherwise the AND statement would be true
We can likely establish that a length of "chain" can only have so many permutations without repeating, here are some sample chains
    1 > (0)
    0 > (1 or 0)
    (in fact every chain is made by adding these two parts together)
"""

cache = {}
def chainPermutations(previousLink, remainingLinks):
    #In order to force the chain to end in 0, set the remaining length to be one less than planned
    inputHash = str(previousLink) + ":" + str(remainingLinks)
    if inputHash in cache:
        return cache[inputHash]
    if remainingLinks == 0:
        return 1
    if previousLink == 1:
        permutationCount = chainPermutations(0, remainingLinks - 1)
    else: #previouLink == 0
        permutationCount = chainPermutations(0, remainingLinks - 1) + chainPermutations(1, remainingLinks - 1)
    cache[inputHash] = permutationCount
    return permutationCount
    



x = 64 #chain length
p = chainPermutations(0, x - 1) + chainPermutations(1, x - 1)
print(p)

loopTypes = [""]*len(loops)
loopLengths = [0]*len(loops)
loop0Permutations = [0]*len(loops)
loop1Permutations = [0]*len(loops)
loop0Multiplier = [0]*len(loops)
loop1Multiplier = [0]*len(loops)

#Individually assemble all of the permutations
i = 0
loopTypes[i] = "LOOP"
loopLengths[i] = 1
loop0Permutations[i] = chainPermutations(0, 0)
loop1Permutations[i] = 0
for i in [1, 2, 3, 4, 8]:
    loopTypes[i] = "LOOP"
    loopLengths[i] = len(loops[i]) - 1
    loop0Permutations[i] = chainPermutations(0, loopLengths[i] - 1)
    loop1Permutations[i] = chainPermutations(1, loopLengths[i] - 2)
#Add strands to the loops
for i, connectedLoop in [(5,1), (6,3), (7,4), (9,2)]: #X strand connects to Y loop
    loopTypes[i] = "STRAND"+str(connectedLoop)
    loopLengths[i] = len(loops[i])
    loop0Permutations[i] = chainPermutations(0, loopLengths[i] - 1)
    loop0Multiplier[connectedLoop] = loop0Permutations[i]
    loop1Permutations[i] = chainPermutations(1, loopLengths[i] - 1)
    loop1Multiplier[connectedLoop] = loop1Permutations[i]
#Still count the loops that do not have connected strands
for i in [0, 8]:
    loop0Multiplier[i] = 1
    loop1Multiplier[i] = 1



for i, loop, type, length, p0, p1, m0, m1 in zip(range(len(loops)), loops, loopTypes, loopLengths, loop0Permutations, loop1Permutations, loop0Multiplier, loop1Multiplier):
    print(f"{i} : {type}; len:{length}; {p0}*{m0} + {p1}*{m1} = {p0*m0 + p1*m1}; {str(loop).replace(" ","")}")

'''
A test for loop length 6 = 18 permutations; with (strand of length 3)
000000 (00 01 10)
000001 (00 01 10)
000010 (00 01 10)
000100 (00 01 10)
000101 (00 01 10)
001000 (00 01 10)
001001 (00 01 10)
001010 (00 01 10)
010000 (00 01 10)
010001 (00 01 10)
010010 (00 01 10)
010100 (00 01 10)
010101 (00 01 10)
100000 (00 01)
100010 (00 01)
100100 (00 01)
101000 (00 01)
101010 (00 01)
----
With strand length we get 13*3 + 5*2 = 49
'''

#claculate the answer
ans = 1
for p0, p1, m0, m1 in zip(loop0Permutations, loop1Permutations, loop0Multiplier, loop1Multiplier):
    x = p0*m0 + p1*m1
    if x > 0:
        ans = ans*x
print("ans", ans) 
#This is somehow the wrong answer, let's try again!

print()
print()

'''
This time we are going to take a more systematic approach to the task where we are not hard coding any of the outputs
For each instance that appears in the grid, we the left side as the child and the right side as the parent
For parents with "-1" states, we assume the states are 1, but we mark that it has a child
What we really need ot do is make the map, then hop around the map
Maybe arbitrarily choose one wat to go at each instance --- that doesn't really make a ton of sense
I need a cleaner algorythm to solve this problem
Some sort of network identification algorythm that I can then apply permutations to
Steps:
    Visited = -1
    Self = (1,1)
The problem was that my strand creation algorythm was not correct, There are no strands and we were doing wayyyy more work than required
'''

def fromLeftGetRight(left):
    a = (left>>5)&1
    b = (left>>4)&1
    c = (left>>3)&1
    right = (left<<1)&63 | (a ^ (b & c))
    return right

leftToLoopNumber = [100]*64

for _ in range(64): #Very inefficient way to do this, but easy to code!
    for left in range(64):
        right = fromLeftGetRight(left)
        if leftToLoopNumber[right] < left:
            leftToLoopNumber[left] = leftToLoopNumber[right]
        else:
            leftToLoopNumber[left] = left

loopLengths = [0]*64
for i in range(64):
    loopLengths[leftToLoopNumber[i]] += 1
loopLengths = [x for x in loopLengths if x > 0]

permutations = 1
for length in loopLengths:
    if length == 1:
        subPermutations = 1
    else:
        subPermutations = chainPermutations(0, length - 1) + chainPermutations(1, length - 2)
    permutations *= subPermutations
    print(length, ":", subPermutations)
print("ans", permutations)

'''
exit()

leftTable = np.array([[n>>(5-i)&1 for i in range(6)] for n in range(64)], bool)

for T in range(64):
    rightTable = [T>>(6-i) for i in range(5)]

exit()


#Table stored in binary format as [A, B, C, D, E, F]: T, where each capital letter represents a binary number of all of the stats of the table 
leftTable = [
    int(("0"*32 + "1"*32)*1,2),
    int(("0"*16 + "1"*16)*2,2),
    int(("0"*8 + "1"*8)*4,2),
    int(("0"*4 + "1"*4)*8,2),
    int(("0"*2 + "1"*2)*16,2),
    int(("0"*1 + "1"*1)*32,2)
]

leftTable = [0]*6
for row in range(64):
    for i in range(6):
        leftTable[i] = leftTable[i] 

def lookupT(A,B,C,D,E,F,T):
    combinedResult = 0
    for i in range(64):
        indexT = (A>>i)&1<<5 | (B>>i)&1<<4 | (C>>i)&1<<3 | (D>>i)&1<<2 | (E>>i)&1<<1 | (F>>i)&1
        print(indexT)
        resultT = (T>>indexT & 1) << i
        combinedResult = combinedResult | resultT
    return combinedResult


result = lookupT(*leftTable, 456785899998763)
print(result)





print(leftTable)

print(format(7, '064b'))
'''