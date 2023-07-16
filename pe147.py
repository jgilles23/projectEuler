import numpy as np

class Expandable:
    def __init__(self, length_x, length_y, expansion_axis=0):
        self.xy = (length_x, length_y)
        self.set_expansion_axis(expansion_axis)

    def set_expansion_axis(self, axis):
        self.axis = axis
        self.off_axis = (axis + 1) % 2
    
    def get_axis_length(self):
        return self.xy[self.axis]
    
    def get_off_axis_length(self):
        return self.xy[self.off_axis]
    
    def increment_length(self):
        if self.axis == 0:
            self.xy = (self.xy[0] + 1, self.xy[1])
        else:
            self.xy = (self.xy[0], self.xy[1] + 1)
    
    def manhattan_length(self):
        return sum(self.xy)

class Rectangle(Expandable):
    def __init__(self, length_x, length_y, initial_count, expansion_axis=0):
        super().__init__(length_x, length_y, expansion_axis)
        self.count = initial_count
    
    def __repr__(self):
        return "[{}, {}]:{}".format(*self.xy, self.count)

    def copy(self):
        # Return a copy of self
        return Rectangle(self.xy[0], self.xy[1], self.count, self.axis)
    
    def multiply_into(self, off_axis_length):
        #Specify the height of the expansion area
        self.count += off_axis_length - self.get_off_axis_length() + 1
    
    def increase_length_into(self, off_axis_length):
        # Return a new rectanlge that is longer than self
        new_rectangle = Rectangle(*self.xy, off_axis_length - self.get_off_axis_length() + 1, self.axis)
        new_rectangle.increment_length()
        return new_rectangle

class Diamond(Expandable):
    def __init__(self, length_x_prime, length_y_prime, initial_count, expansion_axis = 0):
        # Uses x and y to mean x' and y' to allow class re-use
        super().__init__(length_x_prime, length_y_prime, expansion_axis)
        self.count = initial_count
    
    def __repr__(self):
        return "<{}, {}>:{}".format(*self.xy, self.count)
    
    def copy(self):
        return Diamond(*self.xy, self.count, self.axis)
    
    def multiply_into(self, added_squares):
        # Increase count by the manhattan length
        self.count += added_squares - self.manhattan_length() + 2

class Grid(Expandable):
    def __init__(self, length_x=1, length_y=1, rectangles=[Rectangle(1,1,1)], diamonds = [], expansion_axis=0):
        super().__init__(length_x, length_y)
        self.rectangles = rectangles
        self.diamonds = diamonds
    
    def __repr__(self):
        s = "Grid: ({}, {}), Count: {}\n".format(*self.xy, self.sum())
        s += "    Rectangles: {}\n".format(self.rectangles)
        s += "    Diamonds:   {}".format(self.diamonds)
        return s
    
    def copy(self):
        grid_copy = Grid(*self.xy, 
                         [rectangle.copy() for rectangle in self.rectangles], 
                         [diamond.copy() for diamond in self.diamonds],
                         self.axis)
        return grid_copy
    
    def expand(self, axis):
        #Expand the grid, returning a new copy of the grid
        grid = self.copy()
        grid.set_expansion_axis(axis)
        grid.increment_length()
        #Add rectangles
        rectangles_new = []
        for rectangle in grid.rectangles:
            rectangle.set_expansion_axis(axis) # Expand on specificed axis
            #Longest rectangles grow into the new space
            if rectangle.get_axis_length() == grid.get_axis_length() - 1:
                rectangles_new.append(rectangle.increase_length_into(grid.get_off_axis_length()))
            #Rectanges increase count to take up the new space
            rectangle.multiply_into(grid.get_off_axis_length())
        grid.rectangles.extend(rectangles_new)
        return grid
        # Expand only diamonds
        for diamond in grid.diamonds:
            diamond.set_expansion_axis(axis)
            diamond.multiply_into(2*grid.get_off_axis_length() - 1)
        # Add new diamond lengths
        if grid.xy[0] == grid.xy[1]:
            long_diagonal = 2*min(*grid.xy)-2
        else:
            long_diagonal = 2*min(*grid.xy) - 1
        if abs(grid.xy[0] - grid.xy[1]) == 1:
            if grid.xy == (1,2) or grid.xy == (2,1):
                print("2x1 near square", long_diagonal)
                grid.diamonds.append(Diamond(1,1,1))
            else:
                print("near square", long_diagonal)
                #Add a long in both directions
                grid.diamonds.append(Diamond(long_diagonal, 1, 1))
                grid.diamonds.append(Diamond(1, long_diagonal, 1))
        elif grid.xy[0] == grid.xy[1]:
            if grid.xy == (2,2):
                print("2x2 square", long_diagonal)
                grid.diamonds.append(Diamond(1,2,2))
                grid.diamonds.append(Diamond(2,1,2))
                grid.diamonds.append(Diamond(2,2,1))
            else:
                print("square", long_diagonal)
                # Square grid, iterate through a bunch of new shapes
                x_length = 1
                y_length = long_diagonal
                while y_length > 0:
                    grid.diamonds.append(Diamond(x_length, y_length, 2))
                    grid.diamonds.append(Diamond(x_length + 1, y_length, 1))
                    x_length += 2
                    y_length -= 2
                    # To add new diamonds
                    # When increading the dimension such that the new dimension is (a, a+1) or the reverse, add 1 long diagonal in each direction
                    # when increasing to a square (a, a-1) -> (a,a)
                    #   1xlong (2), 2xlong (1)
                    #   3xlong-2 (2), 4xlong-2 (1)
                    #   5xlong-4 (2), 6xlong-4 (1)
        else:
            print("not square", long_diagonal)
            # If grid is not square or longer on one side than the other by 1 there are no new rectangle shapes
            pass

        print(grid)
        return grid
    
    def sum(self):
        # Sum of all of the sub-grid counts
        s = 0
        for rectangle in self.rectangles:
            s += rectangle.count
        return s
        





