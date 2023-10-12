# %%
# Base representation of black and white in each type [(B,W), (B,W), (B,W)]
# Where B0 >= B1 >= B2, etc.
# Where B0 = B1 = B2 = ...
#   W1 >= W2 >= W3 >= ...
# B,W >= 0




def branching(ordered_groups=tuple(), count_B=0, count_W=0):
    if count_B == target_B and count_W == target_W:
        # print(ordered_groups)
        return 1
    # Add B and W
    count = 0
    max_b = min(target_B - count_B,
                ordered_groups[-1][0] if len(ordered_groups) > 0 else 10**10)
    # 1 if target not reached, 0 if target reached
    min_b = int(count_B < target_B)
    for b in range(min_b, max_b + 1):
        # Now also iterate through w
        max_w = target_W - count_W
        min_w = 0 if b > 0 else 1
        if len(ordered_groups) > 0 and ordered_groups[-1][0] == b:
            max_w = min(max_w, ordered_groups[-1][1])
        for w in range(min_w, max_w + 1):
            count += branching(ordered_groups + ((b, w),),
                               count_B + b, count_W + w)
    return count


def collapsed():
    # Tail has the following format: (previous B, previous, W, remaining B, remaining W)
    complete_count = 0
    tails={(target_B, target_W, target_B, target_W): 1}
    while len(tails) > 0:
        new_tails = {}
        for tail in tails:
            previous_B, previous_W, remaining_B, remaining_W = tail
            if remaining_B == 0 and remaining_W == 0:
                complete_count += tails[tail]
                continue
            min_b = 0 if remaining_B == 0 else 1
            max_b = min(previous_B, remaining_B)
            for b in range(min_b, max_b + 1):
                min_w = 0 if remaining_B > 0 else 1
                if b == previous_B:
                    max_w = min(remaining_W, previous_W)
                else:
                    max_w = remaining_W
                for w in range(min_w, max_w + 1):
                    new_tail = (b, w, remaining_B - b, remaining_W - w)
                    if new_tail in new_tails:
                        new_tails[new_tail] += tails[tail]
                    else:
                        new_tails[new_tail] = tails[tail]
        tails = new_tails
    return complete_count

target_B = 60
target_W = 40

# print(branching())
print("ans", collapsed())
