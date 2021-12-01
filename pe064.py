

def iterate(n, m, group):
    """
    Takes a group of the form (a0, b0, c0) of the equation a0 + (sqrt(n) + c0)/b0 and finds the next iterative group of the form
    a0 = 1/[a1 + (sqrt(n) + c1)/b1]
    """
    a0, b0, c0 = group
    b1 = (n - c0**2)//b0 #Maybe //
    a1 = (c0 + m)//b1
    c1 = a1*b1 - c0
    #print("a1",a1, "b1", b1, "c1", c1)
    new_group = (a1, b1, c1)
    #print("   {group:}: {a:} + (sqrt({n:}) - {c:})/{b:}".format(group=new_group, n=n, a=a1,b=b1,c=c1))
    return new_group


def get_period(n):
    print("FINDING", n)
    m = int(n**0.5) #smaller square
    #Return on squares
    if m**2 == n:
        return 0
    #Make list of groups to find the period
    group_timeline = [(m, 1, m)] #Seed with the first group
    while True:
        new_group = iterate(n, m, group_timeline[-1]) #Iterate on the last group
        if new_group in group_timeline:
            period = len(group_timeline) - group_timeline.index(new_group)
            print("   Period found", period)
            return period
        else:
            group_timeline.append(new_group)

for i in range(2,14):
    get_period(i)

periods = [get_period(i) for i in range(2, 10000 + 1)]
count_odd = sum([(p%2)==1 for p in periods])
print("ans", count_odd)