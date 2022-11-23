
def V(x, a, b, c):
    v = 4*(x-1)*(a+b+c+x-2) + 2*(a*b+a*c+b*c)
    return v


N = 1000
max_n = 20000
record = [0]*(max_n+1)

vector = [1, 1, 1, 0] #x,a,b,c
pointer = 3
v = 0
while True:
    if v < max_n:
        pointer = 3
        vector[pointer] += 1
    else:
        pointer -= 1
        if pointer < 0:
            #Exit loop when x is too large
            break
        vector[pointer] += 1
        if pointer == 0:
            vector = [vector[0], 1, 1, 1]
        else:
            for p in range(pointer+1, 4):
                vector[p] = vector[pointer]
    v = V(*vector)
    # print(vector, "pointer", pointer, "v", v)
    if v <= max_n:
        record[v] += 1
# print(record)

print("ANS", record.index(N))

# print(record[22], record[46], record[78], record[118])

# v = 0
# x = 0
# while True:
#     x += 1
#     a = 1
#     if not V(x, a, a, a, max_n, record): break
#     while True:
#         a += 1
#         b = a
#         if not V(x, a, b, b, max_n, record): break
#         while True:
#             b += 1
#             c = b
#             if not V(x, a, b, c, max_n, record): break
#             while True:
#                 c += 1
#                 if not V(x, a, b, c, max_n, record): break
# print(record)


