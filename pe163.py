import numpy as np

size = 36
L = size - 1
M = 2*size - 1
error = 10**-5

# Q = X*W
# W = X^-1 @ Q
# A = X*W

X = np.array([[1, 0, 0], #Bottom left corner
              [1, 2*size, 0], #Bottom right corner
              [1, size, size]]) #Top center corner
Q = np.array([  [-1, -1, L, L, L, M],
                [L, M, -1, -1, L, L],
                [L, L, L, M, -1, -1]])
W = np.linalg.inv(X) @ Q

points_yx = []
points_a = []
def calculate_point(x,y):
    a = [np.array([1,x,y]) @ W[:,z] for z in range(6)]
    a = [int(round(z)) if abs(round(z) - z) < error else None for z in a]
    points_yx.append((y,x))
    points_a.append(a)
    # print("(y: {}, x: {}) -> a_even: {}, a_odd: {}".format(y, x, a[0::2], a[1::2]))

#Corners
for y in range(size + 1):
    for x in range(y, size*2 - y + 1, 2):
        calculate_point(x,y)
#Midpoints along x axis
for y in range(size):
    for x in range(y+1, 2*size - y, 2):
        calculate_point(x,y)
#Midpoints along the other main diagonals
for j in range(0,size):
    for i in range(j, 2*size - j):
        calculate_point(i+0.5, j+0.5)
#Center points upward triangles
for j in range(0,size):
    for x in range(j+1, 2*size - j, 2):
        calculate_point(x, j + 1/3)
#Center points downwards triangles
for j in range(0, size - 1):
    for x in range(j + 2, 2*size - j - 1, 2):
        calculate_point(x, j + 2/3)
print("Num points:", len(points_a))

# Remove edges that are out of bounds
for a in points_a:
    for i in range(len(a)):
        if a[i] is None:
            continue
        elif a[i] < 0:
            a[i] = None
        elif a[i] >= 2*size - 1:
            a[i] = None

# Now compile sets for each eade of the other edges that it intersects
# Edge: (axis, value)
edge_to_edges = dict()
edge_to_points = dict()
for a, yx in zip(points_a, points_yx):
    for i in range(6):
        if a[i] is None:
            continue
        edge_i = (i, a[i])
        #Ensure that edge is in the dictionary
        if not edge_i in edge_to_edges:
                edge_to_edges[edge_i] = set()
                edge_to_points[edge_i] = set()
        #Add the point to the edge
        edge_to_points[edge_i].add(yx)
        #Iterate through the sub-edges
        for j in range(i+1,6):
            if a[j] is None:
                continue
            edge_j = (j, a[j])
            edge_to_edges[edge_i].add(edge_j)
print("num edges:", len(edge_to_edges))
# for edge in sorted(edge_to_edges.keys()):
#     print(edge, 'edges', sorted(edge_to_edges[edge]), 'points', sorted(edge_to_points[edge]))

#Now we do a combine and compare between the edges
count = 0
for edge_a in sorted(edge_to_edges.keys()):
    for edge_b in sorted(edge_to_edges[edge_a]):
        shared_point = edge_to_points[edge_a].intersection(edge_to_points[edge_b]).pop()
        shared_edges = edge_to_edges[edge_a].intersection(edge_to_edges[edge_b])
        for edge_c in shared_edges:
            if shared_point not in edge_to_points[edge_c]:
                # print("a", edge_a, "b", edge_b, "c", edge_c)
                count += 1

print("ans", count)


exit()

size = 2
L = size - 1
M = size - 2
R = 2*L - 1

#Scaling matrix W: [(b, c, d), ...] for each axis
#Point matrix X: [(1,x,y), ...] with (3) points
#Results matrix A: [(a, a, a), ...] for each axis
#Results in different format: Q [(a0, a1, a2, ...), ...] with (3) pointys


