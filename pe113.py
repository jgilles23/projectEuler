increasing_lookup = [[1]*10]
decreasing_count = []


#Number of digits is E
E = 100
for i in range(E):
    increasing_lookup += [[0]*10]
    for j in range(10):
        increasing_lookup[-1][j] = sum(increasing_lookup[-2][j:])
    decreasing_count += [increasing_lookup[-1][0] - 10] 

for a in increasing_lookup:
    print(a)
print(decreasing_count)

print("count non_bouncy", increasing_lookup[-1][0] + sum(decreasing_count)-1)