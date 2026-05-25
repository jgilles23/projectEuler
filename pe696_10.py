#Back to Majohng

#Compact representation of a suit will be a bitmask of the filled positions
#Startin with 

t = 1 #Number of allowed tripples
mass_target = 3*t + 2 #Mass limit

verticle_triple = 0b0001_0001_0001
horizontal_triple = 0b0111
pung = 0b0011

def print_board(board, pos = None):
    row = 0
    while (board >= (1 << (4*row))) or (row == 0):
        line = list(bin((board >> (4*row)) & 0b1111)[2:].zfill(4))
        if pos and pos//4 == row:
            col = pos%4
            line[3 - col] = "X" if line[3 - col] == "1" else "*"
        line = "".join(line)
        line = line.replace("0", ".")
        print(f"{row:02}: {line}")
        row += 1


found_boards = set()
count = 0
def recursive_suit_build(board=0, mass=0, pos=0, pung_allowed=True, max_rank = None, allow_empty_rows = False):
    global count
    if max_rank and (board >= (1 << (4*max_rank))): #board exceeds max suit height
        return
    elif max_rank and (pos >= 4*max_rank): #Position too high for max suit
        return
    elif mass == mass_target: #Found valid configuration
        found_boards.add(board)
        print("Found board with mass", mass)
        print_board(board, pos)
        count += 1
        return
    elif mass > mass_target: #Too much mass
        return
    # elif board in found_boards: #Already been here
    #     return
    elif ((board >> pos) & 0b1) == 1: #Spot taken, cannot place, move to next spot
        recursive_suit_build(board, mass, pos + 1, pung_allowed, max_rank, allow_empty_rows)
        return
    col, row = pos%4, pos//4
    if max_rank and row > max_rank: #Exceeded max suit height, cannot place more pieces
        return
    #Start by adding the verticle triples
    added_piece = verticle_triple << (4*row) << col
    recursive_suit_build(board | added_piece, mass + 3, pos + 1, pung_allowed, max_rank, allow_empty_rows)
    #Horizontal triple
    if col <= 1:
        added_piece = horizontal_triple << (4*row) << col
        if (board & added_piece) == 0:
            recursive_suit_build(board | added_piece, mass + 3, pos + 1, pung_allowed, max_rank, allow_empty_rows)
    #Horizontal pung
    if col <= 2 and pung_allowed:
        added_piece = pung << (4*row) << col
        if (board & added_piece) == 0:
            recursive_suit_build(board | added_piece, mass + 2, pos + 1, False, max_rank, allow_empty_rows)
    #Empty position, must have at least one space filled in each row
    if allow_empty_rows or (col < 3) or (((board >> (4*row)) & 0b1111) > 0):
        recursive_suit_build(board, mass, pos + 1, pung_allowed, max_rank, allow_empty_rows)

recursive_suit_build(max_rank=4, allow_empty_rows=True)
print("count boards", count)
print("unique boards", len(found_boards))