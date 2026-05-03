#Vector (x, y, theta, steps, depth)
F = (0, 1, 0, 1)
L = (0, 0, 3, 0)
R = (0, 0, 1, 0)

step_goal = 500
depth_goal = 10
print_flag = depth_goal <= 3

def add_vectors(A, B):
    (xa, ya, thetaa, stepsa) = A
    (xb, yb, thetab, stepsb) = B
    if thetaa == 0:
        new_x, new_y = xa + xb, ya + yb
    elif thetaa == 1:
        new_x, new_y = xa + yb, ya - xb
    elif thetaa == 2:
        new_x, new_y = xa - xb, ya - yb
    else:
        new_x, new_y = xa - yb, ya + xb
    return (new_x, new_y, (thetaa + thetab)%4, stepsa + stepsb)

def subtract_vectors(A, B):
    #Subtract B from A
    (xb, yb, thetab, stepsb) = B
    return add_vectors(A, (-xb, -yb, -thetab, -stepsb))

def plus_F(vector, depth=0):
    if print_flag: print(f"{'- '*depth}F {vector}")
    return add_vectors(vector, F)

def plus_L(vector, depth=0):
    if print_flag: print(f"{'- '*depth}L {vector}")
    return add_vectors(vector, L)

def plus_R(vector, depth=0):
    if print_flag: print(f"{'- '*depth}R {vector}")
    return add_vectors(vector, R)

A_deltas = [None]*(depth_goal+1)
B_deltas = [None]*(depth_goal+1)

def plus_function(vector, depth, function_list, lookup_list):
    input_vector = vector
    depth += 1
    if depth > depth_goal:
        return vector
    #Check if we have found this depth before
    # if lookup_list[depth] is not None:
    #     if print_flag: print(f"{'- '*depth}Found depth {depth} in lookup, adding {lookup_list[depth]} to {vector}")
    #     vector = add_vectors(vector, lookup_list[depth])
    #     if vector[3] <= step_goal: #Allowed to return because we did not hit the depth count
    #         return vector
    #Need to calculate from scratch
    vector = input_vector
    for f in function_list:
        if vector[3] >= step_goal:
            return vector
        vector = f(vector, depth)
    #Need a hacky way to figure out the input vector here, vectors are not reversable
    delta_vector = subtract_vectors(vector, input_vector)
    if print_flag: print(f"{'- '*depth}Finished depth {depth}, adding {delta_vector} to lookup")
    if add_vectors(input_vector, delta_vector) != vector:
        raise Exception(f"Delta vector {delta_vector} does not match the change from {input_vector} to {vector}")
    lookup_list[depth] = delta_vector
    return vector

def plus_a(vector, depth=0,):
    if print_flag: print(f"{'- '*depth}a {vector}")
    functions = [plus_a, plus_R, plus_b, plus_F, plus_R]
    return plus_function(vector, depth, functions, A_deltas)

def plus_b(vector, depth=0):
    if print_flag: print(f"{'- '*depth}b {vector}")
    functions = [plus_L, plus_F, plus_a, plus_L, plus_b]
    return plus_function(vector, depth, functions, B_deltas)

starting_vector = (0, 0, 0, 0)
return_vector = plus_a(plus_F(starting_vector))
print(return_vector)



