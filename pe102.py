#Project Euler problem 102
import numpy as np

triangles = []
with open("p102_triangles.txt") as file: 
    for line in file:
        a = [int(x) for x in line[:-1].split(",")]
        triangles.append([a[0:2], a[2:4], a[4:6]])
triangles = np.array(triangles)

def det(a,b):
    return a[0]*b[1] - b[0]*a[1]

inside = 0

for triangle in triangles:
    signs = [det(triangle[0], triangle[1]),
             det(triangle[1], triangle[2]),
             det(triangle[2], triangle[0])]
    signs = np.sign(signs)
    if np.all(signs == 1) or np.all(signs == -1):
        inside += 1

print(inside)