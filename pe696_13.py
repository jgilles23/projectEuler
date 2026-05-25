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
    def modular_choose(self, n, k):
        if k > n or k < 0: return 0
        a, b = 1, 1
        for i in range(1, k + 1):
            a = (a * (n - i + 1)) % self.mod
            b = (b * i) % self.mod
        return (a * pow(b, -1, self.mod)) % self.mod
    @cache
    def evaluate_combinations(self, state, n):
        if state not in self.graph:
            return 0
        total = 0
        for (dn, k), occurances in self.graph[state].items():
            total = (total + occurances * self.modular_choose(n - dn, k)) % self.mod
        return total
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
    @cache
    def evaluate(self, mass, ranks):
        total = 0
        for state in self.graph:
            if (state >> 15) == mass and (state & 1):
                total = (total + self.evaluate_combinations(state, ranks)) % self.mod
        return total

class CombGraphSuit(CombGraphRank):
    def __init__(self, mass_limit, modulus, ranks, rank_graph):
        self.ranks = ranks
        self.rank_graph = rank_graph
        super().__init__(mass_limit, modulus)
    #Subclass specific functions
    @cache
    def state_step(self, mass): #Return dict of next states with weights for the suit version of the problem
        new_states_weights = {}
        for new_mass in range(mass, self.mass_limit + 1):
            if new_mass % 3 == 1: 
                continue #Invalid mass modulus, involves a pair in two previous suits, which is not possible
            weight = self.rank_graph.evaluate(new_mass - mass, ranks = self.ranks)
            if weight > 0:
                new_states_weights[new_mass] = weight
        return new_states_weights
    def score_state(self, mass): #Score a state for sorting by the build_comb_graph function
        return mass
    def evaluate(self, mass, suits):
        return self.evaluate_combinations(mass, suits)

#Evaluation
print("Starting...")
num_ranks = 10**8
num_suits = 10**8
num_tripples = 30
modulus = 1_000_000_007
mass_target = 3*num_tripples + 2 #Mass limit


#Rank limit
t0 = time.time()
rank_graph = CombGraphRank(mass_limit = mass_target, modulus = modulus)
rank_graph.build_comb_graph(starting_state = 1)
print(f"Rank graph built in {time.time() - t0:.2f} seconds")
#Add of the suit limit
t0 = time.time()
suit_graph = CombGraphSuit(mass_limit = mass_target, modulus = modulus, ranks = num_ranks, rank_graph = rank_graph)
suit_graph.build_comb_graph(starting_state = 0)
print(f"Suit graph built in {time.time() - t0:.2f} seconds")
q = suit_graph.evaluate(mass_target, num_suits)
print(f"Answer for (ranks: {num_ranks}, suits: {num_suits}, tripples: {num_tripples}): {q:,}")
print("asn:", q)

#PRODUCES THE CORRECT SOLUTION!!!!!!!!!! Cleaning up for posting

'''
print()
print("Validating rank_graph...")
#OK, try to calculate ranks in a way we know works to validate results
expanders = [(a, pung, pung) for pung in range(5) for chow in range(2) for pair in range(2) if (a := pung + 3*chow + 2*pair) <= 4]
permutations_by_mass_rank = [set() for _ in range(mass_target + 1)]
mass_queue = [set() for mass in range(mass_target + 1)] #mass: set of tail states with that mass
mass_queue[0].add((0, 0)) #Start with empty tail
for queue_mass, queue in enumerate(mass_queue):
    while queue:
        state = queue.pop()
        state_mass = sum(state)
        if state_mass > mass_target or len(state) > num_ranks + 2: #Too heavy or too many ranks
            continue
        elif state_mass % 3 == 1: #Invalid mass modulus
            continue
        elif len(state) == num_ranks + 2 and state[-2] == 0 and state[-1] == 0:
            permutations_by_mass_rank[state_mass].add(state)
            # print("Found permutation:", state)
            continue
        head, a0, a1 = state[:-2], state[-2], state[-1]
        for b0, b1, b2 in expanders:
            new_state = head + (a0 + b0, a1 + b1, b2)
            new_mass = sum(new_state)
            if a0 + b0 <= 4 and new_mass <= mass_target:
                mass_queue[new_mass].add(new_state)
    brute_answer = len(permutations_by_mass_rank[queue_mass]) % modulus
    graph_answer = rank_graph.evaluate(queue_mass, num_ranks)
    print(f"Mass {queue_mass}: Brute Answer: {brute_answer:,}, Graph Answer: {graph_answer:,}, Equal: {brute_answer == graph_answer}")
    if brute_answer != graph_answer:
        raise Exception("Rank graph validation failed")

print("Validating suit_graph...")
#OK, now try to calculate suits in a way we know works
permutations_by_mass_suit = [set() for _ in range(mass_target + 1)]
mass_queue = [set() for mass in range(mass_target + 1)] #mass: set of tail states with that mass
mass_queue[0].add(tuple()) #Start with empty tail
for queue_mass, queue in enumerate(mass_queue):
    while queue:
        state = queue.pop()
        state_mass = sum(state)
        if state_mass > mass_target or len(state) > num_suits or state_mass % 3 == 1: #Too heavy or too many suits
            continue
        elif len(state) == num_suits:
            permutations_by_mass_suit[state_mass].add(state)
            # print("Found permutation:", state)
            continue
        for b in range(0, mass_target + 1 - state_mass):
            new_state = state + (b,)
            new_mass = state_mass + b
            if new_mass <= mass_target and new_mass % 3 != 1:
                mass_queue[new_mass].add(new_state)
    #To calculate the answer for this mass, multiply together the permutations
    mass_permutations = 0
    for state in permutations_by_mass_suit[queue_mass]:
        suit_permutations = 1
        for m in state:
            suit_permutations *= len(permutations_by_mass_rank[m])
        mass_permutations += suit_permutations
    brute_answer = mass_permutations % modulus
    graph_answer = suit_graph.evaluate(queue_mass, num_suits)
    print(f"Mass {queue_mass}: Brute Answer: {brute_answer:,}, Graph Answer: {graph_answer:,}, Equal: {brute_answer == graph_answer}")
    if brute_answer != graph_answer:
        raise Exception("Suit graph validation failed")
'''
