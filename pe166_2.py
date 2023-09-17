import numpy as np

test_grid = np.array(
    [6, 3, 3, 0] +
    [5, 0, 4, 3] +
    [0, 7, 1, 4] +
    [1, 2, 4, 5]
)

variables = np.full(16, 0)
row_sums = [
    np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
]
column_sums = [
    np.array([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]),
    np.array([0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
    np.array([0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]),
    np.array([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1])
]
diagonal_sums = [
    np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]),
    np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0])
]

all_sums = np.column_stack((*row_sums, *column_sums, *diagonal_sums))

check_matrices = []
for row in range(4):
    for column in range(4):
        if row == column:
            check_matrices.append(np.column_stack((row_sums[row], column_sums[column], diagonal_sums[0])))
        elif row + column == 3:
            check_matrices.append(np.column_stack((row_sums[row], column_sums[column], diagonal_sums[1])))
        else:
            check_matrices.append(np.column_stack((row_sums[row], column_sums[column])))

# print(test_grid @ all_sums)
# for i in range(16):
#     print(test_grid @ check_matrices[i])

def abc_generator(defined_sum):
    for a in range(max(0, defined_sum - 27), min(10, defined_sum + 1)):
        for b in range(max(0, defined_sum - a - 18), min(10, defined_sum - a + 1)):
            for c in range(max(0, defined_sum -a - b - 9), min(10, defined_sum - a - b + 1)):
                yield (a, b, c, defined_sum - a - b - c)
    return

# grid = np.full(16,0)

# count = 0
# defined_sum = 12
# for row0 in abc_generator(defined_sum):
#     print(row0)
#     grid[0:4] = row0
#     for row1 in abc_generator(defined_sum):
#         grid[4:8] = row1
#         if np.any(grid @ all_sums > defined_sum):
#             continue
#         for row2 in abc_generator(defined_sum):
#             grid[8:12] = row2
#             grid[12:16] = 0
#             implied_remaining = defined_sum - (grid @ all_sums)
#             grid[12:16] = implied_remaining[4:8]
#             if np.any(grid < 0) or np.any(grid >=10) or grid[15] != implied_remaining[8] or grid[12] != implied_remaining[9]:
#                 continue
#             # print(implied_remaining, grid, grid @ all_sums)
#             count += 1
#         grid[8:16] = 0
#     grid[4:8] = 0
# print(count)

# min_grid = np.full(16, 0)
# max_grid = np.full(16, 9)
# position = 0



def general_generator(defined_sum, left_sum, right_count, top_sum, bottom_count, diagonal_flag, diagonal_sum, diagonal_count, hard_max):
    #If the final entry in a row, column or diagonal, set x to that value and check aganist other completed items
    if diagonal_flag and diagonal_count == 0:
        x = defined_sum - diagonal_sum
        if (bottom_count == 0 and x != defined_sum - top_sum) or (right_count == 0 and x != defined_sum - left_sum) or (x > hard_max):
            return
        yield x
        return
    elif bottom_count == 0:
        x = defined_sum - top_sum
        if (right_count == 0 and x != defined_sum - left_sum) or (x > hard_max):
            return
        yield x
        return
    elif right_count == 0:
        x = defined_sum - left_sum
        if x > hard_max:
            return
        yield x
        return
    #Iterate through possible values of x given there is some latitude
    for x in range(
        max(0, defined_sum - left_sum - 9*right_count, defined_sum - top_sum - 9*bottom_count, diagonal_flag*(defined_sum - diagonal_sum - 9*diagonal_count)),
        min(hard_max + 1, defined_sum - left_sum + 1, defined_sum - top_sum + 1, (not diagonal_flag)*1000 + (defined_sum - diagonal_sum + 1))
    ):
        yield x

