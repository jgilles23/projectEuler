from __future__ import annotations
import matplotlib.pyplot as plt


def intersect_line(left_a, right_a, left_b, right_b):
    # Find the bounds of the overlapping portions of the line
    # Return flag: True if overlapping, False otherwise
    # Return flag, left_c, right_c
    if right_a < left_b or left_a > right_b:
        return False, 0, 0
    return True, max(left_a, left_b), min(right_a, right_b)


class Box:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def __str__(self):
        return "[left: {}, right: {}, bottom: {}, top: {}]".format(self.left, self.right, self.bottom, self.top)

    def intersect(self, other: Box, flag_only=True):
        # Intersect 2 boxes returing a 3rd box if intersection works
        flag, left, right = intersect_line(
            self.left, self.right, other.left, other.right)
        if flag == False:
            return False, 0
        flag, bottom, top = intersect_line(
            self.bottom, self.top, other.bottom, other.top)
        if flag == False:
            return False, 0
        if not flag_only:
            return_box = Box(left, right, bottom, top)
        else:
            return_box = 0
        return True, return_box
    
    def intersect_flag(self, other: Box):
        # Intersect 2 boxes returing a 3rd box if intersection works
        flag, left, right = intersect_line(
            self.left, self.right, other.left, other.right)
        if flag == False:
            return False
        flag, bottom, top = intersect_line(
            self.bottom, self.top, other.bottom, other.top)
        if flag == False:
            return False
        return True

    def yield_points(self):
        yield self.left, self.bottom
        yield self.left, self.top
        yield self.right, self.top
        yield self.right, self.bottom

    def point_in_box(self, x, y):
        # left and bottom are OUTSIDE the box
        return x > self.left and x <= self.right and y > self.bottom and y <= self.top

    def split(self):
        # Return 2 boxes that are each half the size of the origional box
        # Split along the currently larger direction
        if self.right - self.left > self.top - self.bottom:
            center = (self.left + self.right)/2
            return Box(self.left, center, self.bottom, self.top), Box(center, self.right, self.bottom, self.top)
        else:
            center = (self.bottom + self.top)/2
            return Box(self.left, self.right, self.bottom, center), Box(self.left, self.right, center, self.top)

    def contains_endpoints(self, line:Line):
        return self.point_in_box(line.x0, line.y0) or self.point_in_box(line.x1, line.y1)

    def contains_line(self, line:Line):
        # Determine if the line enters the box
        # left and bottom are OUTSIDE the box
        #If one or both points are in the box, the box contains the line
        if self.contains_endpoints(line):
            return True
        #Next check in the boxes overlap
        flag, _ = self.intersect(line) #Return flag only
        if flag == False:
            return False
        #Since the boxes do overlap check that the box overlaps with the line
        flag = line.straddle_box(self)
        return flag
    
    def plot(self, color=0):
        plt.plot([self.left, self.left, self.right, self.right, self.left],[self.bottom, self.top, self.top, self.bottom, self.bottom])



