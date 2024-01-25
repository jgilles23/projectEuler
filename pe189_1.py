import numpy as np

perfect_squares = set([i**2 for i in range(20)])

def brute_next_triangle(left_triangle, above_triangle):
    #Yield triangle colors that work in the situation, where 0 means that triangle is not defined
    #There will always be at least 1 option avaliable
    options = [1,2,3]
    if left_triangle in options:
        options.remove(left_triangle)
    if above_triangle in options:
        options.remove(above_triangle)
    for option in options:
        yield option

def brute_recurive_next(pos, type, sequence, L):
    count = 0
    if len(sequence) == L**2:
        #Finished
        # print(sequence)
        return 1
    #left most
    elif pos in perfect_squares:
        for next_triangle in [1,2,3]:
            new_sequence = sequence + (next_triangle, )
            count += brute_recurive_next(pos + 1, "down", new_sequence, L)
    elif type == "down":
        left_triangle = sequence[-1]
        above_triangle = sequence[pos - 2*int(pos**0.5)]
        for next_triangle in brute_next_triangle(left_triangle, above_triangle):
            new_sequence = sequence + (next_triangle, )
            count += brute_recurive_next(pos + 1, "up", new_sequence, L)
    elif type == "up":
        left_triangle = sequence[-1]
        for next_triangle in brute_next_triangle(left_triangle, 0):
            new_sequence = sequence + (next_triangle, )
            count += brute_recurive_next(pos + 1, "down", new_sequence, L)
    else:
        raise Exception
    return count

bitmask_high = int("10"*20, 2)
bitmask_low = bitmask_high >> 1
# print(bin(bitmask_high), bin(bitmask_low))

def bitwise_row_compatable_test(A, B, bit_length):
    C = A ^ B ^ (bit_length**2 - 1)
    combined = ((C & bitmask_high) >> 1) & (C & bitmask_low)
    return combined == 0

def generate_row_options(row_length):
    bitmask_ones = 2**(2*row_length) - 1
    for n in range(bitmask_ones + 1):
        C = n ^ bitmask_ones
        combined = ((C & bitmask_high) >> 1) & (C & bitmask_low)
        if combined == 0:
            yield n

def add_down_row(previous_row_counts: dict, previous_row_length: int):
    new_row_counts = dict()
    for new_row in generate_row_options(previous_row_length): 
        count = 0
        for previous_row in previous_row_counts: 
            if bitwise_row_compatable_test(new_row, previous_row, previous_row_length):
                count += previous_row_counts[previous_row]
        new_row_counts[new_row]  = count
    return new_row_counts

#TRY A NEW METHOD
#left then top
# expand_color_options = {x:{y: "123" for y in "0123"} for x in "0123"}
# for left_triangle in "0123":
#     for above_triangle in "0123":
#         expand_color_options[left_triangle][above_triangle] = expand_color_options[left_triangle][above_triangle].replace(left_triangle, "")
#         expand_color_options[left_triangle][above_triangle] = expand_color_options[left_triangle][above_triangle].replace(above_triangle, "")
# print(expand_color_options)


