# %%

input_real = [
    5616185650518293, 2,
    3847439647293047, 1,
    5855462940810587, 3,
    9742855507068353, 3,
    4296849643607543, 3,
    3174248439465858, 1,
    4513559094146117, 2,
    7890971548908067, 3,
    8157356344118483, 1,
    2615250744386899, 2,
    8690095851526254, 3,
    6375711915077050, 1,
    6913859173121360, 1,
    6442889055042768, 2,
    2321386104303845, 0,
    2326509471271448, 2,
    5251583379644322, 2,
    1748270476758276, 3,
    4895722652190306, 1,
    3041631117224635, 3,
    1841236454324589, 3,
    2659862637316867, 2]

input_test = [
    90342, 2,
    70794, 0,
    39458, 2,
    34109, 1,
    51545, 2,
    12531, 1
]

input = input_real
input_bit = []
input_match = []
L = len(str(input[0]))
for i in range(0, len(input), 2):
    guess_bit = [1 << int(x) for x in str(input[i])]
    input_bit.append(guess_bit)
    input_match.append(input[i+1])
possible_by_position = [2**10 - 1]*L

# %%
# Semi failed method

def recursive_test(possible_bits, input_bits, input_match, pos_start=0):
    #Test if there are no possible matches
    if any([x == 0 for x in possible_bits]):
        return False
    #Test if the problem has been solved
    if len(input_match) == 0:
        print("Found", possible_bits)
        return possible_bits
    #Test options for the next selecton
    guess_bits = input_bits[0]
    guess_matches = input_match[0]
    #Look at 0 matches
    if guess_matches == 0:
        new_possible_bits = [x ^ y for x, y in zip(possible_bits, guess_bits) ]
        r = recursive_test(new_possible_bits, input_bits[1:], input_match[1:])
        if r != 0:
            return r
    else:
        #At least one match, do this inefficiently
        for pos in range(pos_start, L):
            new_possible_bits = possible_bits[:]
            new_possible_bits[pos] = new_possible_bits[pos] & guess_bits[pos]
            new_guess = guess_bits[:pos] + [0] + guess_bits[pos+1:]
            new_input_bits = [new_guess] + input_bits[1:]
            new_input_match = [input_match[0] - 1] + input_match[1:]
            r = recursive_test(new_possible_bits, new_input_bits, new_input_match, pos + 1)
            if r != 0:
                return r
# q = recursive_test(possible_by_position, input_bit, input_match)
# print(q)
# %%
def bit_string_list(input_list):
    # Return a string of the list where each item in the list is turned into a binary string
    return [bin(x) for x in input_list]

# Try again with a popping method this time
def recursive_match(possible_masks, guess_masks, count, start_pos=0):
    new_possible_masks = possible_masks[:]
    for pos in range(start_pos, len(guess_masks)):
        if count > 0:
            #Use that digit as a correct digit - call sub
            if possible_masks[pos] & guess_masks[pos] > 0:
                new_possible_masks[pos] = guess_masks[pos]
                for r in recursive_match(new_possible_masks, guess_masks, count - 1, pos + 1):
                    yield r
        # That was not selected, make that a non-selection
        new_possible_masks[pos] = possible_masks[pos] & ((2**10 - 1) ^ guess_masks[pos])
    if count == 0:
        yield new_possible_masks
    else:
        return

# Test code
# i = 0
# print("Match:", input_match[i], "Guess:", bit_string_list(input_bit[i]))
# for r in recursive_match(possible_by_position, input_bit[i], input_match[i]):
#     print("Possible:", bit_string_list(r))

def recursive_step(possible_masks, input_bits, input_counts, item=0):
    if item >= len(input_counts):
        return possible_masks
    guess_masks = input_bits[item]
    guess_count = input_counts[item]
    if item < 2: print(" -"*item, "Match:", guess_count, "Guess:", bit_string_list(guess_masks))
    for return_masks in recursive_match(possible_masks, guess_masks, guess_count):
        #Check if any of the return masks are 0
        if any([mask == 0 for mask in return_masks]):
            continue
        #Further iterate for non-zero masks
        if item < 2: print(" -"*item, "*Possible:", bit_string_list(return_masks))
        r = recursive_step(return_masks, input_bits, input_counts, item + 1)
        if r != 0:
            return r
    return 0

# Try sorting the inputs first to see if we can do better
# Theory: start with 0s then move from high to low
tupled = [(match, masks) for match, masks in zip(input_match, input_bit)]
tupled.sort()
# tupled = tupled[-1:] + tupled[:-1]
# tupled.append(tupled.pop())
sorted_input_guess_maks = [x[0] for x in tupled]
sorted_input_guess_counts = [x[1] for x in tupled]

r = recursive_step(possible_by_position, sorted_input_guess_counts, sorted_input_guess_maks)
print(r)
#Convert R back to a readable string of digits
ans = [str(bin(x)[2:][::-1].index("1")) for x in r]
ans = "".join(ans)
print("ans", ans)