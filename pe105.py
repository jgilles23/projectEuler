import math

lines = []
with open("p105_sets.txt") as file:
    for line in file:
        lines.append(list(int(x) for x in line[:-1].split(",")))

s = 0

for A in lines:
    special = True
    #Check for sum clashes
    b = 0b1
    for d in A:
        c = b << d
        if (b & c) != 0:
            special = False
            break
        b = b ^ c
    #Check for length clashes
    B = sorted(A)
    for i in range(1, int(math.ceil(len(B)/2))):
        if sum(B[:i+1]) < sum(B[-i:]):
            special = False
            break
    #If sum is still special
    if special == True:
        s += sum(A)

print("ans", s)
