'''
PE210
After drawing by hand, there appear to be some regions that create obtuse triangles:
    The region less than line(slope -1, origin O); excluding the line(slope 1, origin O)
    The region greater than line(slope -1, origin C); excluding the line(slope 1, origin C)
    The square between O and C; excluding the corners and excluding the line(slope1, origin O) 
Reminder that r does not need to be divisable by 4 and therefore the points do not always sit on the line defined above
Need an equation for a "diamond rectangle" on this plane

For the area that is "between the two points", seems like we need to develop a Diaphantine equation to find the number of points that have obtuse angles

'''
import math

'''
N(r) = 1 + 4*sum(i=0 to inf)(floor(r^2/(4i+1)) - floor(r^2/(4i+3)))
for 1 <= r <= 10^9: 

sum(i=1 to floor(r))(floor(sqrt(r^2 - i^2))
    sqrt(r^2 - i^2) > n
    i = sqrt(r^2 - n^2)
    Therefore, for a particular i, we can get the number of values for which the floor will be
        exactly the same
'''

def fullGridSearch(r, display=True):
    #For a particular radius r, search the entire grid for obtuse triangles
    #Make some sort of print function that will print out the grid, similart
    #to how we were doing this in excel before
    C = r/4
    lenOC = math.sqrt(2*(r/4)**2)
    grid = [[" "]*(2*r+1) for i in range(2*r+1)]
    def addToGrid(x,y,c):
        grid[-y+r][x+r] = c
    obtuseCount = 0
    for y in range(r, -r-1, -1):
        for x in range(-r, r+1):
            if x == 0 and y == 0:
                addToGrid(x,y,"@")
                continue
            if abs(x) + abs(y) > r: #Outside the manhattan radius allowed
                addToGrid(x,y,".")
                continue
            if x == y: #Colinear with our initial points (not obtuse)
                addToGrid(x,y,".")
                continue
            lenBO = math.sqrt(x**2 + y**2)
            lenBC = math.sqrt((x-C)**2 + (y-C)**2)
            sortedLengths = sorted([lenBO, lenBC, lenOC])
            if sortedLengths[2]**2 - 0.001 > sortedLengths[0]**2 + sortedLengths[1]**2:
                addToGrid(x,y,"#")
                obtuseCount += 1
            else:
                addToGrid(x,y,".")
    if display:
        for y in range(len(grid)):
            print(" ".join([g[0] for g in grid[y]]))
    print("Obtuse Count: ", obtuseCount, "for r: ", r)

def bruteGaussCentered(r):
    ##Only works for integer r
    count = 0
    r2 = r**2
    for i in range(1, int(r) + 1):
        count += int(math.sqrt(r2 - i**2))
    return 1 + 4*int(r) + 4*count

# def fastGaussCentered(r):
#     #use an alternate form of the equation that appears to be equivalent defined below
#     count = 0
#     for j in range(0, int(r)):
#         count += int(math.sqrt(2*r*j - j**2))
#     return 1 + 4*int(r) + 4*count

def gaussSpecific(r):
    #Where the input r in the r of the entire problem
    count = 0
    R = int(r//4/math.sqrt(2))
    R2 = r**2//32
    for i in range(1, R + 1):
        diff = R2 - i**2
        sqrt = math.isqrt(diff)
        count += sqrt
        #Need to remove points where the sqrt is exact
        count -= (sqrt**2 == diff)
    return 1 + 4*R + 4*count

r = 10**9

# fullGridSearch(r,False)
southwestCount = r**2
northwestCount = r**2//2
gaussCount = gaussSpecific(r)
diagonal = r//4 - 1
ans = southwestCount + northwestCount + gaussCount - diagonal
print("ans: ", ans)
pass

# r= 10**9//4/math.sqrt(2)
# print(int(r**2))
# ir = int(r)
# fr = r - ir
# print(ir**2 + int(2*ir*fr + fr**2))

'''
sqrt(r**2 - i**2) for i in range [1, r]
let i = (r - j) for a j in range [r-1, 0] yields i [1, r]
sqrt(r**2 - (r-j)**2)
sqrt(r**2 - (r**2 - 2rj + j**2))
sqrt(2rj - j**2)
sqrt(j(2r - j))
sqrt(j)*sqrt(2r-j) --- is this computationally less expensive in some way?
sqrt(j)*[sqrt(2r-1)+sqrt(2r-2)+...+sqrt(2r-r)]
'''