import scipy.sparse as sp
import numpy as np
import time

def print_board(board, cursor = None):
    s = "Board:"
    for rank in range(max(1,len(board))):
        s += f"{' >'[rank == cursor]}{board[rank]}"
    print(s)

def add_to_tuple(tup, value, position):
    if position < len(tup):
        return tup[:position] + (tup[position] + value,) + tup[position+1:]
    elif position == len(tup):
        return tup + (value,)
    else:
        raise ValueError("Position out of bounds")


t = 4 #Number of allowed tripples
mass_target = 3*t + 2 #Mass limit
num_ranks = 9
empty_rank_allowed = True

count = 0
found_boards = set()
def recursive_suit_build(board=(), mass=0, cursor=0, pair_allowed=True):
    if num_ranks and (cursor >= num_ranks): #Exceeded max suit height, cannot place more pieces
        return
    elif num_ranks and (len(board) > num_ranks): #board exceeds max suit height
        return
    elif mass == mass_target: #Found valid configuration
        found_boards.add(board)
        global count
        count += 1
        # print("Found board with mass", mass, end=", ")
        # print_board(board, cursor)
        return
    elif mass > mass_target: #Too much mass
        return
    # elif board in found_boards: #Already been here
    #     return
    value = board[cursor] if cursor < len(board) else 0
    # Add PUNG tripple
    if value <= 1:
        new_board = add_to_tuple(board, 3, cursor)
        recursive_suit_build(new_board, mass + 3, cursor, pair_allowed)
    # Add CHOW tripple
    if value <= 3:
        new_board = add_to_tuple(board, 1, cursor)
        new_board = add_to_tuple(new_board, 1, cursor + 1)
        new_board = add_to_tuple(new_board, 1, cursor + 2)
        recursive_suit_build(new_board, mass + 3, cursor, pair_allowed)
    # Add PAIR
    if pair_allowed and value <= 2:
        new_board = add_to_tuple(board, 2, cursor)
        recursive_suit_build(new_board, mass + 2, cursor, False)
    # Add NOTHING
    if empty_rank_allowed or value > 0:
        new_board = add_to_tuple(board, 0, cursor)
        recursive_suit_build(new_board, mass, cursor + 1, pair_allowed)

# recursive_suit_build()
# print("count boards", count)
# print("unique boards", len(found_boards))

# def count_from_found_boards(at_rank, weight):
#     count = 0
#     for board in found_boards:
#         if sum(board[:at_rank+1]) == weight:
#             count += 1
#     return count


# #Tails of the form (pos0, pos1, pair_allowed, delta_mass)
# def generate_tails(tail, delta_mass_limit = 100, tail_length_limit = 100):
#     #Given an input list of tails generate new tails with a delta_mass
#     new_tails = set() #(pos1, pos2, pair_alowed, delta_mass)
#     queue = [(tail[0], tail[1], 0, tail[2], 0)] #pos0, pos1, pos2, pair_allowed, delta_mass
#     while queue:
#         pos0, pos1, pos2, pair_allowed, delta_mass = queue.pop(0)
#         tail_length = (pos0 > 0) + (pos1 > 0) + (pos2 > 0)
#         if pos0 <= 4 and delta_mass <= delta_mass_limit and tail_length <= tail_length_limit:
#             #Add tail to alowed tails
#             new_tails.add((pos1, pos2, pair_allowed, delta_mass))
#             #Expand the tail with a pung, chow, and pair
#             queue.append((pos0 + 3, pos1, pos2, pair_allowed, delta_mass + 3)) #PUNG
#             queue.append((pos0 + 1, pos1 + 1, pos2 + 1, pair_allowed, delta_mass + 3)) #CHOW
#             if pair_allowed:
#                 queue.append((pos0 + 2, pos1, pos2, False, delta_mass + 2)) #PAIR
#     return new_tails

# print("Generating tails...")
# for a in range(5):
#     for b in range(a+1):
#         allowed_tails = generate_tails((a, b, True))
#         print(f"{(a, b, True)} -> {sorted(allowed_tails)}")
# print()

