import numpy as np
import scipy.sparse as sp
from functools import cache
from math import comb
import time

#Formatting functions
TAIL_MASK = (1 << 15 ) - 1 #Mask to extract tail bits from state
def format_long(state):
    if state == 0:
        return "."*17
    else: #[mass]-[tail in binary]
        return f"{state >> 15}-{bin(state & TAIL_MASK)[2:].zfill(15)}"
def format_short(state, justify = (2, 5)):
    if state == 0:
        return "."*(sum(justify) + 1)
    else: #[mass]-[tail in decimal], 0 filled with zfill
        return f"{str(state >> 15).zfill(justify[0])}-{str(state & TAIL_MASK).zfill(justify[1])}"

#Types of objects:
#state: [head mass][tail mask]
#simplestate: [head mass][tail with only one bit set]
#tail: [#, #] representing the fill of each segment of the tail
#dm: change in head mass
#m3: mass mod 3, used for patriy checks to determine valid states

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
        if (state & TAIL_MASK) & (1 << tail_index) == 0: continue #Tail bit not set
        new_states |= tail_index_to_states(tail_index, state >> 15, mass_limit = mass_limit)
    return new_states

@cache
def suit_state_step(mass, weight_function, mass_limit):
    #Input mass int and weight f(mass)->int; Return new_states:weight dict
    return {new_mass: weight_function(new_mass - mass) for new_mass in range(mass, mass_limit + 1)}

def build_graph(starting_state, mass_limit):
    graph = {}
    queue = [starting_state]
    while queue:
        state = queue.pop(-1)
        graph[state] = state_step(state, mass_limit = mass_limit)
        for dm in range(5):
            if graph[state][dm] != 0 and graph[state][dm] not in graph:
                queue.append(graph[state][dm])
    return graph

def reverse_graph(graph):
    reverse = {}
    for origin_state, destination_states in graph.items():
        for dm in range(5):
            if destination_states[dm] != 0:
                reverse[destination_states[dm]] = reverse.get(destination_states[dm], []) + [(origin_state, dm)]
    return reverse

def flood_graph(graph, start_state):
    #Create a list of all items that can be reached from the start state
    queue = [start_state]
    visited = {start_state}
    while queue:
        current = queue.pop()
        visited.add(current)
        for dm in range(5):
            destination = graph[current][dm]
            if destination != 0 and destination not in visited:
                visited.add(destination)
                queue.append(destination)
    return visited

def generate_step_matrix(mass_target):
    A_length = ((mass_target + 1) << 15) + 1
    A = sp.dok_matrix((A_length, A_length), dtype=int)
    graph = build_graph(starting_state = 1, mass_limit = mass_target)
    for origin_state, destination_states in graph.items():
        for dm in range(5):
            if destination_states[dm] != 0:
                A[destination_states[dm], origin_state] = 1
    return A.tocsr()

def generate_jump_matrix(mass_target, steps):
    A = generate_step_matrix(mass_target)
    print(f"Non-zero entries in A: {A.nnz:,}")
    A_n = A ** steps
    print(f"Non-zero entries in A^{steps}: {A_n.nnz:,}")
    return A_n

def sum_solutions(A_n, mass):
    start_vector = np.zeros(A_n.shape[0], dtype=int)
    start_vector[1] = 1
    finish_vector = A_n * start_vector
    return finish_vector[(mass << 15) + 1:((mass + 1) << 15):2].sum()

def build_comb_graph(starting_state, mass_limit, sort_function):
    def gadd(state_dict, addition_dict, ddn, dk): #Add addition_dict into state dict, after modifying entries by ddn and dk
        for choose_tuple, occurances in addition_dict.items():
            new_choose_tuple = (choose_tuple[0] + ddn, choose_tuple[1] + dk) #accumulator (0, +1), pass through (+1, 0)
            state_dict[new_choose_tuple] = state_dict.get(new_choose_tuple, 0) + occurances
    comb_graph = {} #state: {dchoose: occurances} where dchoose: (dn, k) where choose(n - dn, k)
    queue = {starting_state: {(0, -1): 1}} #same as comb_graph, but not yet processed
    while queue:
        state = min(queue, key=sort_function) #Get the state with the lowest head mass (and thus lowest mass total) to process next
        dchooses = queue.pop(state) #Get an item from the queue
        if state & TAIL_MASK == 1: #If the tail is (0,0) this is an accumpulator node 
            ddn, dk = 0, 1 
        else: #otherwise this is a pass through node
            ddn, dk = 1, 0
        #Add the modified dchoose values to the comb_graph
        if state not in comb_graph: comb_graph[state] = {}
        gadd(comb_graph[state], dchooses, ddn = ddn, dk = dk)
        #Add the next nodes to the queue
        next_states = state_step(state, mass_limit = mass_limit)
        for dm in range(5):
            if next_states[dm] != 0 and next_states[dm] != state: #Don't add self to queue
                if next_states[dm] not in queue:
                    queue[next_states[dm]] = {}
                gadd(queue[next_states[dm]], dchooses, ddn, dk)
    return comb_graph

