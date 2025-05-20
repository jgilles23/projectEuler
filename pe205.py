'''
PE205 - Dice Game
'''

def addDiceToDistribution(distribution, faces):
    newDistribution = [0]*(len(distribution) + faces)
    for i in range(len(distribution)):
        for j in range(1,faces+1):
            newDistribution[i + j] += distribution[i]
    return newDistribution

def fullDistribution(numDice, numFaces):
    distribution = [1]
    for _ in range(numDice):
        distribution = addDiceToDistribution(distribution, numFaces)
    return distribution

def probabiliyABeatsB(ADistribution, BDistribution):
    winCount = 0
    totalCount = 0
    BTotal = sum(BDistribution)
    for i in range(len(ADistribution)):
        for j in range(min(i, len(BDistribution))):
            winCount += ADistribution[i] * BDistribution[j]
        totalCount += ADistribution[i] * BTotal
        pass
    return winCount / totalCount

PeterDistribution = fullDistribution(9,4)
ColinDistribution = fullDistribution(6,6)
print(PeterDistribution)
print(ColinDistribution)
ans = probabiliyABeatsB(PeterDistribution, ColinDistribution)
print("full ans", ans)
print("ans rounded to 7 decimal places", round(ans, 7))
#0.0001620 Incorrect