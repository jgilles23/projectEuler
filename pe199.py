import math

def calculate_fourth_circle_radius(a,b,c):
    #Calcualte the radius of the fourth circle given radius a,b,c
    #If one value is negative, that incloses the other circles
    #Resuls in the smallest absolute value answer
    left_side = 1/a + 1/b + 1/c
    right_side = 2*math.sqrt(1/(a*b) + 1/(a*c) + 1/(b*c))
    b_positive = 1/(left_side + right_side)
    b_negative = 1/(left_side - right_side)
    if abs(b_positive) > abs(b_negative):
        return b_negative, b_positive
    else:
        return b_positive, b_negative

depth_limit = 10
def recursive_split(a, b, c, depth=1):
    d,_ = calculate_fourth_circle_radius(a,b,c)
    area_taken = math.pi*d**2
    if depth >= depth_limit:
        return area_taken
    area_taken += recursive_split(a,b,d, depth+1)
    area_taken += recursive_split(a,c,d, depth + 1)
    area_taken += recursive_split(b,c,d, depth + 1)
    return area_taken

q = 1 + 2/math.sqrt(3) #radius of the outer circle
area_total = math.pi*q**2
area_taken = 3*math.pi*1**2
area_taken += 3*recursive_split(-q,1,1)
area_taken += recursive_split(1,1,1)
print(area_taken, area_total, area_taken/area_total, 1-area_taken/area_total)
print("ans", round(1-area_taken/area_total,8))
