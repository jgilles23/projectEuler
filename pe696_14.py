from functools import cache

class CombGraphRank:
    def __init__(self, mass_limit, modulus, starting_state = (0, ((0,0), ))):
        self.mass_limit, self.mod = mass_limit, modulus
        #Build the combination graph
        def gadd(big_dict, state, addition_dict, ddn, dk, weight): #Add addition_dict into state dict, after modifying entries by ddn and dk
            if state not in big_dict: big_dict[state] = {}
            for choose_tuple, occurances in addition_dict.items():
                new_choose_tuple = (choose_tuple[0] + ddn, choose_tuple[1] + dk) #accumulator (0, +1), pass through (+1, 0)
                big_dict[state][new_choose_tuple] = (big_dict[state].get(new_choose_tuple, 0) + occurances*weight) % self.mod
        self.graph = {} #state: {dchoose: occurances} where dchoose: (dn, k) where choose(n - dn, k)
        queue = {starting_state: {(0, -1): 1}} #same as graph, but not yet processed
        while queue:
            state = min(queue, key=self.score_state) #Go through the state in an order
            dchooses = queue.pop(state) #Get an item from the queue
            next_states = self.state_step(state) #returns {state: weight} dict of next states
            ddn, dk = (0, 1) if state in next_states else (1, 0) #Accumular node, otherwise this is a pass through node
            gadd(self.graph, state, dchooses, ddn, dk, weight = 1) #Add the modified dchoose values to the comb_graph
            for next_state, weight in next_states.items(): #Add the next nodes to the queue
                if next_state != state: #Don't add self to queue
                    gadd(queue, next_state, dchooses, ddn, dk, weight)
    @cache
    def modular_choose(self, n, k): #Modular choose function using modular inverse for division
        if k > n or k < 0: return 0
        a, b = 1, 1
        for i in range(1, k + 1):
            a, b = (a * (n - i + 1)) % self.mod, (b * i) % self.mod
        return (a * pow(b, -1, self.mod)) % self.mod
    @cache
    def evaluate_combinations(self, state, n):
        if state not in self.graph: return 0
        total = 0
        for (dn, k), occurances in self.graph[state].items():
            total = (total + occurances * self.modular_choose(n - dn, k)) % self.mod
        return total
    #Subclass specific functions
    @cache
    def tail_to_states(self, head_mass, tail): #Head_mass, tail -> (new_head_mass, tail_set)
        new_states = {}
        for pair, chow, pung in [(x,y,z) for x in range(2) for y in range(2) for z in range(5)]:
            if (delta_head_mass := tail[0] + pung + 3*chow + 2*pair) > 4: continue #Only 4 tiles per type
            elif (new_total_mass:= head_mass + delta_head_mass + sum(new_tail := (tail[1] + pung, pung))) > self.mass_limit: continue #Too heavy
            elif new_total_mass % 3 == 1: continue #Invalid mass modulus
            new_states[head_mass + delta_head_mass] = new_states.get(head_mass + delta_head_mass, set()) | {new_tail}
        return new_states
    @cache
    def state_step(self, state): #state as (head_mass, tail_set) -> {new_state: weight}
        new_states = {}
        for tail in state[1]:
            sub_states = self.tail_to_states(state[0], tail)
            for sub_mass, sub_tail_set in sub_states.items():
                new_states[sub_mass] = new_states.get(sub_mass, set()) | sub_tail_set
        return {(m, tuple(sorted(tail_set))): 1 for m, tail_set in new_states.items()}
    def score_state(self, state): #Score a state for sorting by the build_comb_graph function
        return (state[0], -1*state[1][0]) #Sort by mass, then by tail 0)
    @cache
    def evaluate(self, mass, ranks):
        total = 0
        for state in self.graph:
            if state[0] == mass and (0,0) in state[1]:
                total = (total + self.evaluate_combinations(state, ranks)) % self.mod
        return total

class CombGraphSuit(CombGraphRank):
    def __init__(self, mass_limit, modulus, ranks, starting_state = 0):
        self.ranks = ranks
        self.rank_graph = CombGraphRank(mass_limit, modulus) #Need to build the rank graph to evaluate the suit graph
        super().__init__(mass_limit, modulus, starting_state = starting_state)
    #Subclass specific functions
    @cache
    def state_step(self, mass): #Return dict of next states with weights for the suit version of the problem
        new_states_weights = {}
        for new_mass in range(mass, self.mass_limit + 1):
            if new_mass % 3 == 1: continue #Invalid mass modulus, involves a pair in two previous suits, which is not possible
            if (weight := self.rank_graph.evaluate(new_mass - mass, ranks = self.ranks)) > 0:
                new_states_weights[new_mass] = weight
        return new_states_weights
    def score_state(self, mass): return mass #Score a state for sorting by the build_comb_graph function
    def evaluate(self, mass, suits): return self.evaluate_combinations(mass, suits)

num_ranks, num_suits, num_tripples = 10**8, 10**8, 30
modulus = 1_000_000_007
mass_target = 3*num_tripples + 2 #Mass limit

suit_graph = CombGraphSuit(mass_limit = mass_target, modulus = modulus, ranks = num_ranks)
print(f"Answer for (ranks: {num_ranks}, suits: {num_suits}, tripples: {num_tripples}): {suit_graph.evaluate(mass_target, num_suits)} ")