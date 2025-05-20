'''
pe215 Crack free walls
Esentially get a list of cracks in binary format, compare to other levels and build a wall of allowable cracks
There should be on the order of 2^16 crack position options
 |-| or             |--|
>|-|-| or |--|-| or |-|--| or |--|--|
 *
 L0
>10* or             100*
 L2                 L3
>1010* or 10010* or 10100* or 100100*
 L4       L5        L5        L6
'''
import numpy as np

def computeCrackOptions(currentLength=0, targetLength=0, currentCrackPattern=0):
    withTwoBrick = 2<<(currentLength + 1) |currentCrackPattern
    withThreeBrick = 4<<(currentLength + 1) | currentCrackPattern
    if targetLength - currentLength <= 1:
        return [] #No possible patterns, we shouldn't get here
    elif targetLength - currentLength == 2:
        return [currentCrackPattern] #0Existing
    elif targetLength - currentLength == 3:
        return [currentCrackPattern] #00Existing
    else:
        return computeCrackOptions(currentLength+2, targetLength, withTwoBrick) + computeCrackOptions(currentLength+3, targetLength, withThreeBrick)

def wallString(n, W):
    return "|"+('{0:0'+str(W)+'b}').format(n)[:-1]+"|"

W = 32
H = 10
options = computeCrackOptions(targetLength=W)

rowOptions = np.array(options)
print("rowOptions", rowOptions.size)
nextLayerOptions = []
for i, n in enumerate(rowOptions):
    nextLayerOptions.append(np.arange(rowOptions.shape[0])[(rowOptions & n) == 0])

# for i, option in enumerate(options):
#     print(wallString(option, W), option, "index", i, "compatable", nextLayerOptions[i])

#Now build the wall out of the layers
currentLayerCounts = np.full_like(rowOptions, 1, int)
# print(currentLayerCounts)
for layer in range(1, H):
    nextLayerCounts = np.full_like(rowOptions, 0, int)
    for i in range(len(currentLayerCounts)):
        for nextLayer in nextLayerOptions[i]:
            nextLayerCounts[nextLayer] += currentLayerCounts[i]
    # print(nextLayerCounts)
    currentLayerCounts = nextLayerCounts

ans = np.sum(currentLayerCounts)
print("ans", ans)