def recursive_position_step(defined_sum, position, box_grid):
    if position >= 16:
        # line_grid = np.reshape(box_grid, (16))
        # print(line_grid, line_grid @ all_sums)
        # Need to test rotations and flips into count
        count = 1
        updated_box_grid = box_grid
        for _ in range(3):
            updated_box_grid = np.rot90(updated_box_grid)
            count += not np.array_equal(updated_box_grid, box_grid)
        updated_box_grid = np.fliplr(box_grid)
        count += not np.array_equal(updated_box_grid, box_grid)
        for _ in range(3):
            updated_box_grid = np.rot90(updated_box_grid)
            count += not np.array_equal(updated_box_grid, box_grid)
        print(count)
        print(box_grid)
        return count
    row = position//4
    column = position % 4
    count = 0
    if position == 3: 
        hard_max = box_grid[0,0]
    elif position == 12:
        hard_max = box_grid[0,3]
    elif position == 15:
        hard_max = box_grid[3,0]
    else:
        hard_max = 9
    for x in general_generator(
        defined_sum, 
        np.sum(box_grid[row, :]), 3 - column, 
        np.sum(box_grid[:, column]), 3 - row,
        (row == column or row + column == 3), (row == column)*np.trace(box_grid) + (row + column == 3)*np.trace(np.fliplr(box_grid)), 3 - row,
        hard_max #Hard Max
        ):
        box_grid[row, column] = x
        count += recursive_position_step(defined_sum, position + 1, box_grid)
    box_grid[row, column] = 0
    return count


# count = 0
# max_sum = 1 #9*2
# for defined_sum in range(0, max_sum + 1):
#     box_grid = np.full((4,4), 0)
#     sub_count = recursive_position_step(defined_sum, 0, box_grid)
#     count += sub_count
#     print("sum: {}, sub_count: {:,}".format(defined_sum, sub_count))
# print("ans", count*2)

# sum: 0, sub_count: 1
# sum: 1, sub_count: 8
# sum: 2, sub_count: 48
# sum: 3, sub_count: 200
# sum: 4, sub_count: 675
# sum: 5, sub_count: 1,904
# sum: 6, sub_count: 4,736
# sum: 7, sub_count: 10,608
# sum: 8, sub_count: 21,925
# sum: 9, sub_count: 42,328
# sum: 10, sub_count: 76,976
# sum: 11, sub_count: 131,320
# sum: 12, sub_count: 209,127
# sum: 13, sub_count: 309,968
# sum: 14, sub_count: 427,440

def second_generator(defined_sum, *constraint_tuples:[(int, int)]):
    #Tuples of the form (current sum of constraint, number of cells yet to fill of constriant)
    low_range = max(0, *[defined_sum - s - 9*c for s, c in constraint_tuples])
    high_range = min(9, *[defined_sum - s for s, c in constraint_tuples])
    for x in range(low_range, high_range + 1):
        yield x

defined_sum = 35
count = 0
for defined_sum in range(0, 2*9 + 1):
    sub_count = 0
    for a in second_generator(defined_sum, (0, 3)):
        for f in second_generator(defined_sum, (a, 2), (0, 3)):
            for k in second_generator(defined_sum, (a+f, 1), (0, 3)):
                p = defined_sum - a - f - k
                for g in second_generator(defined_sum, (f, 2), (k, 2), (0, 3), (f+k, 1)): #row, column, anti-diagonal, inner-box
                    j = defined_sum - f - g - k
                    for m in second_generator(defined_sum, (a, 2), (p, 2), (j+g, 1), (a+p,1)):
                        d = defined_sum - g - j - m
                        for e in second_generator(defined_sum, (f+g, 1), (a+m, 1), (0, 3)):
                            h = defined_sum - e - f - g
                            i = defined_sum - a - e - m
                            l = defined_sum - i - j - k
                            if l < 0 or l > 9:
                                continue
                            for b in second_generator(defined_sum, (a+d, 1), (f+j, 1), (0,3)):
                                c = defined_sum - a - b - d
                                n = defined_sum - b - f - j
                                o = defined_sum - m - n - p
                                if o < 0 or o > 9:
                                    continue
                                sub_count += 1
                                # grid = np.array([[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]])
                                # print(flat_grid := np.reshape(grid, (16)), flat_grid @ all_sums)
                                # # print(grid)
    count += sub_count
    print("sum: {}, sub_count: {:,}".format(defined_sum, sub_count))
print("ans", count*2 - sub_count) #Don't double count the final subcount
                            
