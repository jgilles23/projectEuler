k_max = 200

lookup = [[set()], [set([1])]]

for n in range(len(lookup), k_max+1):
    print(n, end=", ")
    best = 1000000
    best_sets = []
    for a in range(1, n//2 + 1):
        b = n - a
        for a_set in lookup[a]:
            for b_set in lookup[b]:
                combined_set = a_set.union(b_set)
                if len(combined_set) < best:
                    best = len(combined_set)
                    best_sets = []
                if len(combined_set) == best:
                    best_sets.append(combined_set.union([n]))
                # print("n", n, "a", a, a_set, "b", b, b_set, "combined", len(combined_set), "best", best)
    lookup.append(best_sets)

print("")
full_sum = 0
for i in range(1, k_max+1):
    print(i, ":", len(lookup[i][0]), "count", len(lookup[i]))
    full_sum += len(lookup[i][0]) - 1
print("ANS", full_sum)