# def batch_suit_build(input_states = {(0, 0, True, 0):1}, cursor_start = 0, print_flag = False):
#     states = {k:v for k,v in input_states.items()} #board state (tail0, tail1, pair_allowed, total mass) -> count of ways to reach that state
#     for cursor in range(cursor_start, num_ranks):
#         new_states = {}
#         for state, count in states.items():
#             tail0, tail1, pair_allowed, total_mass = state
#             for new_tail in generate_tails((tail0, tail1, pair_allowed), 
#                                         delta_mass_limit = mass_target - total_mass, 
#                                         tail_length_limit = num_ranks - cursor):
#                 new_state = (new_tail[0], new_tail[1], new_tail[2], total_mass + new_tail[3])
#                 new_states[new_state] = new_states.get(new_state, 0) + count
#         states = new_states
#         if print_flag:
#             print(f"After processing rank {cursor}, states: {new_states}")
#             #Need to perform some sort of check aganist the found values
#             for m in range(mass_target + 1):
#                 count_recursive = count_from_found_boards(cursor, m)
#                 count_new = 0
#                 for s, c in states.items():
#                     if s[3] - s[0] - s[1] == m:
#                         count_new += batch_suit_build({s: c}, cursor_start=cursor+1, print_flag=False)
#                 print(f"  Mass {m}: count from states = {count_new}, count from found boards = {count_recursive}")
#     if print_flag:
#         print(f"w(n:{num_ranks}, s:{1}, t:{t}) = {states.get((0, 0, False, mass_target), None)}")
#     return states.get((0, 0, False, mass_target), 0)

# batch_suit_build(cursor_start=0, print_flag=True)
# #{(1, 1, True, 6):1, (0, 0, False, 2):1}

# for board in found_boards:
#     if sum(board[:0+1]) == 2:
#         print_board(board)

def generate_tails_v2(head_mass, input_tail0, input_tail1, tail_length_limit):
    states = set() #(head_mass, tail0, tail1)
    queue = [(input_tail0, input_tail1, 0)]
    while queue:
        tail0, tail1, tail2 = queue.pop(0)
        total_mass = head_mass + tail0 + tail1 + tail2
        tail_length = (tail0 > 0) + (tail1 > 0) + (tail2 > 0)
        if tail0 <= 4 and total_mass <= mass_target and tail_length <= tail_length_limit:
            states.add((head_mass + tail0, tail1, tail2)) #(new head mass, new tail0, new tail1)
            queue.append((tail0 + 3, tail1, tail2)) #PUNG
            queue.append((tail0 + 1, tail1 + 1, tail2 + 1)) #CHOW
            if total_mass % 3 == 0: #Pair allowed
                queue.append((tail0 + 2, tail1, tail2)) #PAIR
        else:
            pass
            # print(f"Discarding tail {(tail0, tail1, tail2)} with head mass {head_mass} and total mass {total_mass}")
    return states

def batch_suit_build_v2():
    states = {(0, 0, 0):1} #(head_mass, tail0, tail1) -> count of ways to reach that state
    for cursor in range(num_ranks):
        new_states = {}
        for state, count in states.items():
            head_mass, tail0, tail1 = state
            for new_state in generate_tails_v2(head_mass, tail0, tail1, tail_length_limit = num_ranks - cursor):
                new_states[new_state] = new_states.get(new_state, 0) + count
        states = new_states
        print(f"After processing rank {cursor}, states: {new_states}")
    return states.get((mass_target, 0, 0), 0)

def batch_generate_tails(head_mass, tails, tail_length_limit):
    return_tails_by_head_mass = {head_mass + i: set() for i in range(5)}
    for tail in tails:
        for returned_tails in generate_tails_v2(head_mass, tail[0], tail[1], tail_length_limit):
            return_tails_by_head_mass[returned_tails[0]].add((returned_tails[1], returned_tails[2]))
    return return_tails_by_head_mass

def string_tail_set(tail_set):
    tail_set = sorted(tail_set)
    return f"{"{"}{" ".join(str(x)+str(y) for x, y in tail_set)}{"}"}"

# starting_mass = 5
# for a in range(5):
#     for b in range(a+1):
#         allowed_tails = generate_tails_v2(starting_mass, a, b, tail_length_limit = 100)
#         print(f"{(starting_mass, a, b)} -> {sorted(allowed_tails)}")

# print(batch_suit_build_v2())

# for k, v in batch_generate_tails(5, [(0,0), (1,0)], tail_length_limit = 10).items():
#     print(f"Head mass {k}: {string_tail_set(v)}")

