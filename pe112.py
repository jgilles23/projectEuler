bouncy_count_by_tens = [0]*10
#If the previous digit is i, the bouncy count is bouncy_count_by_100[i]

n = 2
n_parts = [2]

count_nonbouncy = 1
count_bouncy = 0

while n < 1000: #count_bouncy / (count_bouncy + count_nonbouncy) != 0.9900000:
    if n % 1024 == 0:
        print(n, count_bouncy / (count_bouncy + count_nonbouncy))
    #Check for increasing
    increacing = False
    i0 = n_parts[0]
    for i1 in n_parts[1:]:
        if i1 < i0:
            break
        i0 = i1
    else:
        #Is increasing
        increacing = True
    #Check for decreasing
    decreasing = False
    i0 = n_parts[0]
    for i1 in n_parts[1:]:
        if i1 > i0:
            break
        i0 = i1
    else:
        #Is decreasing
        decreasing = True
    #Count
    print(n, n_parts, increacing, decreasing)
    if increacing or decreasing:
        count_nonbouncy += 1
    else:
         count_bouncy += 1
    #Next number 
    n += 1
    carry = 1
    for i in range(len(n_parts)-1,-1,-1):
        n_parts[i] += carry
        if n_parts[i] >= 10:
            carry = n_parts[i]//10
            n_parts[i] = n_parts[i]%10
        else:
            carry = 0
    #Add another number if the carry is still set
    if carry >= 1:
        n_parts = [1] + n_parts
    #Next iteration

print(n, n_parts)
print(count_bouncy, count_nonbouncy)

print("ANS:", n-1)