def permutations_of(state_dict, n):
    total = 0
    for (dn, k), occurances in state_dict.items():
        if (n - dn) >= k:
            total += occurances * comb(n - dn, k)
    return total

def permutations_of_suit(state_dict, n, suit_weight_function):
    total = 0
    for (dn, k), occurances in state_dict.items():
        if (n - dn) >= k:
            total += occurances * comb(n - dn, k) * suit_weight_function(n - dn, k)
    return total

class CombGraphRank:
    def __init__(self, mass_limit, modulus):
        self.mass_limit = mass_limit
        self.mod = modulus
    def build_comb_graph(self, starting_state):
        def gadd(big_dict, state, addition_dict, ddn, dk, weight): #Add addition_dict into state dict, after modifying entries by ddn and dk
            if state not in big_dict: 
                big_dict[state] = {}
            for choose_tuple, occurances in addition_dict.items():
                new_choose_tuple = (choose_tuple[0] + ddn, choose_tuple[1] + dk) #accumulator (0, +1), pass through (+1, 0)
                big_dict[state][new_choose_tuple] = (big_dict[state].get(new_choose_tuple, 0) + occurances*weight) % self.mod
        self.graph = {} #state: {dchoose: occurances} where dchoose: (dn, k) where choose(n - dn, k)
        queue = {starting_state: {(0, -1): 1}} #same as graph, but not yet processed
        while queue:
            state = min(queue, key=self.score_state) #Go through the state in an order
            dchooses = queue.pop(state) #Get an item from the queue
            next_states = self.state_step(state) #returns {state: weight} dict of next states
            if state in next_states: #This is an accumular node
                ddn, dk = 0, 1 
            else: #otherwise this is a pass through node
                ddn, dk = 1, 0
            #Add the modified dchoose values to the comb_graph
            gadd(self.graph, state, dchooses, ddn, dk, weight = 1)
            #Add the next nodes to the queue
            for next_state, weight in next_states.items():
                if next_state != state: #Don't add self to queue
                    gadd(queue, next_state, dchooses, ddn, dk, weight)
    @cache
    def permutations_of(self, state, n):
        total = 0
        for (dn, k), occurances in self.graph[state].items():
            if (n - dn) >= k:
                total = (total + occurances * self.modular_choose(n - dn, k)) % self.mod
        return total
    @cache
    def modular_choose(self, n, k):
        if k > n or k < 0: return 0
        a, b = 1, 1
        for i in range(1, k + 1):
            a = (a * (n - i + 1)) % self.mod
            b = (b * i) % self.mod
        return (a * pow(b, -1, self.mod)) % self.mod
    #Subclass specific functions
    @cache
    def state_step(self, state): #Return dict of next states with weights for the suit version of the problem
        new_states_weights = {}
        for new_state in state_step(state, mass_limit = self.mass_limit):
            if new_state != 0:
                new_states_weights[new_state] = 1
        return new_states_weights
    def score_state(self, state): #Score a state for sorting by the build_comb_graph function
        return (state >> 15, -1*(state & TAIL_MASK))
    def permutations_of_mass(self, mass, n):
        total = 0
        for state in self.graph:
            if (state >> 15) == mass and (state & 1):
                total = (total + self.permutations_of(state, n)) % self.mod #NEED TO CHECK TO MAKE SURE PERMUTATIONS IS WORKING
        return total

class CombGraphSuit(CombGraphRank):
    def __init__(self, mass_limit, rank_limit, rank_graph, modulus):
        super().__init__(mass_limit, modulus = modulus)
        self.rank_graph = rank_graph
        self.rank_limit = rank_limit
    #Subclass specific functions
    @cache
    def state_step(self, mass): #Return dict of next states with weights for the suit version of the problem
        new_states_weights = {}
        for new_mass in range(mass, self.mass_limit + 1):
            weight = self.rank_graph.permutations_of_mass(new_mass - mass, n = self.rank_limit)
            if weight > 0:
                new_states_weights[new_mass] = weight
        return new_states_weights
    def score_state(self, mass): #Score a state for sorting by the build_comb_graph function
        return mass
    def permutations_of_mass(self, mass, n):
        total = 0
        for state in self.graph:
            if state == mass:
                total = (total + self.permutations_of(state, n)) % self.mod
        return total

