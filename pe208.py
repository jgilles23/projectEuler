
"""
So, it seems like we will need a coordinate system for the traverse out and then the traverse back 
THe traverse out of 35 steps yields about 35 trillion results, so this will need to be further reduced
Each positon on the grid is defined a offset from the starting point and a direction

I need to develop an equivelence rule for this particular geometry: e.g. null = LLLLL
I wonder if moves can be reduced suc that they can be performed in any order; e.g. L = RRRLRR?
    The pervious line does not work because whre the left is taken will influnce where you end up
But... an equivlent hypothesis may state that there are only 5 moves on the board, and each of those moves has 10 directions
    So the moves could be reduced to A B C D E and thier negatives -A -B -C -D -E
    With the following geometry rules, A+B+C+D+E = 0; -A + A = 0; and equivelents
    The eaample puzzle could be translated into:
        A A A B C C B A E E E D D D D E A B B B C C C D E
        = 0; simplifies to null because the loop is closed
    There are basically two polarities to each letter that determines what the next letter can be
        So in the clockwise (or positive polarity) The cycle goes +A>+B>+C>+D>+E
        In the counterclockwise (or negative polarity) The Cycle goes -E>-D>-C>-B>-A
    On each move, the cycle can eather continue with the next letter in the cycle (eg +A > +B) or it can flip polarity (eg +A > -A)
    So this would be the claddification in polarity of the initial loop: +A –A +A +B +C –C –B –A –E +E – E –D +D –D +D +E +A +B –B +B +C –C +C +D +E
        There are 3 positive copies of each letter and 3 negative copies --- that probably means something
        Hypothesis: in order to form a complete loop, you much have full positive & full negitive sets. E.g. +A does not cancel -A; they are different!
More strongly stated:
    There are two squences: positive +A>+B>+C>+D>+E and negative -E>-D>-C>-B>-A
    Each move either goes to the next item in it's sequence or fllips sign
    Let a "ring" be a complete set of either positive or negative moves
    All complete loops must consist of only complete rings with the moves in any order across all rings
    The starting move can either be +A or -E; the other solutions do not work because they would not be facing North
We can probably assume in some manner that each of those starting moves is symmetric in some way
QUESTION: is it possible to return to the starting position, but NOT be facting North? If that is possible, this is a much harder problem, so let's hope not
Trial:
    For similicity assume we always start with +A, then we will multiply the result at the end by 2
    We subdivide the total number of moves into "rings" of 5 moves each.
    For a 10 move solution, our options are 2+; or 1+ and 1-
        The 2+ situation is simple, there is only 1 option
        the 1+ 1- situation is more complex, after +A each move can be one of two things with some limits
            Since we need at least some negative, we need at least 2 transitions and those two transitions must subdivide the chain into equal lengths of each sign
        Since each transition is either positive or negative, simply assign the negatives wherever we wish & the rest subdivides cleanly
        In this scenario there acutally must be exactly two of each letter; so that makes things a lot harder to count I think
"""

positiveLoop = [0,1,2,3,4]
negativeLoop = [5,6,7,8,9]

letterMapping = ["+A", "+B", "+C", "+D", "+E", "-A", "-B", "-C", "-D", "-E"]

mapping = {}
for i in range(5):
    mapping[positiveLoop[i]] = [positiveLoop[(i+1)%5], negativeLoop[i]]
    mapping[negativeLoop[i]] = [negativeLoop[(i-1)%5], positiveLoop[i]]
print(mapping)

#Implement a cache/map of the found positions
cache = {}
def recursiveSearch(previousMove, targetTable):
    #Define in a table how many of each move should be in the solution, counts down
    #Returns the number of ways to achieve the target table
    #Check if a solution has been found
    if sum(targetTable) == 0:
        #For the solution to be valid +A(0) must be in the list of next possible moves
        if 0 in mapping[previousMove]:
            return 1 #Found a valid solution
    #setup a cache for faster returns
    hashedInputs = str(previousMove) + ":" + str(targetTable)
    if hashedInputs in cache:
        return cache[hashedInputs]
    #If a cached copy of the solution is not found perform a recursive search
    solutionsCount = 0
    for newMove in mapping[previousMove]:
        if targetTable[newMove] >= 1:
            newTargetTable = targetTable[:]
            newTargetTable[newMove] -= 1
            solutionsCount += recursiveSearch(newMove, newTargetTable)
    #Update the cache
    cache[hashedInputs] = solutionsCount
    return solutionsCount


totalMoves = 70
solutionsCount = 0
for positiveLoops in range(1, totalMoves//5 + 1):
    negativeLoops = totalMoves//5 - positiveLoops
    targetTable = [positiveLoops]*5 + [negativeLoops]*5
    targetTable[0] -= 1 #Assume starting with an +A(0) move
    solutionsCount += recursiveSearch(0, targetTable)
#Multiply by 2 to account for the alternate starting arrangement
solutionsCount = 2* solutionsCount
print("solutions", solutionsCount)