def batch_suit_build_v3():
    states = {(0, ((0,0), )): 1} #(head_mass, tuple of (tail0, tail1) pairs) -> count of ways to reach that state
    for cursor in range(num_ranks):
        new_states = {}
        for state, count in states.items():
            head_mass, tails = state
            new_tails_by_head_mass = batch_generate_tails(head_mass, tails, tail_length_limit = num_ranks - cursor)
            for new_head_mass, new_tails in new_tails_by_head_mass.items():
                new_state = (new_head_mass, tuple(sorted(new_tails)))
                new_states[new_state] = new_states.get(new_state, 0) + count
        states = new_states
        # print(f"After processing rank {cursor}, states:")
        # for s in states:
        #     print(f"  {s}: {states[s]}")
    return states.get((mass_target, ((0,0), )), 0)

print(f"batch_suit_build_v3() = {batch_suit_build_v3():,}")


tail_options = [(i, j) for i in range(5) for j in range(i+1)]

def state_to_int(state):
    head_mass, tails = state
    tail_int = 0
    for t in tail_options[::-1]: #Reverse to put smaller tails in lower bits
        tail_int = tail_int << 1
        if t in tails:
            tail_int = tail_int | 1
    head_int = head_mass << len(tail_options) #Shift head mass to higher bits
    return head_int + tail_int

def int_to_state(i):
    tails = set()
    for t in tail_options[::-1]: #Reverse to match the order in state_to_int
        if i & 1 == 1:
            tails.add(t)
        i = i >> 1
    head_mass = i
    return (head_mass, tuple(sorted(tails)))

def generate_step_matrix(cursor):
    A_length = (mass_target + 1) * 2**len(tail_options) + 1
    # print(f"Length of A: {A_length:,}")
    A = sp.dok_matrix((A_length, A_length), dtype=int)
    for m in range(mass_target + 1):
        for tail_int in range(2**len(tail_options)):
            _, tails = int_to_state(tail_int)
            origin_int = state_to_int((m, tails))
            for new_head_mass, new_tails in batch_generate_tails(m, tails, tail_length_limit=num_ranks - cursor).items():
                if new_tails: #Only add transitions that lead to valid states
                    destination_int = state_to_int((new_head_mass, tuple(sorted(new_tails))))
                    A[destination_int, origin_int] = 1
    A = A.tocsr()
    return A

from functools import cache
@cache
def tail_index_to_states(tail_index, head_mass, mass_limit = None): #Only runs ~1,000 times, further opimization not needed
    tail_options = [np.array([i, j, 0], dtype=int) for i in range(5) for j in range(i+1)]
    tail_to_index = lambda tail: tail[0]*(tail[0]+1)//2 + tail[1] #Convert a tail [x, y] to an index in tail_options
    expanders = [np.array([a, pung, pung], dtype=int) for pung in range(5) for chow in range(2) for pair in range(2) if (a := pung + 3*chow + 2*pair) <= 4]
    #Add each expander to the tail option, check if valid, and if so OR together the resulting tail masks for each dm value
    new_states = np.zeros(5, dtype=int) #[dm][new tail states]
    for expander in expanders:
        T = tail_options[tail_index] + expander
        dm, new_tail = T[0], T[1:]
        new_total_mass = head_mass + dm + sum(new_tail)
        if dm > 4: continue #dm too large
        elif new_total_mass % 3 == 1: continue #Invalid tail modulus
        elif mass_limit and (new_total_mass > mass_limit): continue #Too heavy
        new_states[dm] |= ((head_mass + dm) << 15) | (1 << tail_to_index(new_tail))  #Head is mass + delta, tail is new tail mask
    return new_states
@cache
def state_step(state, mass_limit = None):
    #Return list of next states by dm
    new_states = np.zeros(5, dtype=int)
    for tail_index in range(15):
        if (state & 0b111111111111111) & (1 << tail_index) == 0: continue #Tail bit not set
        new_states |= tail_index_to_states(tail_index, state >> 15, mass_limit = mass_limit)
    return new_states
def generate_step_matrix_v2(cursor):
    A_length = ((mass_target + 1) << 15) + 1
    A = sp.dok_matrix((A_length, A_length), dtype=int)
    for state in range(A_length):
        new_states = state_step(state, mass_limit = mass_target)
        for dm in range(5):
            if new_states[dm] != 0:
                A[new_states[dm], state] = 1
    return A.tocsr()

