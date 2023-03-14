f0_left = 1
f0_right = 1
f1_left = 1
f1_right = 1

def is_pandigital(s):
    if len(s) != 9:
        return False
    for d in "123456789":
        if not d in s:
            return False
    return True

for i in range(3,1000000):
    #Least significant digits
    f2_right = (f0_right + f1_right)%10**9
    f0_right = f1_right
    f1_right = f2_right
    #Most significant digits
    f2_left = (f0_left + f1_left)
    if f2_left >= 10**17:
        f0_left = f1_left//10
        f1_left = f2_left//10
    else:
        f0_left = f1_left
        f1_left = f2_left
    #Determine if pandigital
    pd_count = 0
    if is_pandigital(str(f1_right)):
        pd_count += 1
        print(i,":",str(f1_left)[:9], str(f1_left)[9:], "...", f1_right, "Right")
    if is_pandigital(str(f1_left)[:9]):
        pd_count += 1
        print(i,":",str(f1_left)[:9], str(f1_left)[9:], "...", f1_right, "Left")
    if pd_count >= 2:
        print(i,";","BOTH")
        exit()