# grid = Grid()
# print(grid)
# grid = grid.expand(0)
# grid = grid.expand(1)
# grid = grid.expand(0)
# grid = grid.expand(0)
# grid = grid.expand(1)
# grid = grid.expand(1)

def diamond_grid(length_x, length_y):
    if length_y > length_x:
        rotate_flag = True
        length_x, length_y = (length_y, length_x)
    else:
        rotate_flag = False
    length_prime = length_x + length_y
    print(length_prime)
    A = np.full((length_prime, length_prime), 0)
    # First part
    first_line_y = length_y
    x = 0
    for width in range(length_y):
        A[first_line_y-width:first_line_y+width, x] = 1
        x += 1
    #middle part; maintain width
    width = 2*width + 1
    for y in range(1, abs(length_x - length_y) + 1):
        print("y", y, "x", x)
        A[y:y+width, x] = 1
        x += 1
    second_line_y = length_x
    for width in range(length_y-1, -1, -1):
        A[second_line_y-width: second_line_y+width, x] = 1
        x += 1
    if rotate_flag:
        A = np.rot90(A)
    # Reduce the size of A
    A = A[1:-1, 1:-1]
    print(A)
    return A

def count_diamonds(grid, length_x, length_y):
    if length_x == 1 and length_y == 1:
        return np.sum(grid)
    count = 0
    for x in range(0, grid.shape[1] - length_x + 1):
        for y in range(0, grid.shape[0] - length_y + 1):
            if np.all(grid[y:y+length_y, x:x+length_x]):
                count += 1
    return count

def count_all_diamonds(grid):
    count = 0
    for length_y in range(1,grid.shape[0] + 1):
        for length_x in range(length_y, grid.shape[1] + 1):
            c = count_diamonds(grid, length_x, length_y)
            if length_x == length_y:
                count += c
            else:
                count += 2*c
    return count

