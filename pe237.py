from itertools import product, combinations, permutations
import numpy as np

#0  4
#1  5
#2  6
#3  7

#connections: (Left, Right, Up, Down)
center_options = {(1,0,1,0):"╯", (1,0,0,1):"╮", (0,1,1,0):"╰", (0,1,0,1):"╭", (0,0,1,1):"│", (1,1,0,0):"-"}
caps, passes, turns = [], [], []
pass_map = {}
for centers in product(center_options.keys(), repeat=4):
    up_requirement = 0
    origin, destination = None, None
    pairs = []
    for i, center in enumerate(centers):
        #Check if meeting down requirement
        if center[2] != up_requirement:
            break
        #Generate the up status for the next center
        up_requirement = center[3] #up requirement for next center is the down status of this center
        #Determine origin or destination
        if center == (1,1,0,0):
            origin, destination = i, i + 4
        elif center == (0,0,1,1):
            pass
        elif origin is None:
            origin = i + 4*center[1]
        elif destination is None:
            destination = i + 4*center[1]
        #Check if pair is completed
        if origin is not None and destination is not None:
            pairs.append((origin, destination) if origin < destination else (destination, origin))
            origin, destination = None, None
    else:
        #Check if ending without facing down
        if center[3] != 0:
            continue
        #Now classify the number of crossings
        crossings = 0
        left_connections, right_connections = 0, 0
        for pair in pairs:
            if pair[0] < 4 and pair[1] < 4:
                left_connections += 2
            elif pair[0] >= 4 and pair[1] >= 4:
                right_connections += 2
            else:
                left_connections += 1
                right_connections += 1
                crossings += 1
        #Eliminate odd crossings and non-caps
        if crossings % 2 != 0:
            continue
        if crossings == 0 and right_connections > 0:
            continue
        #valid
        if crossings == 0:
            caps.append(centers)
        elif left_connections != right_connections:
            turns.append(centers)
        elif crossings < 4:
            passes.append(centers)
            left_right = ["0" for _ in range(8)]
            for x, y in pairs:
                left_right[x] = "1"
                left_right[y] = "1"
            left = "".join(left_right[:4])
            right = "".join(left_right[4:])
            pass_map[left] = pass_map.get(left, []) + [right]
        elif crossings == 4:
            passes.append(centers)
            pass_map["1111"] = pass_map.get("1111", []) + ["1111"]
        else:
            raise Exception("Unexpected number of crossings")

#Pass map is already generated above
#Add in turns to the map
turn_map = {}
turn_map["1122"] = turn_map.get("1122", []) + ["0011"]
turn_map["0011"] = turn_map.get("0011", []) + ["1221"]
turn_map["1221"] = turn_map.get("1221", []) + ["1001"]
turn_map["1001"] = turn_map.get("1001", []) + ["1122"]
turn_map["1122"] = turn_map.get("1122", []) + ["1100"]
turn_map["1100"] = turn_map.get("1100", []) + ["1221"]
#Finally a cap map
cap_map = {}
cap_map["1122"] = cap_map.get("1122", []) + ["0000"]
cap_map["1001"] = cap_map.get("1001", []) + ["0000"]

#Print mapping results
to_print = {"passes": (passes, pass_map), "turns": (turns, turn_map), "caps": (caps, cap_map)}
for name, (centers, mapping) in to_print.items():
    print(f'Valid {name}: {len(centers)}')
    print(mapping)
    for line in zip(*(centers)):
        for center in line:
            print(center_options[center], end="   ")
        print()


#combine the pass_map and turn_map into a continue_map
continue_map = {}
for key, values in pass_map.items():
    continue_map[key] = continue_map.get(key, []) + values
for key, values in turn_map.items():
    continue_map[key] = continue_map.get(key, []) + values

#Compose a list of valid states
valid_states = list(set(continue_map.keys()) | set(cap_map.keys()))
valid_states.sort()
print(f"Valid states ({len(valid_states)}):", valid_states)

#Make a matrix of the state mapping
A = np.zeros((len(valid_states), len(valid_states)), dtype=np.int64)
for x in continue_map:
    for y in continue_map[x]:
        A[valid_states.index(y), valid_states.index(x)] += 1
print(A)
start = np.zeros((len(valid_states), 1), dtype=np.int64)
start[valid_states.index("1001"), 0] = 1

#Matrix power functio

N = 10
B = np.linalg.matrix_power(A, N-1)
print("B")
print(B)
result = B @ start
ans = result[valid_states.index("1001")] + result[valid_states.index("1122")]
for i, state in enumerate(valid_states):
    print(f"{state}: {result[i]}", end="   ")
print()
print(ans)

def recursive_connection(left, right, center, input_index, output_index, connection_type):
    #Return False if the connection is not possible, otherwise return a new center and a new right
    #Make sure the center is open & mark it
    a, b = sorted([input_index, output_index])
    if any(center[a, b+1]):
        return False
    for i in range(a, b+1):
        center[i, b+1] = 1
    #Check through the connection types
    if connection_type == 0:
        #left to left
        if left[input_index] != left[output_index]:
            return False
        left[input_index] = 0
        left[output_index] = 0
    elif connection_type == 1:
        #left to right
        pass
    elif connection_type == 2:
        #right to left
        pass
    elif connection_type == 3:
        #right to right
        pass
    else:
        raise Exception("Invalid connection type")
    

    

        
        


#Trying a different approach
def get_right_from_left(left):
    right_options = []
    left_list = list(left)
    center_list = [None for _ in range(4)]