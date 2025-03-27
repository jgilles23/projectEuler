'''
Project Euler 213 -- Flea Circus
Start by trying this problem on a 3x1 grid
    1: 1 1 1
    2: 1 2 0; 0 2 1
    3: 2 1 0; 1 1 1; 1 1 1; 0 1 2 | 2 1 0; 1 1 1; 1 1 1; 0 1 2
    4: equivelent to (2)
    Try with fractions:
    1: 1 1 1     P(0)=0.5; P(1)=0; P(2)-0.5' sum=1
    2: 0.5 2 0.5 P(0)=0.25; P(1)=0; P(1)=0.25
    3: equivelent to (1)
Now lets try this problem with a 4x1 grid; when indexed from 0: A is even, B is odd
    1: 1A 1B 1A 1B > (A 1 1), B 1 1; Solve only for A, B will be the same as A and can be directly permutated together
    2: B: 2 0; 1 1
    3: A: 2 0; 1 1; 1 1; 0 2 | 0 2; 1 1
    4: B: 2 0 | 2 0; 1 1 | 2 0; 1 1 |  
Notes
    I think is actually subscriptable into two problems; the even cells and the odd cells
    The evens and the odds actaully can't mix since the markers cannot stay in the same place
    Maybe there is a way to interleave the evens and the odds so that the problem is further subscriptable
    Actaully two 
Maybe we can build this up on a cell by cell basis
    Important metrics:
        1) The total number of ticks contained within the structure
        2) The (permutations and probablities) of the leading edge
        3) THe average number of unoccupied cells for each of those permutations
        Build some sort of interwoven network which each leading edge has the listed properties and each leading edge is linked to the previous leading edge by it's probabilites?
        Now how do we build this graph?
    Attempt:
        A[1, 1:1] B[2, 1:1] C[3, 1:1]
        A[1, 1:1 0:] [1, 1: 0: ] [2, 1: 0:]
    Attempt: (total, leading edge)count
        A: (1,1)1; B: (2,1)1; C: (3,1)1
        A: (2,2)1 (1,1)1; B: (3,2)1 (2,1)1 (3,1)1 (2,0)1; C: (3,1)1 (3,0)1
    Attempt: (total, leading edge)count
        A: (1,1)1; B: (2,1)1; C: (3,1)1
        O: (0,0)1; A: (1,1)1 B: 
Ok, let's try this in a different way; surely the cells where a single tick ends up are independent; so the probability that a tick doesn't end up in multiple cells is the 

Run singleTickDistribution for each tick, then need to check the probabilities that NONE of the ticks will be in certian sets of squares

P(0 empty) = product(P(0 empty for all ticks))
P(1 empty) = product(P(1 empty for all ticks))
P(0 & 1 empty) = P(0 empty)*P(1 empty)
P(0 empty, 1 not empty) = P(0 empty)*(1 - P(1 empty))
P(1 empty, 0 not empty) = P(1 empty)*(1 - P(0 empty))
P(0 & 1 not empty) = 1 - P(0 & 1 empty) - P(0 empty, 1 not empty) - P(1 empty, 0 not empty)
    P(0 xor 1 empty) = P(0 empty) + P(1 empty) - 2*P(0 empty)*P(1 empty)

Now for (3)
    P(0E,1E,2E) = P(0E)*P(1E)*P(2E)
    P(0E,1E,2N) = P(0E)*P(1E)*P(2N) = P(0E)*P(1E)*(1-P(2E)) = P(0E)*P(1E) - P(0E)*P(1E)*P(2E)
    P(0E,1N,2E) = P(0E)*P(1N)*P(2E) = P(0E)*P(1-P(1E))*P(2E) = P(0E)*P(2E) - P(2E)*P(1E)*P(2E)
    P(0N,1E,2E) = P(0N)*P(1E)*P(2E) = (1-P(0E))*P(1E)*P(2E) = P(1E)*P(2E) - P(0E)*P(1E)*P(2E)
    P(sum 1) = sum[P(XE) choose 2 of 3] - 3*P(0E)*P(1E)*P(2E)
    P(0E,1N,2N) = P(0E)*P(1N)*P(2N)
    P(0N,1E,2N) = P(0N)*P(1E)*P(2N)
    P(0N,1N,2E) = P(0N)*P(1N)*P(2E)
    P(0N,1N,2N) = P(0N)*P(1N)*P(2N)

So we can quite easily independently calculate the probability that any individual cell is empty.
But what about combinatiosn of cells?
P(all the cells are empty) SHOULD = 0; but in this system that I am thinking about, that would not be true
    We actually need to do the sums for each individual tick, then do the multiplications for each case?
        Maybe we can limit by the number of decimal points of percision requested
    Big multiplication + Big multiplication + Big multiplication + ...
    Big multipication = P(condition on 0)*P(condition on 1)*P(condition on 2)*...
    p(Condition on 0) = sum
    P(condition on X) = Up to like 450 things this will get pretty crazy

P0E and P1E = P0E + P1E - P0E*P(1E | 0E)
    = (1-P0F) + (1-P1F) - (1-P0F)*(1 - P1F/(1-P0F))
    = (1-P0F) + (1-P1F) - (1-P0F) + (1-P0F)*P1F/(1-P0F)
    = 1 - P1F + P1F
    P(1F | 0E) = P1F/(1-P0F)
    P(1E | 0E) = 1 - P1F/(1-P0F)
'''