def count_solutions(finish_vector, mass):
    x = np.ones(A_length, dtype=int) #Vector of all 1s to sum over all paths
    finish_int_start = state_to_int((mass, ((0,0), )))
    finish_int_end = state_to_int((mass + 1, tuple()))
    finish_int_step = 2
    print(f"Finish int range: {bin(finish_int_start)} to {bin(finish_int_end)} with step {bin(finish_int_step)}")
    count = finish_vector[finish_int_start:finish_int_end:finish_int_step].sum()
    #Count the number of non-zero entries in the finish vector for debugging
    non_zero_count = np.count_nonzero(finish_vector)
    print(f"Non-zero entries in finish vector: {non_zero_count:,}")
    return count



print("Generating step matrix...")
A_length = (mass_target + 1) * 2**len(tail_options) + 1
start_int = state_to_int((0, ((0,0), )))
finish_int = state_to_int((mass_target, ((0,0), )))
x = np.zeros((A_length), dtype=int)
x[start_int] = 1 #Initial state has count of 1
# for cursor in range(num_ranks):
#     A = generate_step_matrix(cursor)
#     print(f"Cursor {cursor}: Non-zero entries in A: {A.nnz:,}")
#     x = A * x
#     print(f"Final count: {x[finish_int]:,}")
t0 = time.time()
A = generate_step_matrix_v2(cursor=0)
t1 = time.time()
print(f"Time to generate step matrix: {t1 - t0:.2f} seconds")
print(f"Non-zero entries in A: {A.nnz:,}")
B = A ** (num_ranks) #Jump matrix
x = B * x
print(f"Non-zero entries in B: {B.nnz:,}")
print(f"ANSWER: {x[finish_int]:,}")

# m = 1*3 + 2
# print(f"Count of solutions with mass {m}: {count_solutions(x, m):,}")

# A = generate_step_matrix(cursor=0)
# B = A ** (10**8)
# print(f"Non-zero entries in B: {B.nnz:,}")


"""
TAIL_MASK = (1 << 15 ) - 1 #Mask to extract tail bits from state
HEAD_MASK = TAIL_MASK << 15 #Mask to extract head mass from state; 15 bits should be enough
format_state = lambda state: f"{state >> 15}|{bin(state & TAIL_MASK)[2:].zfill(15)}" if state != 0 else "."*17 #state is [mass][tail mask]

mass_tail_to_state = lambda mass, tail: (mass << 15) + (1 << (tail[0]*(tail[0]+1)//2 + tail[1])) #state is [mass][tail mask]
tail_options = [np.array([i, j, 0]) for i in range(5) for j in range(i+1)]
expanders = [np.array([a, pung, pung]) for pung in range(5) for chow in range(2) for pair in range(2) if (a := pung + 3*chow + 2*pair) <= 4]
def m3_tail_dm_to_state(m3, tail, dm):
    individual_tails = [mass_tail_to_state(dm, T) for e in expanders if ((T := tail + e)[0] == dm) and ((sum(T) + m3) % 3 != 1)]
    return np.bitwise_or.reduce(individual_tails) if individual_tails else 0
m3simplestate_dm_to_state = {mass_tail_to_state(m3, tail): [m3_tail_dm_to_state(m3, tail, dm) for dm in range(5)] for m3 in range(3) for tail in tail_options} #m3simplestate: [mass 0-2][tail with only one bit set], None for invald states
tail_length_masks = [np.bitwise_or.reduce([mass_tail_to_state(0, tail) if sum(tail > 0) == length else 0 for tail in tail_options]) for length in range(3)]
def state_to_state_by_dm(state, mass_limit = None, tail_limit = None):
    m3 = (state >> 15) % 3
    m3simplestates = [(m3 << 15) | ss for bit_select in range(15) if (ss := (state & (1 << bit_select))) != 0]
    return_state_by_dm = [0]*5
    for dm in range(5):
        a = np.bitwise_or.reduce([m3simplestate_dm_to_state[m3simplestate][dm] for m3simplestate in m3simplestates])
        return_state_by_dm[dm] = a + (state & HEAD_MASK) if a !=0 else 0#Add back head mass to the returned state
        if mass_limit is not None and (return_state_by_dm[dm] >> 15) > mass_limit:
            return_state_by_dm[dm] = 0
        if tail_limit is not None and tail_limit < 3: #TAIL LIMIT NOT IMPLETEMENTED YET
            pass #return_state_by_dm[dm] = 0
    return return_state_by_dm

for length in range(3):
    print(f"Tail length mask for length {length}: {format_state(tail_length_masks[length])}")
"""
