length = 9
height = 12

#Block is a binary representation of a length x 3 area

def visualize_block(block):
    global length
    s = bin(block)[2:].replace("1", "#").replace("0"," ")
    s = s.rjust(3*length, " ")
    print("┌"+s[:length]+"┐")
    print("│"+s[length:2*length]+"│")
    print("└"+s[2*length:]+"┘")

#Now we need to create masks for each block corresponding to the triominoes
triominoes_by_name = {
    "r": 2**0 + 2**length + 2**(length-1),
    "t": 2**0 + 2**length + 2**(length+1),
    "l": 2**0 + 2**1 + 2**(length+1),
    "j": 2**0 + 2**1 + 2**length,
    "i": 2**0 + 2**length + 2**(2*length),
    "o": 2**0 + 2**1 + 2**2,
}
exclusions = {
    0:["r"],
    -2:["o"],
    -1:["t","l","j","o"]
}

triominoes_by_position = [list(triominoes_by_name.values()) for _ in range(length)]
for key in exclusions:
    for t in exclusions[key]:
        triominoes_by_position[key].remove(triominoes_by_name[t])
triominoes_by_position = [[t<<i for t in T] for i,T in enumerate(triominoes_by_position)]

#Visualize the triominoes_by_position
# for i in range(length):
#     print(i)
#     for t in triominoes_by_position[i]:
#         visualize_block(t)

def recursive_first_row_fill(block, position, next_block_dict):
    if position >= length:
        # unique_complete_blocks.add(block)
        # visualize_block(block)
        block = block>>length #Shift the block since the bottom row is filled
        if block in next_block_dict:
            next_block_dict[block] += 1
        else:
            next_block_dict[block] = 1
        return
    if block & (1<<position):
        #Position filled, call on the next position instead
        recursive_first_row_fill(block, position + 1, next_block_dict)
    # Fill the block from position by all possible triominoes at that position, rejecting those that yield errors
    for triomino in triominoes_by_position[position]:
        if block & triomino == 0:
            #triomino fits in the block at the position, recursively call
            recursive_first_row_fill(block + triomino, position + 1, next_block_dict)

unexplored_blocks = {0}
block_map = {0:{}} # {block: {next_block: count}}
while len(unexplored_blocks) > 0:
    block = unexplored_blocks.pop()
    recursive_first_row_fill(block, 0, block_map[block])
    #Add blocks to be explored if they are new
    for next_block in block_map[block]:
        if next_block not in block_map:
            unexplored_blocks.add(next_block)
            block_map[next_block] = {}

# for block in block_map:
#     print("block: {}, count: {}".format(block, sum(block_map[block].values())))
print("Blocks found:", len(block_map))

#Iterate through the block map to get to the specified height
block_weights = {0:1}
for i in range(height):
    print("level:", i)
    next_block_weights = {}
    for block in block_weights:
        for next_block in block_map[block]:
            if next_block in next_block_weights:
                next_block_weights[next_block] += block_weights[block] * block_map[block][next_block]
            else:
                next_block_weights[next_block] = block_weights[block] * block_map[block][next_block]
    block_weights = next_block_weights
    # print(block_weights)

#Final block added must fill the rectangle
final_block = 0
if final_block in block_weights:
    final_count = block_weights[final_block]
else:
    final_count = 0
print("ans", final_count)