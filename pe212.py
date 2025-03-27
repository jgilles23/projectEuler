'''
PE212 combined volume of cuboids
We are working with the UNION not the intersection
How do we deal with the union of optentailly muliple overlapping cuboids?
Count the full area of cuboid #1, how do we do this overlapping thing?
    I do feel like I have solved this problem before
Maybe we make some sort of graph of each cuboid & sub cuboids that might be shared
    A sub cuboid is a cuboid; that needs to be subtracted from the main cuboid
    then added to the list of cuhboids that need to be analyized
Step down through levels where we alternate between adding area and subtracting area
Need to write a formula for the intersection of cuboids
    For an intersection to occur, we must have an intersection in x, y, and z
    xA, dA, xB, dB as an example
    let xMin, xMax = sort(xA, xB) and associated dMin, dMax
    There is overlap xMax <= xMin + dMin
    let dOverlap = min(dMin - (xMax - xMin), dMax)
Scenarios:
    xA <= xB
        (xA+dA < )
'''
import time

N = 50000

#Generate S, lagged fibonacci generator
generator = [0]*(6*N + 1)
for k in range(1, 56):
    generator[k] = (100003 - 200003*k + 300007*k**3) % 1000000
for k in range(56, 6*N + 1):
    generator[k] = (generator[k-24] + generator[k-55]) % 1000000

def getParameters(n):
    #Get the parameters for the nth cuboid
    X = (generator[6*n-5]%10000, 1+(generator[6*n-2]%399))
    Y = (generator[6*n-4]%10000, 1+(generator[6*n-1]%399))
    Z = (generator[6*n-3]%10000, 1+(generator[6*n]%399))
    return [X,Y,Z]

def singleAxisIntersection(A, B):
    #Return False if there is no intersection, otherwise return the overlap
    xA, dA = A
    xB, dB = B
    if xA <= xB:
        if xA + dA <= xB:
            return False
        else:
            if xB + dB <= xA + dA:
                return (xB, dB)
            else:
                return (xB, xA + dA - xB)
    else:
        if xB + dB <= xA:
            return False
        else:
            if xA + dA <= xB + dB:
                return (xA, dA)
            else:
                return (xA, xB + dB - xA)

def testSingleAxisIntersection(A, B, result, printFlag = False):
    r = singleAxisIntersection(A,B)
    if r == result:
        s = "PASS"
    else:
        s = "FAIL"
    if s == "FAIL" or printFlag == True:
        print(s, "A", A, "B", B, "result", r, "expected", result)

#B far right
testSingleAxisIntersection((10,10), (25,20), False)
testSingleAxisIntersection((10,10), (20,20), False)
testSingleAxisIntersection((10,10), (15,20), (15,5))
testSingleAxisIntersection((10,10), (10,20), (10,10))
testSingleAxisIntersection((10,10), (5,20), (10,10))
#B at right end
testSingleAxisIntersection((10,10), (15,5), (15,5))
testSingleAxisIntersection((10,10), (10,10), (10,10))
testSingleAxisIntersection((10,10), (5,15), (10,10))
#B in middle
testSingleAxisIntersection((10,10), (12,3), (12,3))
testSingleAxisIntersection((10,10), (10,5), (10,5))
testSingleAxisIntersection((10,10), (5,10), (10,5))
#B at left end
testSingleAxisIntersection((10,10), (5,5), False)
#B left of left end
testSingleAxisIntersection((10,10), (5,2), False)
#Completed tests
print("Completed single axis tests")

def intersection(cuboidA, cuboidB):
    #Find the intesection of cuboidA and cuboidB
    #Cuboid in the form of ((x, dx), (y, dy), (z, dz))
    #IF there is no intersection, return False
    intersectingCuboid = []
    for i in range(3):
        C = singleAxisIntersection(cuboidA[i], cuboidB[i])
        if C == False:
            return False
        intersectingCuboid.append(C)
    return intersectingCuboid

def volume(cuboid):
    #Get the volume of a cuboid
    return cuboid[0][1] * cuboid[1][1] * cuboid[2][1]

start = time.time()

def recursiveUnion(collection, start = 0):
    #Find the volumne of the union of the collection recursively
    if len(collection) == 1:
        #If this is the 
        return volume(collection[0])
    V = 0
    for i in range(len(collection)):
        V += volume(collection[i])
        subCuboids = []
        for j in range(i+1, len(collection)):
            intersectingCuboid = intersection(collection[i], collection[j])
            if intersectingCuboid != False:
                subCuboids.append(intersectingCuboid)
        if len(subCuboids) > 0:
            deductiveVolume = recursiveUnion(subCuboids)
            V -= deductiveVolume
        if start > 0:
            if time.time() - start > 10:
                print(i)
                start = time.time()
    return V


collection = [getParameters(n) for n in range(1, N+1)]
ans = recursiveUnion(collection, True)
print("ans", ans)

#print(recursiveUnion([[(10,10),(10,10),(10,10)], [(15,10),(15,10),(15,10)]]))
