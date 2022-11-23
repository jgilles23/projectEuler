m = 50
T = 10**6

red_start = [0]*m
grey_start = [1]*m

l = m - 1
while red_start[l] + grey_start[l] <= T:
    l += 1
    red_start.append(red_start[l-1] + grey_start[l-m])
    grey_start.append(red_start[l-1] + grey_start[l-1])
    # print(l, ":", red_start[l], grey_start[l], red_start[l] + grey_start[l])

print(l, ":", red_start[l] + grey_start[l])