class Mapper:
    def __init__(self, L):
        #Make a mapper for L
        self.L = L
        self.triangle_to_index = list(range(L**2))
        # self.index_to_triangle = list(range((L+1)**2))
        self.perfect_squares = set([i**2 for i in range(L)])
        self.current_triangle = 0
    
    def get_index(self, triangle):
        return self.triangle_to_index[triangle]
    
    def get_triangle(self, index):
        return self.index_to_triangle[index]
    
    def get_left_triangle(self):
        #get triangle to the left of the current triangle
        if self.current_triangle in self.perfect_squares:
            return None
        else:
            return self.current_triangle - 1
    
    def get_above_triangle(self):
        #get triangle above the current triangle
        if (self.current_triangle - int(self.current_triangle**0.5)) % 2 == 1:
            #downward triangle
            return self.current_triangle - 2*int(self.current_triangle**0.5)
        else:
            #upward triangle
            return None
    
    def get_left_triangle_index(self):
        triangle = self.get_left_triangle()
        if triangle is None:
            return None
        else:
            return self.triangle_to_index[triangle]
    
    def get_above_triangle_index(self):
        triangle = self.get_above_triangle()
        if triangle is None:
            return None
        else:
            return self.triangle_to_index[triangle]
    
    def step_triangle(self):
        self.current_triangle += 1
        left_index = self.get_left_triangle_index()
        above_index = self.get_above_triangle_index()
        # step the current triangle by 1
        # recreate the maps to update the index
        # return index to be removed from the hash
        if (self.current_triangle - int(self.current_triangle**0.5)) % 2 == 1:
            #downward triangle
            triangle_to_remove = self.get_above_triangle()
        else:
            #upward triangle
            triangle_to_remove = self.get_left_triangle()
        if triangle_to_remove is None:
            index_to_remove = None
        else:
            index_to_remove = self.triangle_to_index[triangle_to_remove]
            self.triangle_to_index[triangle_to_remove] = None
            for t in range(triangle_to_remove+1, self.L**2):
                if self.triangle_to_index[t] is not None:
                    self.triangle_to_index[t] -= 1
        return left_index, above_index, index_to_remove

def minimize_hash(hash: str):
    #Produce the minimum value of the hash
    if hash[0] != "1":
        hash = hash.replace("1", "$").replace(hash[0], "1").replace("$", hash[0])
    for next_char in hash[1:]:
        if next_char != "1":
            break
    if next_char == "3":
        hash = hash.replace("2", "$").replace("3", "2").replace("$", "3")
    return hash

L = 8
M = Mapper(L)
alphabet_hash = tuple(range(L**2))
hash_counts = {"1": 3}
for i in range(L**2 - 1):
    # left_index, above_index, remove_index = M.step_triangle()
    # print("triangle", M.current_triangle, "left", "0" if left_index is None else hash[left_index], "above", "0" if above_index is None else hash[above_index], "remove_index", remove_index)
    # if remove_index is not None:
    #     hash = hash[:remove_index] + hash[remove_index+1:]

    new_hash_counts = {}
    left_index, above_index, remove_index = M.step_triangle()
    #Display progress
    print("triangle", M.current_triangle, "left", "N" if left_index is None else alphabet_hash[left_index], "above", "N" if above_index is None else alphabet_hash[above_index], "remove_index", remove_index)
    if remove_index is not None:
        alphabet_hash = alphabet_hash[:remove_index] + alphabet_hash[remove_index+1:]
    #Iterate through the previous hashes
    for hash in hash_counts:
        left_value = "0" if left_index is None else hash[left_index]
        above_value = "0" if above_index is None else hash[above_index]
        for new_value in "123".replace(left_value,"").replace(above_value,""):
            #expand
            new_hash = hash + new_value
            #chop - remove unnecessary index
            if remove_index is not None:
                new_hash = new_hash[:remove_index] + new_hash[remove_index+1:]
            #minimize
            new_hash = minimize_hash(new_hash)
            #collapse into new dictionary
            if new_hash in new_hash_counts:
                new_hash_counts[new_hash] += hash_counts[hash]
            else:
                new_hash_counts[new_hash] = hash_counts[hash]
    hash_counts = new_hash_counts

ans = sum(hash_counts.values())
print("ans", ans)

# print("brute", brute_recurive_next(0, "up", tuple(), L))




# L = 2

# map_triangle_to_index = list(range((L+1)**2))
# map_triangle_to_left = 1

# print(minimize_hash("133333111211111"))

# A = add_down_row({1:1, 2:1, 3:1}, 1)
# print(A)

# count = brute_recurive_next(0, "up", tuple(), 4)
# print(count)
# print(bitwise_row_compatable_test(int("1111", 2), int("1110", 2), 4))
# for A in generate_row_options(3):
#     print(bin(A))
# print(brute_recurive_next(0, "up", tuple(), 2))