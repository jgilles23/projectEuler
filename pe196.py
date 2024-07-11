#PE196
import sympy
import sympy.ntheory

def rowStartEnd(r):
    #Get the start and end integers of row r
    end = (r + 1)*r//2
    start = end - r + 1
    return start,end

def primeCheck(N, r):
    if sympy.ntheory.primetest.isprime(N):
        return [(N, r)]
    else:
        return []

def getPrimeNeighbors(n, r):
    rowStart, rowEnd = rowStartEnd(r)
    primeNeighbors = []
    #Check all 8 numbers
    #Positions
    #n-r        n-r+1       n-r+2
    #n-1        n           n+1
    #n+r-1      n+r         n+r+1
    if n != rowStart:
        #left column
        primeNeighbors += primeCheck(n-r, r-1)#top left
        # primeNeighbors += primeCheck(n-1, r)#middle left
        primeNeighbors += primeCheck(n+r-1, r+1)#bottom left
    if n < rowEnd - 1:
        #top right
        primeNeighbors += primeCheck(n-r+2, r-1)#top right
    if n != rowEnd:
        #top center AND right middle
        primeNeighbors += primeCheck(n-r+1, r-1)#top middle
        # primeNeighbors += primeCheck(n+1, r)#middle right
    #remaining
    primeNeighbors += primeCheck(n+r, r+1)#bottom middle
    primeNeighbors += primeCheck(n+r+1, r+1)#bottom right
    return primeNeighbors

def isTriplet(n, r):
    primeNeighbors = getPrimeNeighbors(n, r)
    if len(primeNeighbors) >= 2:
        return True
    elif len(primeNeighbors) == 1:
        return len(getPrimeNeighbors(*primeNeighbors[0])) >= 2
    else:
        return False


# R = 8
# previousRowStart, _ = rowStartEnd(R-1)
# thisRowStart, thisRowEnd = rowStartEnd(R)
# _, nextRowEnd = rowStartEnd(R+1)
# primesInRange = list(sympy.primerange(previousRowStart, nextRowEnd + 1))
# primesInRangeSet = set(primesInRange)
# print(primesInRange)

def getRowSum(R):
    rowSum = 0
    thisRowStart, thisRowEnd = rowStartEnd(R)
    print("range:", thisRowStart, thisRowEnd)
    for prime in sympy.primerange(thisRowStart, thisRowEnd + 1):
        if isTriplet(prime, R):
            # print(prime)
            rowSum += prime
    print("SUM:", rowSum)
    return rowSum

ans = getRowSum(5678027) + getRowSum(7208785)
print("ans", ans)
