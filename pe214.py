'''
PE214 Totient Chains
'''

import numpy as np
import math

def bruteEuler(n):
    E = 0
    for k in range(1,n+1):
        if math.gcd(k,n) == 1:
            E += 1
    return E

def bruteCheckChain(n):
    chainLength = 1
    N = n
    isPrime = False
    while n > 1:
        E = bruteEuler(n)
        if n == N and E == N - 1:
            isPrime = True
        n = E
        chainLength += 1
    return chainLength, isPrime

# print(bruteCheckChain(7))

N = 40*10**6
targetLength = 25

euler = np.full(N,1) #Calcualtion for euler(2028)
for primeFactor in range(2, N//2 + 1): #[2,2000]
    if euler[primeFactor] > 1:
        continue
    for power in range(2,int(math.log(N,primeFactor))+1): #2:[2,11] 3:[2:7] 13:[2,3]
        euler[primeFactor**power::primeFactor**power] *= primeFactor
    euler[primeFactor*2::primeFactor] *= primeFactor - 1
print("euler calculated")

chainLength = np.full(N,0)
chainLength[1] = 1
sumCorrectPrimes = 0
for n in range(2,N):
    if euler[n] == 1:
        #Indicates that this is a prime
        euler[n] = n - 1
        chainLength[n] = chainLength[n-1] + 1
        if chainLength[n] == targetLength:
            # checkLen, checkPrime = bruteCheckChain(n)
            # if checkPrime and checkLen == targetLength:
            #     print("correctly found", n)
            # else:
            #     print("INCORRECT", n, "chainLen", chainLength[n], "actualLen", checkLen, "isPrime", checkPrime)
            #     pass
            sumCorrectPrimes += n
    else:
        #Avoid recursion and just compute every possible answer
        chainLength[n] = chainLength[euler[n]] + 1
#print(euler)
#print(chainLength)
print("ans", sumCorrectPrimes)

exit()

checkSum = 0
for n in range(2,N):
    chainLength, isPrime = bruteCheckChain(n)
    if isPrime and chainLength == targetLength:
        checkSum += n
print("chk", checkSum)
#Incorrect 1633867589582
#          1677366278943