class Line(Box):
    def __init__(self, xyxy):
        super().__init__(min(xyxy[::2]), max(xyxy[::2]), min(xyxy[1::2]), max(xyxy[1::2]))
        self.xyxy = xyxy
        self.x0, self.y0, self.x1, self.y1 = xyxy
        if self.x1 - self.x0 == 0:
            self.slope = None
            self.b = None
        else:
            self.slope = (self.y1 - self.y0)/(self.x1 - self.x0)
            self.b = self.y0 - self.slope*self.x0
        

    def polarize_point(self, x, y):
        # Determine if a point is:
        # 1 above the live
        # 0 on the line
        # -1 below the line
        left_side = (y - self.y0)*(self.x1 - self.x0)
        right_side = (self.y1 - self.y0)*(x - self.x0)
        if left_side < right_side:
            return -1  # below
        elif left_side == right_side:
            return 0  # on the line
        else:
            return 1  # above

    def straddle_box(self, box: Box):
        # Determine if a box "stradles" a line
        counts = [0, 0, 0]  # =[0s, 1s, -1s]
        for x, y in box.yield_points():
            counts[self.polarize_point(x, y)] += 1
        # Determine if stradeling
        return counts[1] < 4 and counts[2] < 4
    
    def plot(self, color="black", plot_box=False):
        if plot_box:
            super().plot(color)
        plt.plot([self.x0, self.x1], [self.y0, self.y1], color=color)
    
    def check_parallel(self, other:Line):
        # Check if two lines are parallel
        return (self.y1 - self.y0)*(other.x1 - other.x0) == (other.y1 - other.y0)*(self.x1 - self.x0)
    
    def point_on_segement(self, x:int, y:int):
        # Check if point x,y is on the line segement
        # only works if x AND y are INTEGERS for sure -- otherwise potential floating point error
        return (y - self.y0)*(self.x1 - self.x0) == (self.y1 - self.y0)*(x - self.x0)
    
    def intersect_line(self, other:Line):
        # Find the xy intersection point of a line and another line
        # Return a flag indicating if that point is on the line
        if self.check_parallel(other) is True:
            return False, 0, 0
        # Check endpoints
        if self.point_on_segement(other.x0, other.y0): return False, other.x0, other.y0
        if self.point_on_segement(other.x1, other.y1): return False, other.x1, other.y1
        if other.point_on_segement(self.x0, self.y0): return False, self.x0, self.y0
        if other.point_on_segement(self.x1, self.y1): return False, self.x1, self.y1
        #Calcualte non-trivial intersection point
        if self.slope is None:
            x = self.x0
            y = other.slope*x + other.b
        elif other.slope is None:
            x = other.x0
            y = self.slope*x + self.b
        else:
            x = (other.b - self.b)/(self.slope - other.slope)
            y = self.slope*x + self.b
        #Check if x,y is on BOTH lines
        flag = self.point_in_box(x, y) and other.point_in_box(x,y)
        return flag, x, y

def bbs_factory():
    sn = 290797
    while True:
        sn = (sn * sn) % 50515093
        tn = sn % 500
        yield tn

def recurse(box:Box, lines:list[Line]):
    global min_box_length
    # Narrow down the lines that are in the box
    lines2 = [line for line in lines if box.contains_line(line)]
    if len(lines2) <= 1:
        # 1 or fewer lines in the proposed box
        return 0
    if len(lines2) == 2:
        #Only two lines left, check if they intersect in the box; if yes, we are done here
        flag, x, y = lines2[0].intersect_line(lines2[1])
        if flag == False:
            # Lines do not intersect at all
            return 0
        # Check if the intersection point of the lines is in the box and return
        if box.point_in_box(x, y):
            # box.plot()
            # print("two", box)
            return 1
        else:
            return 0 
    # Check if the box is "small enough" --- must be 3 or more lines for this to take effect
    if (box.right - box.left) < min_box_length and (box.top - box.bottom) < min_box_length:
        #Check if all the lines intersect with each other in the box, if yes, done, if not, maybe problem
        for a in range(len(lines2)):
            for b in range(a + 1, len(lines2)):
                flag, x, y = lines2[a].intersect_line(lines2[b])
                if flag == False:
                    #Lines do not intersect at all
                    return 0
                if box.point_in_box(x,y) == False:
                    #Lines do not intersect in the box
                    return 0
        #Lines do intersect in the minimum box
        plt.scatter([x], [y], marker="o")
        for line in lines2:
            line.plot()
        box.plot()
        print("mor", box)
        return 1
    # Split the box into two and call recurse box on each half
    box_a, box_b = box.split()
    count = recurse(box_a, lines2) + recurse(box_b, lines2)
    return count


L1 = [27, 44, 12, 32]
L2 = [46, 53, 17, 62]
L3 = [46, 70, 22, 40] #intersects L2
L4 = [11, 29, 22, 40]
L5 = [12, 30, 400, 421] #Share a point with L4
L6 = [1, 1, 2, 2] #Parralel to L4
L7 = [10, 10, 50, 50]
L8 = [15, 45, 45, 15]
L9 = [30, 5, 30, 40]

N = 5000
min_box_length = 10**-10

bbs = bbs_factory()
main_lines =[Line([bbs.__next__(), bbs.__next__(), bbs.__next__(), bbs.__next__()]) for _ in range(N)]

# main_lines = [Line(L7), Line(L8), Line(L9)]
main_box = Box(0, 499, 0, 499)

# for line in main_lines:
#     line.plot(0)
main_box.plot(0)


print(recurse(main_box, main_lines))
plt.show()


# 2868997
# 2868997
# 187304
# 2856137 <- new algo
# 2856345
# 2856345 <- Same wrong answer... with 10^-10 as the small box bounds
