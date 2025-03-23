import math
low = math.sqrt(1020304050607080900)
high = math.sqrt(1929394959697989990)
low, high = int(low), int(high)
low = low - low%10
print(low, high)


perfection = "1_2_3_4_5_6_7_8_9_0"
#Interate through 1 digit numbers, finding those numbers where the final 1 digit match perfection after squaring
#Then take those 1 digit numbes and add two more digits to the front
#Iterate through 3 didit numbers, finding those numbers where the final 3 digits match perfection after squaring
#Continue this pattern until perection is found on the squared number

def countDigitsMatched(nString):
    for matchedDigits in range(0,10,1):
        if len(nString) < 2*matchedDigits + 1:
            return matchedDigits - 1
        if nString[-2*matchedDigits-1] != perfection[-2*matchedDigits-1]:
            return matchedDigits
    return 10

previousSolutions = ["0"]
for q in range(10):
    print(previousSolutions)
    newSolutions = []
    for pString in previousSolutions:
        for i in range(0,100):
            iString = f"{i:02}"
            newNString = iString + pString
            newMString = str(int(newNString)**2)
            digitsMatched = countDigitsMatched(newMString)
            if digitsMatched == 10:
                print("ans", newNString, int(newNString)**2)
                exit()
            elif countDigitsMatched(newMString) < len(newNString)/2:
                continue
            else:
                newSolutions.append(newNString)
    previousSolutions = newSolutions


    
print(countDigitsMatched("2020304050607080901"))



