#number to a power
sequence = []
n_by_p = [0, 0, 2, 2]
a_by_p = [float('inf'), float('inf'), 4, 8]

while len(sequence) < 30:
    m = min(a_by_p)
    j = a_by_p.index(m)
    n_by_p[j] += 1
    a_by_p[j] = n_by_p[j]**j
    if j == len(n_by_p) - 1:
        n_by_p.append(2)
        a_by_p.append(2**(j+1))
    #Check if matches the sequence
    sum_dig = sum([int(x) for x in str(a_by_p[j])])
    if sum_dig == n_by_p[j]:
        sequence.append(a_by_p[j])
        print("FOUND", len(sequence), ":", n_by_p[j], "**", j, "=", a_by_p[j])
    # print(n_by_p, a_by_p)
# print(sequence)
print(sequence[-1])