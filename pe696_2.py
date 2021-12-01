#PE 691, working on idea #3
#CONTAINS NOTHING USEFUL
#METHOD NOT FRUITFUL AS REQUIRES COUNTING ARRANGEMENTS. BETTER TO GO WITH THE "TOWER APPROACH"
import itertools

def print_counts(counts):
    t = len(counts) - 1
    n = len(counts[0])
    print("COUNTS for n = {:} and t = {:}".format(n,t))
    for i in range(t+1):
        s = " ".join(["{:3}".format(x) for x in counts[i]])
        print("   {:}:".format(i), s)

def brute_layout_chow(n,t):
    #Determine the number of arrangements for t chows in n numbers
    #Do this with a brute force method to use for fact checking
    starts = itertools.product(range(n-2), repeat=t)
    starts = [tuple(sorted(x)) for x in starts]
    starts = set(starts)
    #Setup counts object
    counts = [[0 for _ in range(n)] for _ in range(t+1)]
    #Iterate through the starts
    for S in starts:
        layout = [0]*n
        for s in S:
            layout[s] += 1
            layout[s+1] += 1
            layout[s+2] += 1
        for i in range(n): #Each locaiton in layout
            for j in range(0,layout[i]+1): #Count @ location and below
                counts[j][i] += 1
    return counts

def layout_chow(n,t):
    #Use faster method to complete the layout of the chow
    pass


n = 4
t = 2
print("SLOW LAYOUT")
q = brute_layout_chow(n,t)
print_counts(q)