print("UPRIGHT")
#Upright triangles
upright_triangles_yx = []
upright_triangles_a = []
if size > 1:
    X = np.array([[1, 0, 0], #Bottom left corner
              [1, 2*L, 0], #Bottom right corner
              [1, L, L]]) #Top center corner
    Q = np.array([[0, 0, L, L, L, 2*L],
                [L, 2*L, 0, 0, L, L],
                [L, L, L, 2*L, 0, 0]])
    W = np.linalg.inv(X) @ Q
    for y in range(0, size):
        for x in range(y, 2*size-y, 2):
            a = [np.rint(np.array([1,x,y]) @ W[:,z]).astype(int) for z in range(6)]
            upright_triangles_yx.append((y,x))
            upright_triangles_a.append(a)
            print("(y: {}, x: {}) -> a_even: {}, a_odd: {}".format(y, x, a[0::2], a[1::2]))
elif size == 1:
    upright_triangles_yx += [(0,0)]
    upright_triangles_a += [(0, 0, 0, 0, 0, 0)]

print("DOWNWARD")
#Downward triangles
downward_triangles_yx = []
downward_triangles_a = []
if size > 2:
    X = np.array([[1, 1, 0], #Bottom left corner
                [1, R, 0], #Bottom right corner
                [1, L, M]]) #Top center corner
    Q = np.array([[0, 1, M, L, M, R],
                [M, R, 0, 1, M, L],
                [M, L, M, R, 0, 1]])
    W = np.linalg.inv(X) @ Q
    for y in range(0, size - 1):
        for x in range(y+1, 2*(size-1) - y, 2):
            a = [np.rint(np.array([1,x,y]) @ W[:,z]).astype(int) for z in range(6)]
            downward_triangles_yx.append((y,x))
            downward_triangles_a.append(a)
            print("(y: {}, x: {}) -> a_even: {}, a_odd: {}".format(y, x, a[0::2], a[1::2]))
elif size == 2:
    downward_triangles_yx += [(0, 1)]
    downward_triangles_a += [(0, 1, 0, 1, 0, 1)]


triangles_yx = upright_triangles_yx + downward_triangles_yx
triangles_a = upright_triangles_a + downward_triangles_a

if True:
    # Put together a visual representation of the triangles so that the lines can be visualized
    for axis in range(6):
        print("AXIS:", axis)
        Z = np.full((size, 2*size-1), 9)
        for (y,x), a in zip(triangles_yx, triangles_a):
            Z[y,x] = a[axis]
        print(str(Z[::-1,:]).replace("9", " "))

# Now compile sets for each eade of the other edges that it intersects
# Edge: (axis, value)
edge_to_edges = dict()
for a in triangles_a:
    for i in range(6):
        edge_i = (i, a[i])
        #Ensure that edge is in the dictionary
        if not edge_i in edge_to_edges:
                edge_to_edges[edge_i] = set()
        #Iterate through the sub-edges
        for j in range(i+1,6):
            edge_j = (j, a[j])
            edge_to_edges[edge_i].add(edge_j)
for edge in sorted(edge_to_edges.keys()):
    print(edge, sorted(edge_to_edges[edge]))


exit()

#Try again, this time by triangle interaction
t = (0,0,0)
t = (2,2,2)


size = 2

# Upright triangles
a3 = 2*size 
for a0 in range(size, -1, -1):
    a1 = a0
    for a2 in range(size, size-a0-1, -1):
        #Derive base on sum of each triangle being the same
        a4 = 2*size - (a0+a2)
        #Derive off axis
        a3 = a2*2
        a5 = 3*size - (a1+a3)
        print((a0,a2,a4), (a1,a3,a5))
        #Iterate
        a1 += 1

exit()

#Define points to derive corner relationships
C0 = (1, 0, 1, 3, 2, 3) #Point A
C1 = (0, 1, 1, 2, 1, 1) #Point B
#Generate corners
corners = []
for a0 in range(0, size+1):
    for a1 in range(-a0, size - 2*a0 + 1):
        corner = tuple([C0[i]*a0 + C1[i]*a1 for i in range(6)])
        corners.append(corner)

