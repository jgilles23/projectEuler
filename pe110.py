import math

#BAD PROGRAMMING NOTATION
#When it pauses for a long time, this is the best answer

M = 4*10**6
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]


def evaluate2(factors):
    n = 1 #Big number
    m = 1 #number of breakdowns
    for i, f in enumerate(factors):
        n = n*primes[i]**f
        m = m*(2*f + 1)
    m = (m+1)//2
    return n, m

best_n = 10**100
best_m = None

def iterate(old_factors):
    # print(old_factors)
    #See if the recursion should break
    global best_n, best_m
    n, m = evaluate2(old_factors)
    if n >= best_n:
        #break if n is too large
        return
    if m > M:
        best_n = n
        best_m = m
        print("Found best: log_n {:.4}, n {:}, m {:,}, level {:}, factors {:}".format(math.log10(n), n, m, sum(old_factors), tuple(old_factors)))
        return
    #Continue recursion
    for k in range(len(old_factors), -1, -1):
        new_factors = [x for x in old_factors]
        if k == 0:
            new_factors[k] += 1
        elif k < len(old_factors):
            if old_factors[k-1] > old_factors[k]:
                new_factors[k] += 1
            else:
                continue
        else:
            new_factors.append(1)
        #Iterate on the new_factors
        iterate(new_factors)
    return


iterate([1,1,1,1,1,1,1])

exit()

def step2(old_factors):
    print("Stepping:", old_factors)
    old_n, old_m = evaluate2(old_factors)
    best_m = 0
    best_factors = None
    best_ratio = 0
    for k in range(len(old_factors)+1):
        #Create the new factors
        new_factors = [x for x in old_factors]
        if k < len(old_factors):
            new_factors[k] += 1
        else:
            new_factors.append(1)
        new_n, new_m = evaluate2(new_factors)
        #Calculate ratio
        ratio = (new_m - old_m)/(new_n - old_n)
        #See if this is the answer
        if new_m > M:
            print(" *** Fulfilled: ", end="")
            print(" > k {:}, log_n {:.4}, n {:}, m {:,}, ratio {:.4}".format(k, math.log(new_n), new_n, new_m, ratio), end="")
            print("")
        #See if it is the best answer so far
        if ratio > best_ratio:
            best_m = new_m
            best_factors =  new_factors
            best_ratio = ratio
            # print(", new best")
        else:
            pass
            # print("")
    if best_m > M:
        return best_factors, True
    else:
        return best_factors, False

q = [1]
fulfilled = False
while fulfilled == False:
    q, fulfilled = step2(q)
print("Fulfilled.")
exit()



def evaluate(factors, verbose=True, integer_n=False):
    #(numdiv(n^2)+1)/2
    log_n = 0
    n = 1
    log_m = 0
    m = 1
    for i,f in enumerate(factors):
        log_n += log_primes[i]*f #Size of number
        m = m*(2*f + 1) #Sum of the number of breakdowns
        if integer_n:
            n = n*primes[i]**f
    #Evaluate the true m
    m = (m+1)/2
    if integer_n:
        print("n", n)
    elif verbose:
        print("log_n", log_n, "m", "{:,}".format(m))
        if log_m > log_M:
            print("FOUND IT")
            evaluate(factors, False, True)
    return(log_n, m, m > M)

def step(old_factors):
    print("Stepping:", old_factors)
    old_n, old_m, _ = evaluate(old_factors, False)
    best_factors = 0
    best_ratio = 0
    best_i = 0
    for i in range(len(old_factors)+1):
        new_factors = [x for x in old_factors]
        if i == len(old_factors):
            new_factors.append(1)
        else:
            new_factors[i] = new_factors[i] + 1
        new_n, new_m, resolved = evaluate(new_factors, False)
        if resolved == True:
            return True, new_factors
        ratio = (math.log(new_m) - math.log(old_m))/(new_n - old_n)
        print(" > {:}: log_n {:.4}, log_m {:.4}, m {:,}, ratio {:.4}".format(i, new_n, math.log(new_m), new_m, ratio), end=" ")
        if ratio > best_ratio:
            best_ratio = ratio
            best_factors = [x for x in new_factors]
            best_i = i
            print("new best")
        else:
            print("")
        # if resolved == True:
        #     return True, best_factors
    print(" > BEST:", best_i)
    return False, best_factors


q = [1]
fulfilled = False
while fulfilled == False:
    fulfilled, q = step(q)
    # break
print("################# PRINTING ANSWER #################")
print(q)
evaluate(q)
evaluate(q, True, True)

fulfilled, q = step(q)
