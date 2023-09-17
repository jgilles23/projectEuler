import math
import matplotlib.pyplot as plt

def intersect(line0:list[int], line1:list[int]):
    #line: [x, y, x, y]
    x00, y00, x01, y01 = line0
    x10, y10, x11, y11 = line1
    #Check parallel
    dx0 = x01 - x00
    dy0 = y01 - y00
    dx1 = x11 - x10
    dy1 = y11 - y10
    #Check if parallel
    if dy0*dx1 == dy1*dx0:
        return False, (0, 0), (0, 0)
    #Get intersection
    #Answers in the form n / f
    xn = dx0*dx1*(y10 - y00) - dx0*dy1*x10 + dx1*dy0*x00
    xf = dx1*dy0 - dx0*dy1
    g = math.gcd(xn, xf) * (-2*(xf < 0) + 1)
    xn, xf = xn // g, xf // g
    #Ensure x is in range for both line segments
    if xn < min(x00,x01)*xf or xn > max(x00,x01)*xf or xn < min(x10, x11)*xf or xn > max(x10, x11)*xf:
        return False, (xn, xf), (0, 0)
    #Calculate the y intersection
    if dx0 == 0:
        yn = dy1*xn + y10*xf*dx1 - xf*dy1*x10
        yf = dx1*xf
    else:
        yn = dy0*xn + y00*xf*dx0 - xf*dy0*x00
        yf = dx0*xf
    g = math.gcd(yn, yf)*(-2*(yf < 0) + 1)
    yn, yf = yn//g, yf//g
    #Ensure y is in range for both line segments
    if yn < min(y00,y01)*yf or yn > max(y00,y01)*yf or yn < min(y10, y11)*yf or yn > max(y10, y11)*yf:
        return False, (xn, xf), (0, 0)
    #Ensure x, y is not an end point for the line segements
    if xf == 1 and yf == 1 and (xn==x00 and yn==y00) or (xn==x01 and yn==y01) or (xn==x10 and yn==y10) or (xn==x11 and yn==y11):
        return False, (xn, xf), (yn, yf)
    # print((xn/xf, yn/yf))
    return True, (xn, xf), (yn,yf)

def bbs_factory():
    sn = 290797
    while True:
        sn = (sn * sn) % 50515093
        tn = sn % 500
        yield tn

L0 = [5, 7, 10, 12]
L1 = [14, 5, 6, 13]
L2 = [6,5, 6,6]
L3 = [10,1,10,12]
L4 = [1,1, 15,1]
L5 = [11,0, 9,12]

N = 5000

bbs = bbs_factory()
lines = [[bbs.__next__() for _ in range(4)] for _ in range(N)]
# lines = [L0, L1, L2, L3, L4, L5]

# for line in lines:
#     plt.plot([line[0], line[2]], [line[1], line[3]])

intersection_points = set()

for i in range(len(lines)):
    if i % 100 == 0:
        print(i)
    for j in range(i+1, len(lines)):
        flag, x, y = intersect(lines[i], lines[j])
        if flag:
            # print(flag, x, y)
            # plt.scatter(x[0]/x[1], y[0]/y[1])
            intersection_points.add((x,y))
print("ans", len(intersection_points))

# plt.show()

# 2868997
# 2868997
# 187304
# 2856137 <- new algo
# 2856345
# 2856345 <- Same wrong answer... with 10^-10 as the small box bounds
# 12370609 <- integer refactor (3); I think that seems wrong, picking up something extra
# 2868868 <- fixed an obvious error with adding non-solutions