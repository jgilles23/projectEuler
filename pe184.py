# %%
import math
import functools

def point_to_tripple(x,y):
    # Turn a point into a tripple of the following format
    # (Quadrant, rise y, run x)
    # Quadrant: 0 +x +y, 1 +x - y, 2 -x -y, 3 +x, -y
    if x > 0:
        if y > 0:
            q = 1 #0
        elif y == 0:
            return (2, 0, 1) #right
        elif y < 0:
            q = 3 #1
    elif x == 0:
        if y > 0:
            return (0, 1, 0) #up
        elif y == 0:
            return (-1, 0, 0) # The orgin
        elif y < 0:
            return (4, 1, 0) #down
    elif x < 0:
        if y > 0:
            q = 7 #3
        elif y == 0:
            return (6, 0, 1)#left
        elif y < 0:
            q = 5 #2
    g = math.gcd(abs(x),abs(y))
    return (q, abs(y)//g, abs(x)//g)

def compare(tripple0, tripple1):
    #Return -1, 0, 1 for less, equal, greater
    q0, rise0, run0 = tripple0[:3]
    q1, rise1, run1 = tripple1[:3]
    if q0 < q1:
        return -1
    elif q0 > q1:
        return 1
    else:
        #They are in the same quadrant
        if q0%2 == 0:
            # On the same horizontal or vertical line
            return 0
        w = run0*rise1 - run1*rise0
        if w < 0:
            r = -1
        elif w > 0:
            r = 1
        else:
            r = 0
        if q0 == 1 or q0 == 5:
            return r
        else:
            return -r


# points = [(0, 7), (0, 8), (1, 5), (2,2), (5, 1), (10, 0), (6, -2), (3, -3), (1, -7), (0, -8), (0, -3), (6, -6),
#           (-1, -7), (-2, -14), (-5,-5), (-10, -1), (-20, 0), (-5, 0), (-10, 1), (-6, 6), (-12, 12), (-1, 7), (0, 3)]
# points_sorted = sorted(points[::-1], key=functools.cmp_to_key(lambda a, b: compare(point_to_tripple(*a), point_to_tripple(*b))))
# print(points_sorted)
# print(compare(point_to_tripple(5,-1), point_to_tripple(2,-2)))
        

r = 105
count_by_angles_dict = dict()
for x in range(-r+1, r):
    for y in range(-r+1, r):
        # Check if INSIDE the defined radius
        if x**2 + y**2 >= r**2:
            continue
        tripple = point_to_tripple(x, y)
        if tripple in count_by_angles_dict:
            count_by_angles_dict[tripple] += 1
        else:
            count_by_angles_dict[tripple] = 1
count_by_angles_dict.pop((-1,0,0)) #Remove the origin
# print(count_by_angles_dict)
count_by_angles = [key + (count_by_angles_dict[key],) for key in count_by_angles_dict]
count_by_angles.sort(key=functools.cmp_to_key(compare))
# print(count_by_angles)

#Create separate sorted angles & sorted counts
sorted_angles = [X[:3] for X in count_by_angles]
sorted_counts = [X[3] for X in count_by_angles]
sorted_gammas = [0]*len(sorted_counts)
for i in range(len(sorted_gammas) - 2, -1, -1):
    sorted_gammas[i] = sorted_counts[i+1] + sorted_gammas[i+1]

#Use better terms
points = count_by_angles_dict
gammas = {sorted_angles[i]:sorted_gammas[i] for i in range(len(sorted_angles))}

def flip(tripple):
    return (tripple[0] + 4 % 8, ) + tripple[1:]

#Do a slow count of the total number of triangles
triangles = 0
for ai, a in enumerate(sorted_angles):
    print(a)
    if a == (4,1,0):
        #Until the down ray
        break
    for bi, b in enumerate(sorted_angles[ai+1:]):
        if b == (4,1,0):
            #Until the down ray
            break
        adder = points[a]*points[b]*(gammas[flip(a)] - gammas[flip(b)] - points[flip(b)])
        # print(a,b,adder)
        triangles += adder
    for b in sorted_angles[ai + bi + 1:]:
        if b == flip(a):
            #Never get more than 180 deg away from a
            break
        adder = points[a]*points[b]*gammas[flip(a)]
        # print(a,b,adder)
        triangles += adder
print("ans", triangles)




# %%