print("Starting...")
num_ranks = 9
num_suits = 1
num_tripples = 6
modulus = 10**100 + 7
mass_target = 3*num_tripples + 2 #Mass limit


# #Build a graph of the states from the empty state
# graph = build_graph(starting_state = 1, mass_limit = mass_target)
# A_n = generate_jump_matrix(mass_target, steps = num_ranks)
# q = sum_solutions(A_n, mass_target)
# print(f"ANSWER using sparse matrix: {q:,}")
# # for state, destinations in sorted(graph.items()):
# #     print(f"{format_short(state)}: {" ".join([format_short(destinations[dm]) for dm in range(5)])}")
# print()

t0 = time.time()
comb_graph = build_comb_graph(starting_state = 1, mass_limit = mass_target, sort_function=lambda s: (s >> 15, -1*(s & TAIL_MASK)))
t1 = time.time()
print(f"Time to build combination graph: {t1 - t0:.2f} seconds")
# for state, combs in sorted(comb_graph.items()):
#     print(f"{format_short(state)}: {combs}")
finish_state = (mass_target << 15) + 1
print(f"Number of combs in finish state for t={num_tripples}: {len(comb_graph[finish_state])}")
q = permutations_of(comb_graph[finish_state], num_ranks)
print(f"ANSWER using combinations: {q:,}")
print()

#Rank limit
t0 = time.time()
comb_graph_rank = CombGraphRank(mass_limit = mass_target, modulus = modulus)
comb_graph_rank.build_comb_graph(starting_state = 1)
t1 = time.time()
print(f"Time to build combination graph with rank: {t1 - t0:.2f} seconds")
q = comb_graph_rank.permutations_of_mass(mass_target, num_ranks)
print(f"ANSWER using combinations with rank: {q:,}")
# #Test items
# for mass in range(mass_target + 1):
#     print(f"Mass {mass}: {comb_graph_rank.permutations_of_mass(mass, num_ranks):,} combinations")
#Add of the suit limit
t0 = time.time()
comb_graph_suit = CombGraphSuit(mass_limit = mass_target, rank_limit = num_ranks, rank_graph = comb_graph_rank, modulus = modulus)
comb_graph_suit.build_comb_graph(starting_state = 0)
t1 = time.time()
print(f"Time to build combination graph with suit: {t1 - t0:.2f} seconds")
q = comb_graph_suit.permutations_of_mass(mass_target, num_suits)
print(f"ANSWER using combinations with suit: {q:,}")
# for mass in range(4):
#     try:
#         print(mass, comb_graph_suit.graph[mass])
#     except KeyError:
#         print(mass, "No states")
# pass

#OK We have found an issue! The sum at individual levels is not correct
print("Test ")
'''
#Count the number of states by head mass
count_states_by_head_mass = [0]*(mass_target + 1)
#How many unique tail masks are there in the graph as a whole?
unique_tail_occurances = {}
unique_tails = [set() for _ in range(mass_target + 1)]
unique_tails_m3 = [set() for _ in range(3)]
for origin_state, destination_states in graph.items():
    head_mass, tail_mask = origin_state >> 15, origin_state & TAIL_MASK
    count_states_by_head_mass[head_mass] += 1
    unique_tail_occurances[tail_mask] = unique_tail_occurances.get(tail_mask, 0) + 1
    unique_tails[head_mass].add(tail_mask)
    unique_tails_m3[head_mass % 3].add(tail_mask)
#Sort the unique tail masks so that we can get index as needed; but do this smartish
for m3 in range(3):
    unique_tails_m3[m3] = sorted(unique_tails_m3[m3], key=lambda x: unique_tail_occurances.get(x, 0), reverse=True)
for head_mass_mod3, tail_masks in enumerate(unique_tails_m3):
    print(f"Head mass mod 3: {head_mass_mod3}, length {len(tail_masks)}: [{' '.join(map(str, tail_masks))}]")
# reachable = flood_graph(reverse_graph(graph), start_state = (30 << 15) + 1)
# print(reachable)
#Iterate through each mass and print a line with symbols representing the tail masks
max_index = max(len(masks) for masks in unique_tails_m3)
for mass in range(mass_target + 1):
    line = ["."] * max_index
    for tail_mask in unique_tails[mass]:
        i = unique_tails_m3[mass % 3].index(tail_mask)
        line[i] = f"*"
    print(f"Mass {str(mass).zfill(2)}, unique {str(len(unique_tails[mass])).zfill(2)}: {"".join(line)}")

print("Count of states by head mass:", count_states_by_head_mass)
print(f"Unique tail masks: {len(unique_tail_occurances)}")
# for head_mass, tail_masks in enumerate(unique_tails):
#     print(f"Head mass {head_mass}: {" ".join(map(str, sorted(tail_masks)))}")
'''