import numpy as np
from datetime import datetime

def brute(a, b, K):
    # Return the sequence with k terms, Ulam(a,b)
    sequence = [a,b]
    c = b
    while len(sequence) < K:
        c += 1
        count = 0
        for i, x in enumerate(sequence):
            for y in sequence[i+1:]:
                count += x + y == c
        if count == 1:
            sequence.append(c) 
    # print(sequence)
    # deltas = [0] + [y - x for x,y in zip(sequence[:-1], sequence[1:])]
    # print(np.array(deltas))
    # printable = np.array([sequence, deltas])
    # print(printable)
    return sequence

def sieve(a, b, N):
    #Use a sieve to find numbers that work
    hit_count = np.full(N, 0)
    sequence = [a,b]
    hit_count[a+b] = 1
    for x in range(a+b,N):
        if hit_count[x] != 1:
            continue
        #Append the hit count with x plus items already in the sequence
        for c in sequence:
            if c + x >= N:
                break
            hit_count[c + x] += 1
        #Finish by adding x to the sequence
        sequence.append(x)
    # print(sequence)
    deltas = (np_sequence := np.array(sequence))[1:] - np_sequence[:-1]
    # print(deltas)
    # print(hit_count)
    return(sequence)

def fast_sieve(b, N):
    #Use a faster sieve method to find numbers that work
    #Assumes a = 2 & b > 5
    #Exclude large even numbers to make it faster
    if b % 2 == 0 or b < 5:
        raise Exception("Invalid b.")
    #Setup the inital odds
    initial_odds = list(range(b, 2*b + 2, 2))
    #Set up the sieve
    hit_count_odd = np.full((N + 2*b + 2)//2 + 1, 0)
    hit_count_odd[b//2] += 1
    #Setup the other even
    other_even = 2*b + 2
    other_even_location = (b+2)//2 + 1
    #Iterate through the odds
    sequence = []
    for i, x in enumerate(range(1, N, 2)):
        if hit_count_odd[i] != 1:
            continue
        #Update the hit_counts
        hit_count_odd[(2 + x)//2] += 1
        hit_count_odd[(other_even + x)//2] += 1
        #Add to the sequence
        sequence.append(x)
    sequence.insert(other_even_location, other_even)
    sequence.insert(0, 2)
    # print(sequence)
    return(sequence)


def bitmask(b, N):
    c = 2*b + 2
    #Use a bitmask to find repitition
    odd_array = np.full(N//2 + c//2 - ((N//2) % (c//2)), False)
    odd_array[b//2:c//2] = True
    for i in range(c//2, len(odd_array)):
        odd_array[i] = odd_array[i-1] != odd_array[i-b-1]
    #Convert odd array to something more useable
    compressed_odd_array = np.full(len(odd_array)//(c//2), 0)
    for j in range(c//2):
        compressed_odd_array *= 2 #Leftshift
        compressed_odd_array += odd_array[j::c//2] #Add new int
    print(compressed_odd_array)
    return compressed_odd_array
    #Produce the sequence requested
    # sequence = [2*i + 1 for i, flag in enumerate(odd_array) if flag]
    # sequence.insert(b//2+2, c)
    # sequence.insert(0, 2)
    # print(sequence)
    # return sequence

def bitmask_rolling(b):
    c = 2*b + 2
    sieve = 2**(c//2 - b//2) - 1
    full = 2**(c//2) - 1
    yield sieve
    # sequence = [sieve]
    while True:
        for _ in range(c//2): 
            sieve = ((sieve & 1) ^ (sieve >> (c//2 - 1))) + ((sieve << 1) & full)
        yield sieve
    #     sequence.append(sieve)
    # print(np.array(sequence))

def repitition_finder(b):
    gen = bitmask_rolling(b)
    initial = gen.__next__()
    count = 1
    odd_count = initial.bit_count()
    while (nxt := gen.__next__()) != initial:
        odd_count += nxt.bit_count()
        count += 1
    print(count, odd_count)
    return count

def rolling_rep_finder(b):
    c = 2*b + 2
    window = np.full(b + 1, False)
    window[b//2:] = True
    initial = window.copy()
    count = 0
    odd_count = np.sum(window)
    while True:
        count += 1
        for c_pointer in range(c//2):
            item = window[c_pointer - 1] ^ window[c_pointer] #2_pointer XOR c_pointer
            window[c_pointer] = item
            odd_count += item
        if np.array_equal(initial, window):
            break
        # odd_count += np.sum(window)
    odd_count -= np.sum(window)
    print(count, odd_count)

def bitmask_rolling_with_count(b):
    c = 2*b + 2
    sieve = 2**(c//2 - b//2) - 1
    initial = sieve
    full = 2**(c//2) - 1
    odd_count = sieve.bit_count()
    count = 0
    # sequence = [sieve]
    while True:
        count += 1
        for _ in range(c//2):
            sieve = ((sieve & 1) ^ (sieve >> b)) + ((sieve << 1) & full)
        if initial == sieve:
            break
        odd_count += sieve.bit_count()
    # odd_count -= sieve.bit_count()
    # print(count, odd_count)
    return 2*(count*c//2), odd_count

def bitmask_rolling_stopper(b, k):
    c = 2*b + 2
    sieve = 2**(c//2 - b//2) - 1
    full = 2**(c//2) - 1
    odd_count = sieve.bit_count()
    count = c//2 - 1
    # sequence = [sieve]
    while odd_count < k:
        count += 1
        item = ((sieve & 1) ^ (sieve >> b))
        sieve = item + ((sieve << 1) & full)
        odd_count += item
    #Back calc which odd number is being called
    # print(count*2 + 1)
    return count*2 + 1

def U_cycles(b, k):
    cycle_length, odds_per_cycle = bitmask_rolling_with_count(b)
    print("b: {}".format(b))
    print("  odds per cycle: {:,}, cycle length {:,}".format(odds_per_cycle, cycle_length))
    complete_cycles = (k-2) // odds_per_cycle
    k_remaining = (k - 2) % odds_per_cycle
    print("  complete cycles: {:,}, k_remaining: {:,}".format(complete_cycles, k_remaining))
    value = complete_cycles*cycle_length + bitmask_rolling_stopper(b, k_remaining)
    print("  value: {:,}".format(value))
    return value

k = 10**11
start = datetime.now()
total = 0
for n in range(2, 11):
    total += U_cycles(2*n + 1, k)
print("ans", total)
print("time", datetime.now() - start)

# b = 11
# N = 2000
# k = 10000
# U_cycles(b, k)
# print("sieve", fast_sieve(b, 5*k)[k-1])
# brute(2,9,40)
# seq = sieve(2, b, N)
# print(len(seq))
# seq = fast_sieve(b, N)
# seq = bitmask(b, N)
# print(len(seq))
# bitmask_rolling(b)
# start = datetime.now()
# count = repitition_finder(b)
# print(datetime.now() - start)
# A = bitmask(b,N)
# print(A[0], A[count])
# rolling_rep_finder(b)
# start = datetime.now()
# bitmask_rolling_with_count(b)
# print(datetime.now() - start)

# print(np.unpackbits(np.array([4], dtype=np.uint8)))

# TRY A FASTER STRATEGY

# def chunker(b):
#     c = 2*b + 2
#     block_size = c//4
#     full_block = 2**(block_size) - 1
#     bit_masks = [2**i for i in range(block_size-1, -1, -1)]
#     # Create the block map -- [lead_bit, block] -> next_block
#     block_map = np.full((2,2**block_size), 0)
#     block_odd_count = np.full(2**block_size, 0)
#     for super_lead_bit in range(2):
#         for block in range(2**block_size):
#             new_block = 0
#             odd_count = 0
#             lead_bit = super_lead_bit
#             for bit_mask in bit_masks:
#                 lead_bit = lead_bit ^ bool(block & bit_mask)
#                 new_block = (new_block << 1) + lead_bit
#                 odd_count += lead_bit
#             block_map[super_lead_bit, block] = new_block
#             block_odd_count[new_block] = odd_count
#     # Interate through blocks to create chunks of (4) blocks until a repeat is found
#     three_quarter_chunk = 2**(block_size*3) - 1
#     initial_chunk = 2**(c//2 - b//2) - 1
#     chunk = initial_chunk
#     chunk_count = 0
#     odd_count = initial_chunk.bit_count()
#     while True:
#         chunk_count += 1
#         for _ in range(4):
#             chunk = ((chunk & three_quarter_chunk) << block_size) + block_map[chunk & 1, chunk >> (3*block_size)]
#             odd_count += block_odd_count[chunk & full_block]
#         if chunk == initial_chunk:
#             break
#     odd_count -= chunk.bit_count()
#     print(chunk_count, odd_count)



# b = 9
# chunker(b)