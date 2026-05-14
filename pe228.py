import numpy as np


def regular_polygon(n):
    k_column = np.arange(1, 2*n, 2, dtype=np.float64)/n*np.pi
    #Take the cosine of the a k_column and set next to the sine of the k_column
    points = np.column_stack((np.cos(k_column), np.sin(k_column)))
    return points

def add_shapes(pointsA, pointsB):
    #Convolute the two shapes by adding together all pairs of points from the two shapes
    points = pointsA[:, np.newaxis, :] + pointsB[np.newaxis, :, :]
    #Remove the extra dimension
    return points.reshape(-1, 2)

def add_shapes_fast(circleA, circleB):
    #First re-order each set of points so that they are in a clockwise order starting from 0 radians
    thetaA = np.arctan2(circleA[:, 1], circleA[:, 0])
    thetaB = np.arctan2(circleB[:, 1], circleB[:, 0])
    circleA = circleA[np.argsort(thetaA)]
    thetaA = thetaA[np.argsort(thetaA)]
    circleB = circleB[np.argsort(thetaB)]
    thetaB = thetaB[np.argsort(thetaB)]
    for A, tA in zip(circleA, thetaA):
        

        for B in circleB:
            yield A + B

def min_x_point_index(points):
    idx = np.argmin(points[:, 0])
    return points[idx, :], idx

def max_x_point_index(points):
    idx = np.argmax(points[:, 0])
    return points[idx, :], idx

def cross2d(x, y):
    return x[..., 0] * y[..., 1] - x[..., 1] * y[..., 0]

def above_below_equals(pointA, pointB, points):
    #Check if the points are above or below the line formed by pointA and pointB
    #Return a boolean array where True means above and False means below
    line_vector = pointB - pointA
    point_vectors = points - pointA
    cross_products = cross2d(line_vector, point_vectors)
    return cross_products > 0, cross_products < 0, cross_products == 0

def distances_to_line(pointA, pointB, points):
    unit_line_vector = (pointB - pointA) / np.linalg.norm(pointB - pointA)
    distance = np.linalg.norm((pointA - points) - np.dot(pointA - points, unit_line_vector)[:, np.newaxis] * unit_line_vector, axis=-1)
    return distance

def furthest_point_from_line(pointA, pointB, points):
    #Return the point, and the index of that point
    distances = distances_to_line(pointA, pointB, points)
    idx = np.argmax(distances)
    return points[idx, :], distances[idx]

def convex_hull_recurse(pointA, pointB, points):
    if len(points) == 0:
        return []
    above_mask, below_mask, equals_mask = above_below_equals(pointA, pointB, points)
    if np.sum(above_mask) == 0:
        return []
    pointC, distanceC = furthest_point_from_line(pointA, pointB, points[above_mask])
    fill_points_AC = convex_hull_recurse(pointA, pointC, points[above_mask])
    fill_points_CB = convex_hull_recurse(pointC, pointB, points[above_mask])
    return fill_points_AC + [pointC] + fill_points_CB

def convex_hull(points):
    A, _ = min_x_point_index(points)
    B, _ = max_x_point_index(points)
    fill_points_above = convex_hull_recurse(A, B, points)
    fill_points_below = convex_hull_recurse(B, A, points)
    hull = [A] + fill_points_above + [B] + fill_points_below
    hull = np.array(hull)
    #Step around the hull and remove any points that are nearly collinear with a neighbor
    points_to_remove = []
    for i in range(len(hull)):
        prev_point = hull[i - 1]
        curr_point = hull[i]
        next_point = hull[(i + 1) % len(hull)]
        if distances_to_line(prev_point, next_point, curr_point.reshape(1, -1))[0] < 1e-10:
            points_to_remove.append(i)
    hull = np.delete(hull, points_to_remove, axis=0)
    return hull

def convolute_shapes(shapeA, shapeB):
    points = add_shapes(shapeA, shapeB)
    hull = convex_hull(points)
    return hull

if False:
    points = add_shapes(regular_polygon(30), regular_polygon(17))
    A, _ = max_x_point_index(points)
    B, _ = min_x_point_index(points)
    above_mask, below_mask, equals_mask = above_below_equals(A, B, points)
    distance_to_line = distances_to_line(A, B, points)
    print("Number of points before convex hull:", len(points))
    # points = convex_hull(points, min_x_index(points), max_x_index(points))
    # print("Number of points after convex hull:", len(points))
    hull = convolute_shapes(regular_polygon(30), regular_polygon(17))
    print("Number of points after convoluting shapes:", len(hull))

    #Plot the points, color by above, below, or on the line
    import matplotlib.pyplot as plt
    plt.scatter(points[above_mask, 0], points[above_mask, 1], color='green', label='Above')
    plt.scatter(points[below_mask, 0], points[below_mask, 1], color='red', label='Below')
    plt.scatter(points[equals_mask, 0], points[equals_mask, 1], color='blue', label='On the line')
    #Label each point with its distance to the line
    for i in range(len(points)):
        plt.text(points[i, 0], points[i, 1], f"{distance_to_line[i]:.2f}", fontsize=8)
    #Plot line between A and B
    plt.plot([A[0], B[0]], [A[1], B[1]], color='black', label='Line AB')
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    #show the plot
    if hull.shape[0] > 0:
        #mark the hull points with an orange unfilled circle
        plt.scatter(hull[:, 0], hull[:, 1], facecolors='none', edgecolors='orange', label='Convex Hull Points')
        plt.plot(hull[:, 0], hull[:, 1], color='orange', label='Convex Hull')
    plt.show()

running_total = 1
for n in range(1864, 1909 + 1):
    running_total = running_total + n - 1
print("Running total:", running_total)

print("---------------------")
n_start, n_end = 1864, 1909
hull = regular_polygon(n_start)
for n in range(n_start + 1, n_end + 1):
    hull = convolute_shapes(hull, regular_polygon(n))
    print(f"n: {n}, number of points in hull: {len(hull)}")
print("Final number of points in hull:", len(hull))

#86734 wrong