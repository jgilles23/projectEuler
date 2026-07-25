#Can't remember the problem name and don't have internet, but getting started anyway
from functools import cache
from itertools import product
import time
import random

def opposite(turn):
    if turn == "L":
        return "R"
    else:
        return "L"

def check_winner(game_strings, turn):
    if all([len(s) == 1 for s in game_strings]):
        L_count, R_count = 0, 0
        for s in game_strings:
            if s == "L":
                L_count += 1
            else:
                R_count += 1
        if L_count > R_count:
            return "L"
        elif R_count > L_count:
            return "R"
        else:
            return "T"
    return None

def check_tail_winner(game_strings, turn):
    if turn == "L":
        if sum([s[-1] == "L" for s in game_strings]) > len(game_strings) // 2:
            return "L"
    else:
        if sum([s[0] == "R" for s in game_strings]) > len(game_strings) // 2:
            return "R"
    return None

@cache
def G_brute_recurse(game_strings, turn, winner_func=check_winner):
    #Game strings as tuple
    if (winner := winner_func(game_strings, turn)) is not None:
        return winner
    #Iterate through the possible new game states
    found_T = False
    for i in range(len(game_strings)):
        s = game_strings[i]
        for j in range(1, len(s)):
            if turn == "L":
                new_string = s[j:]
            else:
                new_string = s[:-j]
            new_game_strings = game_strings[:i] + (new_string,) + game_strings[i+1:]
            resultA = G_brute_recurse(new_game_strings, turn) #If player does not relenquish turn
            resultB = G_brute_recurse(new_game_strings, opposite(turn)) #If player does relenquish turn
            if resultA == turn or resultB == turn:
                return turn
            elif resultA == "T" or resultB == "T":
                found_T = True
    #Did not find a winning move
    if found_T:
        return "T"
    else:
        return opposite(turn)

def G(word_len, num_words, func, print_escalator = 1.3):
    print_counter = 0
    print_threshold = 10**4
    count_L, count_R, count_T = 0, 0, 0
    string_permutations = ["".join(x) for x in product(*[["L", "R"] for _ in range(word_len)])]
    for game_strings in product(*[string_permutations for _ in range(num_words)]):
        result = func(game_strings, "L")
        if result == "L":
            count_L += 1
        elif result == "R":
            count_R += 1
        else:
            count_T +=1
        if print_escalator:
            if print_counter >= print_threshold:
                print(f"winner: {result}, game_strings: {' '.join(game_strings)}, iteration: {print_counter:,}")
                print_threshold = int(print_threshold * print_escalator)
            print_counter += 1
    return (count_L, count_R, count_T)

@cache
def reverse_game_int(game_int):
    #Reverse the binary representation of the game int, so that the current player is always represented by 1s
    s = bin(game_int)[3:]
    s = s.replace("0", "2").replace("1", "0").replace("2", "1")
    r = (int(s[::-1], 2)) | (1 << (game_int.bit_length() - 1))
    # print(f"Reversed {bin(game_int)[:]} to {bin(r)[:]}")
    return r
def reverse_game_ints(game_ints):
    #Reverse the binary representation of the game ints, so that the current player is always represented by 1s
    return tuple(reverse_game_int(x) for x in game_ints)

#Upgrade to a performative version that uses binary representations
@cache
def G_binary_recurse(game_ints, turn):
    #Binary game_int as an integer, always starting with 1, followed by 0/1 where 1 is the current player
    if all(x <= 0b11 for x in game_ints):
        return 1 if sum(x & 1 for x in game_ints) > len(game_ints) // 2 else 0 #Return the player with the most 1s, or 0 for a tie
    elif sum((x >> (x.bit_length() - 2)) & 1 for x in game_ints) > len(game_ints) // 2:
        return 1 #Current player wins if they have more 1s in the second to last position
    #Iterate through the possible new game states
    for i in range(len(game_ints)):
        x = game_ints[i]
        for j in range(1, x.bit_length() - 1):
            new_x = x >> j
            new_game_ints = game_ints[:i] + (new_x,) + game_ints[i+1:]
            resultA = G_binary_recurse(new_game_ints, turn) #If player does not relenquish turn
            if resultA == 1: #I win
                return 1
            resultB = G_binary_recurse(reverse_game_ints(new_game_ints), opposite(turn)) #If player does relenquish turn
            if resultB == 0: #Opponent loses, so I win
                return 1
    #Did not find a winning move
    return 0 #No winning move found, so I lose

def G_bin(word_len, num_words, func, print_escalator = 1.3):
    print_counter = 0
    print_threshold = 10**4
    count_L, count_R = 0, 0
    for game_ints in product(*[range(0b1 << word_len, 0b10 << word_len) for _ in range(num_words)]):
        result = func(game_ints, "L")
        if result == 1:
            count_L += 1
        else:
            count_R += 1
        if print_escalator:
            if print_counter >= print_threshold:
                print(f"winner: {result}, game_ints: {' '.join([bin(x)[3:] for x in game_ints])}, iteration: {print_counter:,}")
                print_threshold = int(print_threshold * print_escalator)
            print_counter += 1
    return (count_L, count_R, 0)
#Binary representation is actually not more performative, for some reason I am sure


#Next version is going to make some assumptions on what you would choose to do
#All cuts by the left player looks something like this:
#...R|L... or ...|L or ...|R or 


word_len = 4
num_words = 5

# t0 = time.time()
# r = G(word_len, num_words, lambda gs, turn: G_brute_recurse(gs, turn, check_winner))
# print(r)
# print("Elapsed time:", time.time() - t0)

# t0 = time.time()
# r = G(word_len, num_words, lambda gs, turn: G_brute_recurse(gs, turn, check_tail_winner))
# print(r)
# print("Elapsed time:", time.time() - t0)

t0 = time.time()
r = G_bin(word_len, num_words, lambda gs, turn: G_binary_recurse(gs, turn))
print(r)
print("Elapsed time:", time.time() - t0)

