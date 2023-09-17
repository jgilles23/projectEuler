N = 10**6

count = 0
hole_perimeter = 1
square = 8
while square <= N:
    width = 0
    while square <= N:
        count += 1
        width += 2
        square += 4*(hole_perimeter + width) + 4
    hole_perimeter += 1
    square = 4*hole_perimeter + 4

print(count)