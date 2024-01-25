# %%
L = 5
print("Number of triangles:", L**2)

edges = [[] for _ in range(L**2)]

max_t = -1
layer_size = L + 1
t = -1
for layer, layer_size in enumerate(range(2*L-1, 0, -2)):
    min_t = t + 1
    max_t = min_t + layer_size - 1
    for i in range(layer_size):
        t += 1
        if t-1 >= min_t:
            edges[t].append(t-1)
        if t+1 <= max_t:
            edges[t].append(t+1)
        if layer % 2 == 0:
            if t % 2 == 0:
                delta = -layer_size - 1
            else:
                delta = layer_size - 1
        else:
            if t % 2 == 0:
                delta = layer_size - 1
            else:
                delta = -layer_size - 1
        if t + delta >= 0 and t + delta < L**2:
            edges[t].append(t+delta)

edges_lesser = [[edge for edge in edges[t] if edge < t] for t in range(L**2)]
edges_greater = [[edge for edge in edges[t] if edge > t] for t in range(L**2)]
colors = [0]*(L**2)

def recursive_triangle(t, colors):
    if t == L**2:
        #Reached the end
        return 1
    color_options = [True, True, True]
    for edge in edges_lesser[t]:
        color_options[colors[edge]] = False
    count = 0
    for color, flag in enumerate(color_options):
        if flag == True:
            colors[t] = color
            count += recursive_triangle(t+1, colors)
    return count

count = recursive_triangle(0, colors)
print(count)