def count_diagonal_rectangles(x_length, y_length, print_flag=False):
    #Get the shared with with subsequent columns as a width
    # x_length >= y_length
    if y_length > x_length:
        raise Exception("x must be >= y")
    # Assumne 3 regions of the graph:
    #iff y = 1:
        #special case
    if y_length == 1:
        return x_length - 1
    # start: [0] H=2, D=0; S=0, E=2
    columns = [0]
    starts = [0]
    ends = [-2]
    # a: increacing height of columns [1, y-2] H+2, D+1; S+1, E-1
    for c in range(1, y_length-2+1):
        columns.append(c)
        starts.append(starts[-1] + 1)
        ends.append(ends[-1] - 1)
    # iff x==y: 
        # ac_transition:  [y-1] H+0, D+0; S+0, E+0
    if x_length == y_length:
        columns.append(y_length-1)
        starts.append(starts[-1] + 0)
        ends.append(ends[-1] + 0)
    # else: 
    else:
        # ab_transition: [y-1] H+1, D+0; S+0, E-1
        columns.append(y_length-1)
        starts.append(starts[-1] + 0)
        ends.append(ends[-1] - 1)
        # b: constant height of columns [y, x-2] H+0, D-1; S-1, E-1
        for c in range(y_length, x_length-2+1):
            columns.append(c)
            starts.append(starts[-1] - 1)
            ends.append(ends[-1] - 1)
        # bc_transition: [x-1] H-1, D-1; S-1, E+0
        columns.append(x_length-1)
        starts.append(starts[-1] - 1)
        ends.append(ends[-1] + 0)
    # c: decreasing height of columns [x, x+y-3] H-2, D-1; S-1, E+1
    for c in range(x_length, x_length+y_length-3+1):
            columns.append(c)
            starts.append(starts[-1] - 1)
            ends.append(ends[-1] + 1)
    # Need to translate the starts and ends into a usable format
    max_start = max(starts)
    starts = [max_start - z for z in starts]
    ends = [max_start - z for z in ends]
    if print_flag:
        print("Columns:", columns)
        print("Starts :", starts)
        print("Ends   :", ends)
        #Make into a visual matrix
        A = np.full((max(ends), max(columns)+1), 0)
        for c, start, end in zip(columns, starts, ends):
            A[start:end, c] = 1
        print(A)
    # Part 2 -- turn the diagonals into rectangles
    # Schema for Iteration:
    # Column
        # Width <= max_height and Width <= remaining columns
            #Height <= max_height
    rectangle_count = 0
    for c in range(len(starts)):
        # height >= width
        for width in range(1, len(starts) - c + 1):
            start = max(starts[c:c+width])
            end = min(ends[c:c+width])
            max_height = end - start
            if (max_height < width):
                break
            # Should be able to lookup the width by the height in a table (if it exists)
            # rectangle_count += max_height - width + 1
            # for height in range(width+1, max_height+1):
            #     rectangle_count += 2*(max_height - height + 1)
                # if print_flag: print("Column: {}, (width: {}, height: {}), count: {}, max_height: {}".format(c, width, height, count, max_height))
            # This can be wrapped into a function, does not need to be a loop (I think)
            rectangle_count += (max_height - width + 1)**2
            
    if print_flag: print("Rectangle count:", rectangle_count)
    return rectangle_count

def count_normal_rectangles(x_length, y_length):
    # Directly adopt the diagonal counting method, but with removed complexity becvause the max height is always the same
    rectangle_count = ((y_length + 1)*y_length//2) * ((x_length + 1)*x_length//2)
    return rectangle_count

# Go for the answer
x_max = 47
y_max = 43
total = 0
for x_length in range(1, x_max+1):
    for y_length in range(1, min(x_length, y_max)+1):
        rectangles = count_normal_rectangles(x_length, y_length)
        diamonds = count_diagonal_rectangles(x_length, y_length)
        both = rectangles + diamonds
        total += both
        # print((x_length, y_length), "rectangles: {:,}, diamonds: {:,}, both: {:,}".format(rectangles, diamonds, both))
        if x_length != y_length and x_length <= y_max:
            # Double the count to account for the transpose of this shape
            # print((y_length, x_length), "double count")
            total += both
print("ans", total)

# TESTS

# length_x = 20
# length_y = 10
# G = diamond_grid(length_x, length_y)
# print("brute force diagonal", count_all_diamonds(G))
# print("smart diagonal      ", count_diagonal_rectangles(length_x,length_y, print_flag=False))

# grid = Grid()
# for _ in range(1, length_x):
#     grid = grid.expand(0)
# for _ in range(1, length_y):
#     grid = grid.expand(1)
# print("recursive normal:", grid.sum())
# print("smart normal    :", count_normal_rectangles(length_x, length_y))

# To add new diamonds
# When increading the dimension such that the new dimension is (a, a+1) or the reverse, add 1 long diagonal in each direction
# when increasing to a square (a, a-1) -> (a,a)
#   1xlong (2), 2xlong (1)
#   3xlong-2 (2), 4xlong-2 (1)
#   5xlong-4 (2), 6xlong-4 (1)

# def LD(x,y):
#     long_diagonal = min(x,y)*2 - 2
#     print((x,y), long_diagonal)

# LD(1,1)
# LD(3,72)