#Generate midpoints
midpoints = []
#axis 0 perpindicular 3
for a0 in range(size):
    for a3 in range(a0+1, 2*size-a0, 2):
        midpoint = (a0, None, a3, None, None, None)
        midpoints.append(midpoint)
#axis 2, perpendicular 5
for a2 in range(size):
    for a5 in range(a2+1, 2*size-a2, 2):
        midpoint = (None, None, a2, None, None, a5)
        midpoints.append(midpoint)
#Axis 4, perpendicular 1
for a4 in range(1, size+1):
    for a1 in range(-a4+1, a4, 2):
        midpoint = (None, a1, None, None, a4, None)
        midpoints.append(midpoint) 

for m in midpoints:
    print(m)

centers = []
#Generate centers
a5_start = 1
a1_start = 0
#Begin iteratio
for level in range(size):
    a3 = level + 1
    a5 = a5_start
    a1 = a1_start
    for a3 in range(level+1, 2*size - level):
        center = (None, a1, None, a3, None, a5)
        centers.append(center)
        if (a3+level) % 2 == 1:
            a5 += 1
        if (a3+level) % 2 == 0:
            a1 += 1
    a5_start += 2
    a1_start -= 1

vertices_long = corners + midpoints + centers

#Get lookup of verticies to edges
verticies_to_edges = []
for vertex in vertices_long:
    verticies_to_edges.append(set([(i, vertex[i]) for i in range(6) if vertex[i] is not None]))

#get lookup of edges to verticies
edges_to_verticies = dict()
for vertex_id in range(len(verticies_to_edges)):
    for edge in verticies_to_edges[vertex_id]:
        if edge in edges_to_verticies:
            edges_to_verticies[edge].append(vertex_id)
        else:
            edges_to_verticies[edge] = [vertex_id]
for edge in edges_to_verticies:
    for vertex in edges_to_verticies[edge]:
        print("edge: {}, vertex: {}, long: {}".format(edge, vertex, vertices_long[vertex]))

def greater_than(edge0, edge1):
    # Return True if edge 0 is greater than edge 1
    if edge0[0] > edge1[0]:
        return True
    elif edge0[0] < edge1[0]:
        return False
    else: #Same
        return edge0[1] > edge1[1]

#Calculate a lookup of edges to edges
edges_to_edges = dict()
for edge0 in edges_to_verticies:
    if len(edges_to_verticies[edge0]) <= 1:
        continue
    for vertex in edges_to_verticies[edge0]:
        for edge1 in verticies_to_edges[vertex]:
            if len(edges_to_verticies[edge1]) <= 1:
                continue
            if greater_than(edge1, edge0):
                if edge0 in edges_to_edges:
                    edges_to_edges[edge0].add(edge1)
                else:
                    edges_to_edges[edge0] = {edge1}

for edge in edges_to_edges:
    print(edge, edges_to_edges[edge])
exit()

#Calculate the count of triangles
count = 0
for a in range(len(verticies_to_edges)):
    for edge_a in verticies_to_edges[a]:
        print("a: {}, long: {}, edge_a: {}".format(a, vertices_long[a], edge_a))
        for b in edges_to_verticies[edge_a]:
            if b <= a:
                continue
            for edge_b in verticies_to_edges[b]:
                if edge_b == edge_a:
                    continue
                print("    b: {}, long: {}, edge_b: {}".format(b, vertices_long[b], edge_b))
                for c in edges_to_verticies[edge_b]:
                    if c > b:
                        print("        c: {}, long: {}".format(c, vertices_long[c]))
                        count += 1
print("ans", count)

exit()

for edge in edges_to_verticies:
    print("edge: {}".format(edge))
    for x in edges_to_verticies[edge]:
        print("    point: {}, long: {}".format(x, vertices_long[x]))