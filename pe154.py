import numpy as np
import math
# Naive build of pascal triangle

def make_nth_triangle_row(n, modulus):
    row = np.full(n+1,0, dtype=np.int64)
    row[0] = 1
    for k in range(1,n+1):
        row[k] = (row[k-1]*(n+1-k)//k)
    return row

def make_nth_triangle_row_addition_method(N, modulus):
    row = np.full(n+1,0, dtype=np.int64)
    row[0] = 1
    for k in range(1,n+1):
        row[k] = (row[k-1]*(n+1-k)//k)
    return row

def final(generator):
    for i, x in enumerate(generator):
        if i%10**4 == 0:
            print("step: {:,}".format(i))
        pass
    return x

def yield_successive_pascal_rows(N, modulus, mode = 2):
    # Yeild successive pyramid rows for the Nth level of the pyramid
    # Mode = 2, yield rows of pascals triangle
    # Mode = 3, yield rows of pascals pyramid
    # Mode = 4, yield a COUNT (int) of the 
    if mode != 2: 
        multiplier = final(yield_successive_pascal_rows(N, modulus, mode=2))
    triangle_row = np.full(N+1, 0, dtype=np.int64)
    triangle_row[0] = 1
    if mode == 2:
        yield triangle_row[0:1]
    else: 
        yield triangle_row[0:1]*multiplier[0]
    for n in range(1, N+1):
        triangle_row[1:n] = (triangle_row[:n-1] + triangle_row[1:n])%modulus
        triangle_row[n] = 1
        if mode == 2:
            yield triangle_row[:n+1]
        elif mode == 3:
            yield (triangle_row[:n+1]*multiplier[n])%modulus


class Triangle:

    def __init__(self, N, modulus):
        # Prepare a triangle that will have up to N+1 rows
        # Keep results modulus the defined modulus
        # Only a single row will be held at a time, they can yield as required
        self.N = N
        self.modulus = modulus
        # Establish the half row data structure
        self.row_number = 0
        self.half_row = np.full(self.N//2 + 1, 0, dtype=np.int64)
        self.half_row[0] = 1
    
    def reset(self):
        #Reset the triangle to the initial state, so that things can be re-calculated or printed
        print("RESETING TRIANGLE")
        self.row_number = 0
        self.half_row[:] = 0
        self.half_row[0] = 1

    def half_length(self):
        # Return the last index used of the half row
        return (self.row_number)//2 + 1
    
    def calc_next_row(self):
        # Calculate the next row of the triangle based on the previous row
        stop = self.half_length() - 1
        if self.row_number % 2 == 1:
            self.half_row[stop+1] = (2*self.half_row[stop])%self.modulus
        self.half_row[1:stop+1] = (self.half_row[:stop] + self.half_row[1:stop+1])%self.modulus
        #Increase the row number
        self.row_number += 1
    
    def get_row(self, mirror_flag=False):
        # Return the full row e.g. the mirrored half roow or just the half row
        # Return the half row
        if mirror_flag == False:
            return self.half_row[:self.half_length()]
        # Return the mirrored version
        if self.row_number % 2 == 0:
            return np.concatenate((self.half_row[:self.half_length()], self.half_row[:self.half_length()-1][::-1]))
        else:
            return np.concatenate((self.half_row[:self.half_length()], self.half_row[:self.half_length()][::-1]))

    def yield_rows(self, mirror_flag=False, progress_flag = True):
        # Check if reset needed
        if self.row_number >= self.N:
            self.reset()
        # Yield the sucessive rows up to N
        yield self.get_row(mirror_flag)
        for n in range(1, self.N+1):
            # Print progress
            if n % 10**4 == 0 and progress_flag:
                print("progress: {:,} of {:,} | {:.0%}".format(n, self.N, n/self.N))
            self.calc_next_row()
            yield self.get_row(mirror_flag)
    
    def get_last_row(self, mirror_flag=False, progress_flag=True):
        # Return the last row, calculate if required
        if self.row_number < self.N:
            for row in self.yield_rows(False): #Never mirror, as these values are not used for anything
                pass
        # Return the last row
        return self.get_row(mirror_flag=mirror_flag)

    def print_full(self, mirror_flag = True):
        print("Triangle with N: {:,}, modulus: {:.0%}".format(self.N, self.modulus))
        for row in self.yield_rows(mirror_flag, progress_flag=False):
            print("   ", row)
    
    def get_value(self, k):
        #get value from current row with index k
        if k < self.half_length():
            return self.half_row[k]
        else:
            if self.row_number % 2 == 0:
                return self.half_row[2*self.half_length() - 2 - k]
            else:
                return self.half_row[2*self.half_length() - 1 - k]
                

class Pyramid(Triangle):

    def __init__(self, N, modulus):
        super().__init__(N, modulus)
        # Define multiplier to be the values along the bottom row of pascals triangle
        self.triangle_end = Triangle(N, modulus)
        self.triangle_end.get_last_row()
        self.triangle = Triangle(N,modulus)
        # The first half row just equals 1
    
    def reset(self):
        super().reset()
        self.triangle.reset()
    
    def calc_next_row(self):
        self.row_number += 1
        self.triangle.calc_next_row()
        self.half_row = self.triangle.get_row()*self.triangle_end.get_value(self.row_number) % self.modulus


class Counting_Pyramid(Triangle):
    def __init__(self, N, modulus):
        super().__init__(N, modulus)
        # Count only the items in the pyramid that are congruent to 0
        self.triangle_end = Triangle(N, modulus)
        self.triangle_end.get_last_row()
        # Create a count
        self.count = 0
    
    def get_remainder(self):
        # for the value in triangle end, get the remainder
        a = self.triangle_end.get_value(self.row_number)
        if a == 0:
            return 1
        else:
            return self.modulus//math.gcd(a,self.modulus)
    
    def calc_next_row(self):
        super().calc_next_row()
        # Count only the items that are congruent to 0 modulo the remainder
        r = self.get_remainder()
        previous_count = self.count
        self.count += 2*sum(self.get_row() % r == 0)
        # Correct for even numbered rows double counting the center
        if self.row_number % 2 == 0:
            self.count -= (self.get_row()[-1] % r == 0)
        # print(self.count - previous_count, end=", ")
        # if self.count - previous_count > 0:
        #     pass


def modular_division(numerator, denominator, modulus):
    g = math.gcd(denominator, modulus)
    if g == 1 and denominator != 1:
        denominator_inverse = pow(denominator, -1, modulus)
        return (numerator*denominator_inverse) % modulus
    return numerator//denominator

N = 2*10**5
M = 10**12

# pyramid = Pyramid(N,M)
# count_by_row = [sum(pyramid.get_row(mirror_flag=True)%M == 0) for _ in pyramid.yield_rows()]
# # pyramid.print_full()
# print("count", sum(count_by_row))
# # print(count_by_row)

pyramid_counting = Counting_Pyramid(N,M)
pyramid_counting.get_last_row()
ans = pyramid_counting.count
# print()
print("ans  ", ans)

#134777591 -- incorrect

exit()

def get_from_pyramid(pyramid, level, row, column):
    # Return item from the pyramid, use 0 for out of bounds items
    if row < 0 or row >= len(pyramid[level]):
        return 0
    if column < 0 or column >= len(pyramid[level][row]):
        return 0
    return pyramid[level][row][column]

def pyramid_print(pyramid, level=-1):
    #level -1 is print all levels, otherwise print specificed level
    if level < 0:
        level_range = range(0, len(pyramid))
    else:
        level_range = [level]
    for L in level_range:
        print("Level: {}".format(L))
        for row in pyramid[L]:
            print("   ", row)


#Setup the pyramid
pyramid = [[[1]]] #Level -> Row -> Column
for n in range(1, N+1):
    pyramid.append([])
    r = 0
    column_max = n + 1
    while column_max > 0:
        row = []
        for c in range(column_max):
            row.append(get_from_pyramid(pyramid, n-1, r-1, c) + 
                       get_from_pyramid(pyramid, n-1, r, c-1) + 
                       get_from_pyramid(pyramid, n-1, r, c))
        pyramid[n].append(row)
        r += 1
        column_max -= 1

pyramid_print(pyramid, N)


exit()

count = 0

print("Level:", N)
for row in yield_successive_pascal_rows(N, M, mode=2):
    pass
print("   ", row[:5])


triangle = Triangle(N,M)
q = triangle.get_last_row()
print(q[:5])
pass

exit()

# print("Level:", N)
# for row in yield_successive_pascal_rows(N, 64, mode=3):
#     print("   ", row)

# print(make_nth_triangle_row(N, M))



# print(make_nth_triangle_row(N))
print("Level:", N)
for row in yield_successive_pyramid_rows(N, M):
    print("   ", row)


def make_triangle(N):
    # Make a pascals triangle to the Nth row
    triangle = np.full((N+1, N+1), 0)
    triangle[0,0] = 1
    for n in range(1, N+1):
        triangle[n, 1:n] = triangle[n-1, :n-1] + triangle[n-1, 1:n]
        triangle[n,0] = 1
        triangle[n,n] = 1
    return triangle

def make_nth_pyramid_layer(n):
    # Make the nth layer of the pyramid
    pyramid = make_triangle(n)
    pyramid *= pyramid[-1, :][:, np.newaxis]
    return pyramid

# print(make_triangle(N))
print(make_nth_pyramid_layer(N))

exit()


def get_from_pyramid(pyramid, level, row, column):
    # Return item from the pyramid, use 0 for out of bounds items
    if row < 0 or row >= len(pyramid[level]):
        return 0
    if column < 0 or column >= len(pyramid[level][row]):
        return 0
    return pyramid[level][row][column]

def pyramid_print(pyramid, level=-1):
    #level -1 is print all levels, otherwise print specificed level
    if level < 0:
        level_range = range(0, len(pyramid))
    else:
        level_range = [level]
    for L in level_range:
        print("Level: {}".format(L))
        for row in pyramid[L]:
            print("   ", row)


#Setup the pyramid
pyramid = [[[1]]] #Level -> Row -> Column
for n in range(1, N+1):
    pyramid.append([])
    r = 0
    column_max = n + 1
    while column_max > 0:
        row = []
        for c in range(column_max):
            row.append(get_from_pyramid(pyramid, n-1, r-1, c) + 
                       get_from_pyramid(pyramid, n-1, r, c-1) + 
                       get_from_pyramid(pyramid, n-1, r, c))
        pyramid[n].append(row)
        r += 1
        column_max -= 1

pyramid_print(pyramid, N)