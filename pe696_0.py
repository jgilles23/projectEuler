# Project euler #696 Mahjong 20210503
# CONTAINS: brute_iterate_group([],n,s,t) for brute forcing through the solution
# This is likely to be a very long solve...

def str_hand(hand):
    s = "<"
    for tile in hand:
        s += chr(tile[0]+65) + str(tile[1]) + " "
    s = s[:-1]
    s += ">"
    return s


def is_count_valid(n, s, hand):
    count = {}
    for tile in hand:
        if tile in count:
            count[tile] += 1
        else:
            count[tile] = 1
    # Validate sum
    for key in count:
        if count[key] > 4:
            return False
    return True


brute_verbose = True
def brute_iterate_group(hand, N, S, T):
    if len(hand) >= 3*T + 2:
        if is_count_valid(N, S,hand):
            hand.sort()
            return set([tuple(hand)])
        else:
            return set()
    winning = set()
    for s in range(S):
        if brute_verbose:
            if len(hand) ==0:
                print("Suit {:}: Pung".format(s), end="", flush=True)
        # Check Pung - (two or three of a kind)
        for n in range(N):
            if brute_verbose:
                if len(hand) ==0:
                    print("-"+str(n), end="", flush=True)
            tile = (s, n)
            new_hand = [t for t in hand] + [tile, tile]
            if len(hand) != 0:
                new_hand += [tile]
            winning.update(brute_iterate_group(new_hand, N, S, T))
        if brute_verbose:
            if len(hand) ==0:
                print()
        if len(hand) == 0:
            # Don't check Chow for the pair
            continue
        # Check Chow (run of 3)
        for n in range(N-2):
            new_hand = [t for t in hand]
            new_hand += [(s, n), (s,n+1), (s,n+2)]
            winning.update(brute_iterate_group(new_hand, N, S, T))
    return winning

def brute_classify(hand, found=[]):
    if len(hand) == 0:
        return [found]
    # Count occurances of each tile
    counts = {}
    for tile in hand:
        if tile in counts:
            counts[tile] += 1
        else:
            counts[tile] = 1
    wins = []
    # Find a pair
    if not found:
        # Find a pair first
        for tile in counts:
            if counts[tile] >= 2:
                new_hand = [x for x in hand]
                new_hand.remove(tile)
                new_hand.remove(tile)
                new_found = [x for x in found]
                new_found.append((tile, tile))
                wins.extend(brute_classify(new_hand, new_found))
    else:
        # Not a pair
        # Find a pung
        for tile in counts:
            if counts[tile] >= 3:
                new_hand = [x for x in hand]
                new_hand.remove(tile)
                new_hand.remove(tile)
                new_hand.remove(tile)
                new_found = [x for x in found]
                new_found.append((tile, tile, tile))
                wins.extend(brute_classify(new_hand, new_found))
        # Find a chow
        for tile in hand:
            tile1 = (tile[0], tile[1] + 1)
            tile2 = (tile[0], tile[1] + 2)
            if tile1 in hand and tile2 in hand:
                new_hand = [x for x in hand]
                new_hand.remove(tile)
                new_hand.remove(tile1)
                new_hand.remove(tile2)
                new_found = [x for x in found]
                new_found.append((tile, tile1, tile2))
                wins.extend(brute_classify(new_hand, new_found))
    if not found and len(wins) == 0:
        print("COULD NOT FIND GROUPS FOR", hand)
    return wins


# TRY 1 AT SEARCHING
def tree_calculate_2(n, s,t):
    if (t !=2):
        print("TREE CALCULATE ONLY DOES t=2")
    hands = 0
    # Calcuate the number of pairs
    pairs = n*s
    # pung-pung
    pung_pung = pairs*(n*s-1)*(n*s-2)
    hands += pung_pung
    # pung-chow & visa versa
    pung_chow = pairs*(n*s-1)*((n-2)*s)//2  # /2 to remove end swaps
    hands += pung_chow
    # chow-chow
    chow_chow = 0
    chow1 = (n-2)*s
    chow2_diff = (n-3)*s
    chow_chow += pairs*chow1*chow2_diff  # When they are different
    chow_chow += pairs*chow1*chow1//2  # End swapping when same
    hands += chow_chow
    print(pung_pung, pung_chow, chow_chow)
    return hands

def main():
    n,s,t = (4,1,2)
    q = brute_iterate_group([], n,s,t)
    print("brute (n={:}, s={:}, t={:}) winning hands: {:,}".format(n, s,t,len(q)))
    # for hand in list(q)[::int(len(q)/9)]:
    #    print(hand)

#main()

