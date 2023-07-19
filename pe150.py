import numpy as np

rows = 1000
N = (rows + 1)*rows//2
print("N:", N)

#Linear Congruential Generator
S = np.full(N+1, 0)
t = 0
for k in range(1, N+1):
    t = (615949*t + 797807)%2**20
    S[k] = t - 2**19

print("Test:", S[1], S[1]==273519)
print("Test:", S[2], S[2]==-153582)
print("Test:", S[3], S[3]==450905)

# rows = 6
# S = [0,15,-14,-7,20,-13,-5,-3,8,23,-26,1,-4,-5,-18,5,-16,31,2,9,28,3]

# Makse into a square
square = np.full((rows, rows), 0)
i = 1
for row in range(rows):
    square[row, 0:row+1] = S[i: i+row+1]
    i += row+1
print("Square")
print(square)

row_sum = square.cumsum(1)
print("row_sum")
print(row_sum)

column_row_sum = row_sum.cumsum(0)
print("column_row_sum")
print(column_row_sum)

diagonal_row_sum = row_sum.copy()
for row in range(1, diagonal_row_sum.shape[0]):
    diagonal_row_sum[row, 1:] += diagonal_row_sum[row-1, :-1]
print("diagonal_row_sum")
print(diagonal_row_sum)

#Now iterate through the smallest sums
min_sum = 0
for row in range(rows):
    if row%100==0: print("row: {:,}".format(row))
    for column in range(0, row+1):
        #Diagonal cumulative sum minus column cumulative sum (both cumulative sums across the row cumulative sum)
        #Save only the relevant section
        diagonal_minus_column = diagonal_row_sum.diagonal(column-row)[column:].copy()
        if column != 0:
            diagonal_minus_column -= column_row_sum[row:, column-1]
        #Shift out the pivot point & add on the value of the origional pivor point
        diagonal_minus_column += square[row, column] - diagonal_minus_column[0]
        m = np.min(diagonal_minus_column)
        if m < min_sum:
            min_sum = m
            print("New min: {:,}".format(min_sum))
print("ans", min_sum)
