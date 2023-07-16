N = 10**9

reversable_count = 0
for n in range(N):
    reverse = str(n)[::-1]
    if reverse[0] == "0":
        continue
    a = str(n + int(reverse))
    for d in a:
        if d=="0" or d=="2" or d=="4" or d=="6" or d=="8":
            break
    else:
        #Exit normally
        reversable_count += 1
        if reversable_count%1000 == 0:
            print("Found", n, "sum", a, "count", reversable_count)
print("ans", reversable_count)

# Smarter approach would be to look at each length of number and go through the digits,
# Could probably solve on pen and paper, but the brute force finished in like 20 mintes,
# So call it good enough!