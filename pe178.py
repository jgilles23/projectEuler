# %%
P = 40



count = 0

for starting_digit in range(10):
    reached_none = [0]*10
    reached_0 = [0]*10
    reached_9 = [0]*10
    reached_09 = [0]*10
    reached_none[starting_digit] = 1
    p = 1
    while True:
        # Classify
        reached_0[0] += reached_none[0]
        reached_none[0] = 0
        reached_9[9] += reached_none[9]
        reached_none[9] = 0
        reached_09[9] += reached_0[9]
        reached_0[9] = 0
        reached_09[0] += reached_9[0]
        reached_9[0] = 0
        # Print
        print("p:", p)
        print("  None:", reached_none)
        print("  Zero:", reached_0)
        print("  Nine:", reached_9)
        print("  Both:", reached_09)
        # Count completions, lead digit cannot be 0
        count += sum(reached_09[1:])
        #Check for end
        if p == P:
            break
        # Process
        for L in [reached_none, reached_0, reached_9, reached_09]:
            new_L = [0]*10
            new_L[0] = L[1]
            new_L[9] = L[8]
            for i in range(1,9):
                new_L[i] = L[i-1] + L[i+1]
            L[:] = new_L
        #Iterate
        p += 1

print("ans", count)

# %%
