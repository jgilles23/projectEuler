import sympy

P = 10**8

# triangle (a,b,c) where a < b < c
# Let d = b - a and be a divisor of c s.t.
# c = d*f

def recursion_1(j, f):
    yield j,f
    while True:
        (j,f) = (3*j - 4*f, -2*j + 3*f)
        yield j,f

def recursion_2(j,f):
    yield j,f
    while True:
        (j,f) = (3*j + 4*f, 2*j + 3*f)
        yield j,f

# Use integer solver and recursive solutions to find the values of f that work for this equation

# # BAD Always negative (other than (1,1))
# for j,f in recursion_1(1,1):
#     print((j,f))
#     if abs(f) >= C: break

# GOOD 
jf_valid = []
for j,f in recursion_2(1,1):
    # print((j,f))
    jf_valid.append((j,f))
    if abs(f) >= P//2: break

#Eliminate the (1,1) solution because it always yields an a = 0, which is not a valid solution
jf_valid = jf_valid[1:]
print("jf_valid", jf_valid)

# #BAD - always negative f
# for j,f in recursion_1(-1,-1):
#     print((j,f))
#     if abs(f) >= C: break

# #BAD - always negative f
# for j,f in recursion_2(-1,-1):
#     print((j,f))
#     if abs(f) >= C: break

#Reduce run time by knowing the exact number of times that 5 should be counted
triangle_count = 0

c_solutions = set()
for j, f in jf_valid:
    d = 1
    while (c := f*d) < P:
        #Test triangle
        a = (j-1)//2*d
        b = d + a
        if a+b+c < P:
            #Found a solution
            triangle_count += 1
        #Iterate d
        d += 1
    print("jf", (j,f), "count", triangle_count)
    
print("ans", triangle_count)






# for f in range(2, C):
#     j, integer_flag = sympy.integer_nthroot(2*f**2 - 1, 2)
#     if integer_flag:
#         print(f, end=" ")