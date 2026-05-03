import numpy as np
#The chase
#Normally, <- 1/6 left, 4/6 stay, 1/6 right ->
#When you stack the second dice; 
#   +2 1/36 towards each other
#   +1 4/6*1/6 + 4/6*1/6 = 8/36 towards each other
#   -1 4/6*1/6 + 4/6*1/6 = 8/36 away from each other
#   -2 1/36 away from each other
#   0 4/6*4/6 = 16/36 no change
# Total = 34/36 -- missing something
intermediate_36 = {
    -2: 1, #directly together 1*1
    -1: 8, #one stays other towards = 1*4 + 4*1
    0: 18, #both stay or move in same direction = 4*4 + 1*1 + 1*1
    1: 8, #one stays other away = 1*4 + 4*1
    2: 1 #directly apart 1*1
}

number_players = 6
sig_figs = 10
threshold = 10**(-sig_figs*2)

N = number_players//2 + 1

M_i = np.full((N, N+4), 0, dtype=np.double)
for input_index in range(N):
    for delta in range(-2, 3):
        output_index = input_index + delta
        M_i[input_index, input_index + delta] = intermediate_36[delta]
# print(M_i.transpose())

M = M_i[:, :N]
M[:, 1] += M_i[:, -1]
M[:, 2] += M_i[:, -2]
M[:, N-2] += M_i[:, N]
M[:, N-3] += M_i[:, N+1]
M_pre = M.copy()
M[0, :] = 0
M[0, 0] = 36
M = M / 36
# print(M.transpose())
print(M.sum(axis=1))

x = np.full((N,), 0, dtype=np.double)
x[-1] = 1
x_start = x.copy()
print("Iterating start:")
average_game_length = 0
turn = 0
while True:
    games_ended = x[0]
    average_game_length += games_ended * turn
    x[0] = 0
    if turn % 1000 == 0:
        print(f"Turn {turn}: {games_ended} ended here, {x.sum()} ongoing, {average_game_length} avg length")
        if x.sum()*turn < threshold and turn != 0:
            print("Terminating.")
            break
    #Roll and pass representation
    x = x @ M
    turn += 1

#Dirty rounding
rounded_ans = 0
i = 0
while len(str(rounded_ans)) < sig_figs + 1:
    rounded_ans = round(average_game_length, i)
    i += 1

print("ans", rounded_ans)

#14762.1249 incorrect
#14762.12487 incorrect
#3631.506249 incorrect
#3780.618622 correct

# M = M_pre
# M[:, 0] = 0

# v = np.full_like(x_start, 0)
# v[0] = 1
# print(x_start)
# a = M @ np.linalg.inv(np.eye(N) - M)**2
# print(a)

# A = 0
# for n in range(0, 1000+1):
#     A += n * x_start @ M**n @ v
# print("TESTING...")
# print(np.transpose(M))
# print(np.transpose(M**4))
# print(x_start @ M**3)
# print("A", A)