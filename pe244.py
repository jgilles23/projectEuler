

#boards are 

starting_state = ((0,0), ((0, 1, 2, 2), (1, 1, 2, 2), (1, 1, 2, 2), (1, 1, 2, 2)))
target_state =   ((0,0), ((0, 2, 1, 2), (2, 1, 2, 1), (1, 2, 1, 2), (2, 1, 2, 1)))
# target_state =   ((3,1), ((1, 1, 2, 2), (1, 1, 2, 2), (1, 1, 2, 2), (1, 0, 2, 2)))

def clamp (value, min_value, max_value):
    return max(min_value, min(value, max_value))

def substitute(board, position, new_value):
    new_board = tuple(tuple(new_value if (j, i) == position else board[j][i] for i in range(4)) for j in range(4))
    return new_board

def move(state, delta_empty):
    empty_pos, board = state
    d_row, d_col = delta_empty
    x, y = (clamp(empty_pos[0] + d_row, 0, 3), clamp(empty_pos[1] + d_col, 0, 3)) #New empty position
    new_board = substitute(board, empty_pos, board[x][y]) #into the empty position, put the value of the new empty position
    new_board = substitute(new_board, (x, y), 0) #into the new empty position, put 0
    return ((x, y), new_board)

UP, DOWN, LEFT, RIGHT = (1, 0), (-1, 0), (0, 1), (0, -1)
ASCII_lookup = {UP: 85, DOWN: 68, LEFT: 76, RIGHT: 82}


def search(state, distance = 0, max_distance = 200):
    #Stop looking if we get too deep or if we have already found a shorter path to this location
    if distance > max_distance:
        return
    if state in state_lookup and state_lookup[state] <= distance:
        return
    #Found a shorter distance to this location
    state_lookup[state] = distance
    for delta in [UP, DOWN, LEFT, RIGHT]:
        new_state = move(state, delta)
        search(new_state, distance + 1, max_distance)

def search_breath(state, target_state):
    state_lookup = {} #state: shortest_distance
    queue = [(state, 0)]
    target_distance = 1000
    while queue:
        state, distance = queue.pop(0)
        if distance > target_distance:
            continue
        if state in state_lookup and state_lookup[state] <= distance:
            continue
        state_lookup[state] = distance
        if state == target_state:
            print("Found target state at distance:", distance)
            target_distance = distance
            continue
        for delta in [UP, DOWN, LEFT, RIGHT]:
            new_state = move(state, delta)
            queue.append((new_state, distance + 1))
    return state_lookup

def path_search(state, target_state, state_lookup, target_depth=[32], current_depth = 0):
    #Assume that the provided max_depth is correct, the function will return False if too shallow, will run long if too deep
    if state == target_state: #Found the target
        target_depth[0] = current_depth
        state_lookup[state] = (current_depth, True)
        print("Found target state at depth:", current_depth)
        return True
    elif current_depth >= target_depth[0]: #Too deep without finding the target
        return False
    elif state in state_lookup: #already visited this node
        if state_lookup[state][0] <= current_depth: #already found a shorter path to this node
            return False
        else:
            return state_lookup[state][1] #return whether we have found the target from this node before
    #input the state, but hasn't been proven to find the target yet
    state_lookup[state] = (current_depth, False) #False means we haven't found the target state from this state yet
    #Iterate through the possible moves
    for delta in [UP, DOWN, LEFT, RIGHT]:
        new_state = move(state, delta)
        if path_search(new_state, target_state, state_lookup, target_depth, current_depth + 1):
            #If we find the target state, return True and add this state to the lookup with the distance
            state_lookup[state] = (current_depth, True) #True means we have found the target state from this state
            return True
    #Did not find the target state, return True
    return False

