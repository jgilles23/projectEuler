import numpy as np
# import sympy

# x00, x01, y00, y01 = sympy.symbols("x00 x01 y00 y01", integer=True)
# x10, x11, y10, y11 = sympy.symbols("x10 x11 y10 y11", integer=True)
# m0 = (y01 - y00)/(x01 - x00)
# b0 = m0*x01 + y01
# m1 = (y11 - y10)/(x11 - x10)
# b1 = m1*x11 + y11
# #Solve x and y
# d = (m1 - m0)
# x = sympy.simplify(1/d*(-1*b0 - m1*b1))
# y = sympy.simplify(1/d*(1*b0 + m0*b1))
# x_num, x_den = sympy.fraction(x)
# x_num = sympy.utilities.lambdify(x, x_num,'numpy')
# y_num, y_den = sympy.fraction(y)

# print(sympy.simplify(x))
# print(sympy.simplify(y))

# def eval_points(L0, L1):
#     subs = {sym:value for sym,value in zip([x00, x01, y00, y01, x10, x11, y10, y11], L0 + L1)}
#     print(subs)
#     X = (x_num.evalf(subs=subs), x_den.evalf(subs=subs))
#     Y = (y_num.evalf(subs=subs), y_den.evalf(subs=subs))
#     print("here",X,Y)
#     return (X,Y)


# L1 = [27, 44, 12, 32]
# L2 = [np.array(x) for x in [46, 53, 17, 62]]
# L3 = [np.array(x) for x in [46, 70, 22, 40]]
# L4 = [5, 5, 22, 40]

# eval_points(L2,L3)

# exit()

error = 10**-8

intersection_points = set()

def intersect_test(L1, L2):
    if L1.shape != (4,) and L2.shape[1] != 4:
        raise "Incorrect Shape for Input"
    #L1 (4) = np.array [x, y, x, y]
    #L2 (N x 4) = np.array [[x, y, x, y]], [[x, y, x, y], ...]
    x0, y0, x1, y1 = L1
    X0, Y0, X1, Y1 = L2.transpose()
    #Test if a point of L1 is on any L2
    point_shared_a = np.logical_or((y0 - Y0)*(X1 - X0) == (Y1 - Y0)*(x0 - X0), (y1 - Y0)*(X1 - X0) == (Y1 - Y0)*(x1 - X0))
    point_shared_b = np.logical_or((Y0 - y0)*(x1 - x0) == (y1 - y0)*(X0 - x0), (Y1 - y0)*(x1 - x0) == (y1 - y0)*(X1 - x0))
    point_shared = np.logical_or(point_shared_a, point_shared_b)
    #Check for same slope
    slope_shared = (y1 - y0)*(X1 - X0) == (x1 - x0)*(Y1 - Y0)
    #Combine trivial tests
    non_intersecting = np.logical_not(np.logical_or(point_shared, slope_shared))
    #Reduce L2 into only the relevant points
    # print("removed", np.sum(np.logical_not(non_intersecting)))
    L3 = L2[non_intersecting, :]
    X0, Y0, X1, Y1 = L3.transpose()
    #Compile the A matrix: [[]]
    A = np.full((L3.shape[0], 2, 2), 0)
    A[:, 0, 0] = x1 - x0
    A[:, 1, 0] = y1 - y0
    A[:, 0, 1] = X0 - X1
    A[:, 1, 1] = Y0 - Y1
    #Compile the b matrix
    b = np.full((L3.shape[0], 2, 1), 0)
    b[:, 0, 0] = X0 - x0
    b[:, 1, 0] = Y0 - y0
    #Compute A @ x = b; where x = [s,t]; x: (N,2,1)
    x = np.linalg.inv(A) @ b
    #Test the conformance of x to the bounding box
    in_box_st = np.logical_and( x > 0, x < 1)
    in_box = np.logical_and(in_box_st[:, 0, 0], in_box_st[:, 1, 0])
    #Add unique points
    s_in_box = x[in_box, 0, 0]
    xy_answers = np.full((s_in_box.shape[0], 2), 0)
    xy_answers[:, 0] = (1 - s_in_box)*x0 + s_in_box*x1
    xy_answers[:, 1] = (1 - s_in_box)*y0 + s_in_box*y1
    xy_answers = np.round(xy_answers, 10)
    for a in xy_answers:
        intersection_points.add(tuple(a))
    #Increate the count
    count = np.sum(in_box)
    # if np.any(np.logical_and(np.abs(x) < error, np.abs(x - 1) < error)):
    #     raise "Too close to call."
    return count

def bbs_factory():
    sn = 290797
    while True:
        sn = (sn * sn) % 50515093
        tn = sn % 500
        yield tn

L1 = np.array([27, 44, 12, 32])
L2 = np.array([46, 53, 17, 62])
L3 = np.array([46, 70, 22, 40])
L4 = np.array([11, 29, 22, 40])
L5 = np.array([12, 30, 400, 421]) #Share a point with L4
L6 = np.array([1, 1, 2, 2]) #Parralel to L4

# print(intersect_test(L4,np.array([L6])))
# exit()

N = 5000

bbs = bbs_factory()
lines = np.array([[bbs.__next__() for _ in range(4)] for _ in range(N)])

count = 0
for i in range(N):
    if i % 100 == 0:
        print(i)
    count += intersect_test(lines[i,:], lines[i+1:,:])
print("cnt", count)
print("ans", len(intersection_points))