import numpy as np

def singleTickDistribution(gridSize, startingPosition, bellCount):
    #Get the final probability distribution of a single tick after the bellCount
    grid = np.zeros(gridSize, float)
    grid[startingPosition] = 1
    #Division grid for how the parts are distributed
    divisionGrid = np.full_like(grid, 4, float)
    divisionGrid[0,:] -= 1
    divisionGrid[-1,:] -= 1
    divisionGrid[:,0] -= 1
    divisionGrid[:,-1] -= 1
    for i in range(bellCount):
        newGrid = np.zeros_like(grid, float)
        newGrid[1:,:] += grid[0:-1,:]/divisionGrid[0:-1,:]
        newGrid[0:-1,:] += grid[1:,:]/divisionGrid[1:,:]
        newGrid[:,1:] += grid[:,0:-1]/divisionGrid[:,0:-1]
        newGrid[:,0:-1] += grid[:,1:]/divisionGrid[:,1:]
        grid = newGrid
    # print(grid)
    return grid

gridSize = (30,30)
bellCount = 50

inverseGrids = []
for x in range(gridSize[0]):
    for y in range(gridSize[1]):
        newGrid = singleTickDistribution(gridSize, (x,y), bellCount)
        inverseGrids.append(1 - newGrid)

averageFilledSquares = 0
for i in range(len(inverseGrids)):
    if i%10==0: print(i)
    product = 1 - inverseGrids[i]
    for j in range(i+1, len(inverseGrids)):
        product = product*inverseGrids[j]
    averageFilledSquares += np.sum(product)

print("averageFilledSquares", averageFilledSquares)
ans = gridSize[0]*gridSize[1] - averageFilledSquares
print("full ans", ans)
print("     ans", round(ans, 6))





# def bruteForce(startGrid, bellCount, position=(0,0), optionToExplore=0, newGrid = None):
#     shape = startGrid.shape
#     if position == shape and optionToExplore == 4:
#         #One iteration of the grid has been traversed
#         startGrid = newGrid
#         bellCount -= 1
#         position = (0,0)
#         newGrid = None
#         if bellCount == 0:
#             return 1
#     count = 0
#     if newGrid is None:
#         newGrid = np.full(shape, 0)
#     if optionToExplore == 0 and position[0] - 1 > 0:
#         count += bruteForce(startGrid, )