def bi_directional_search(starting_state, target_state):
    active_queue = [(starting_state, 0)]
    inactive_queue = [(target_state, 0)]
    active_lookup = {starting_state: 0}
    inactive_lookup = {target_state: 0}
    starting_active = True
    current_search_depth = 0
    intersect_mode = False
    solution_depth = 1000
    queue_insertion_point = 1
    while active_queue or inactive_queue:
        #Check if we should swap to the other side of the search because we are out of queue or need to deepen
        if (not active_queue) or (active_queue[0][1] > current_search_depth): #Swap active and inactive queues
            active_queue, inactive_queue = inactive_queue, active_queue
            active_lookup, inactive_lookup = inactive_lookup, active_lookup
            starting_active = not starting_active
            current_search_depth = active_queue[0][1]
            queue_insertion_point = len(active_queue)
            continue
        #Search at the top item of the queue
        state, depth = active_queue.pop(0)
        #Iterate through the possible moves
        for delta in [UP, DOWN, LEFT, RIGHT]:
            new_state = move(state, delta)
            if new_state in active_lookup: #Already visited
                continue
            elif new_state in inactive_lookup and inactive_lookup[new_state] <= solution_depth - depth: #Found an intersection
                if intersect_mode == False: #Found the first intersection
                    intersect_mode = True
                    solution_depth = depth + inactive_lookup[new_state]
                    #Remove items already added to the lookup and the queue this round
                    for state_to_delete in active_queue[queue_insertion_point:]:
                        del active_lookup[state_to_delete[0]]
                    active_queue = active_queue[:queue_insertion_point]
            elif intersect_mode: #In intersect mode, but not an intersection
                continue
            #Add the state to the lookup and the queue
            active_lookup[new_state] = depth + 1
            active_queue.append((new_state, depth + 1))
    #Finished while loop, now analyze the results
    if starting_active:
        starting_lookup, target_lookup = active_lookup, inactive_lookup
    else:
        starting_lookup, target_lookup = inactive_lookup, active_lookup
    print("Total states in starting lookup:", len(starting_lookup))
    print("Total states in target lookup:", len(target_lookup))
    #Get the intersection of the two lookups with the values from the starting lookup
    combined_lookup_from_start = {state: starting_lookup[state] for state in starting_lookup if state in target_lookup}
    print("Total states in intersection:", len(combined_lookup_from_start))
    #Print the deepest item in the intersection
    deepest_state = max(combined_lookup_from_start, key=lambda state: combined_lookup_from_start[state])
    print("Deepest state in intersection has depth:", combined_lookup_from_start[deepest_state])
    return combined_lookup_from_start

def add_to_checksum(checksum, move):
    return (checksum * 243 + ASCII_lookup[move]) % 100_000_007

def calc_delta(start_pos, end_pos):
    return (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

lookup = bi_directional_search(starting_state, target_state)
#Sort lookup by values
lookup_as_list = sorted(lookup.items(), key=lambda item: item[1])
checksum = 0
for state, i in lookup_as_list[1:]:
    previous_pos = lookup_as_list[i-1][0][0]
    current_pos = state[0]
    delta = calc_delta(previous_pos, current_pos)
    ascii_value = ASCII_lookup[delta]
    checksum = add_to_checksum(checksum, delta)
    print(f"State: {state}, Distance: {i}, delta: {delta}, ascii: {ascii_value}, checksum: {checksum}")
print("ans:", checksum)


# states_from_0 = search_breath(starting_state, target_state)
# states_from_target = search_breath(target_state, starting_state)
# #Get the intersection of the two state lookupsm with the values from states_from_0 being the distances
# intersection_states = {state: states_from_0[state] for state in states_from_0 if state in states_from_target}
# print("total states in intersection:", len(intersection_states))
# #Target state distance
# print("target state distance in intersection:", intersection_states.get(target_state, "not found"))

# state_lookup = {} #state: shortest_list of moves
# search(starting_state, max_distance = 200)
# print(len(state_lookup))

# for depth in range(0, 33):
#     count_at_depth = sum(1 for state in intersection_states if intersection_states[state] == depth)
#     print(f"Depth: {depth}, count: {count_at_depth:,}")

# path_lookup = {}
# path_result = path_search(starting_state, target_state, path_lookup, target_depth=[60])
# print("Found path:", path_result)
# print("Total states in path lookup:", len(path_lookup))
# print("Depth of target state in path lookup:", path_lookup.get(target_state, ("not found",))[0])