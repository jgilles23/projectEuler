# Project Euler Problem 681
from sympy import primerange

# Declare constants
n = 10**4 # value provided in problem
print_period = 500 #how often print
max_A = 4*n  # By hand calculation
count = 0 #Starting count

# Find the relevant primes
print("Generating primes")
primes = list(primerange(0, n))
print("Generated", len(primes), "primes less than", n)

def apply_parts(orig,x):
    #Takes an orig -- an ordered 4 tuple and applys x^2 partitions then returns the partitions
    #Start with applications of 2,0,0,0 partitions
    a,b,c,d = orig
    A,B,C,D = (a*x, b*x, c*x, d*x)
    #2,0,0,0 partitions
    new_parts = [[A*x,b,c,d], [a,B*x,c,d], [a,b,C*x,d], [a,b,c,D*x], #2,0,0,0 partitions
    [A,B,c,d], [A,b,C,d], [A,b,c,D], [a,B,C,d], [a,B,c,D], [a,b,C,D]] #1,1,0,0 paritions
    out = set()
    for part in new_parts:
        part.sort(reverse=True) #Sort partitions smallest to largest
        #Throw away parts that are too large
        if part[0] > max_A:
            #Do not pass along items where A is too large
            continue
        #v = part[2]*part[3]
        #w = part[2] + part[3]
        #if part[0] > n**(1/3) + 4*n/(part[2]*part[3])**0.5:
        #    #print("Escaping Here")
        #    continue
        out.add(tuple(part))
    return out

def apply_parts_to_all(parts, x):
    #run apply_parts on a set of partitions and output a single set
    out = set()
    for part in parts:
        out.update(apply_parts(part,x))
    return out


def sum_abcd(part):
    #function to provide sum of side lengths if a quadralaterial is made
    A,B,C,D = part #unpack tuple
    if A >= B+C+D:
        #Quick check to see if A is in the right range
        return 0
    #Calculate the side lengths
    a = (B+C+D-A)/4
    b = (A+C+D-B)/4
    c = (A+B+D-C)/4
    d = (A+B+C-D)/4
    if a%1==0 and b%1==0 and c%1==0 and d%1==0 and a<b+c+d:
        #Ensure all the side lengths are integers, that side lengths close shape
        #s = (a+b+c+d)/2
        #area = ((s-a)*(s-b)*(s-c)*(s-d))**(1/2)
        #print("Success", "sides", (a,b,c,d), "bigs", (A,B,C,D), "area", area)
        return int(a+b+c+d)
    else:
        return 0


def print_progress(fact_inds, q, count, len_parts):
    s = ""
    for ind in fact_inds:
        if ind > 99:
            s += "** "
        else:
            s += "{:2} ".format(ind)
    s = s.ljust(50)
    s += "| {:12,} q | {:12,} parts |{:12,} count".format(q, len_parts, count)
    print(s)

def next_factor(q, max_prime_ind, latest_fact, parts, fact_inds):
    #Recursive function for stepping through the q tree - where q is the area of the target quadralaterial
    #print("q", q, "ind", max_prime_ind, "latest_fact", latest_fact, "#partitions", len(parts), "fact_inds", fact_inds)
    global count
    count += 1
    if count%print_period==0:
        print_progress(fact_inds, q, count, len(parts))
    SP = 0 #Track the sum of abcd at this level in the q tree
    for part in parts:
        SP += sum_abcd(part)
    for new_max_prime_ind, new_fact in zip(range(max_prime_ind, len(primes)), primes[max_prime_ind:]):
        new_q = q*new_fact
        if new_q > n:
            #Stop when the area of the quad will be greater than n
            break
        SP += next_factor(new_q, new_max_prime_ind, new_fact, apply_parts_to_all(parts,new_fact), fact_inds.copy()+[new_fact])
    #Return the summed score from this q (area) of quad
    return SP


#Create partitions of 2^4 = 16
starting_parts = apply_parts((1,1,1,1), 2)
starting_parts = apply_parts_to_all(starting_parts, 2)
#print("starting_parts",starting_parts)

ans = next_factor(1, 0, 1, starting_parts, [])
print("SP({:,}) = {:,}".format(n,ans))
print("raw:", ans)

#SP(1,000,000) = 2,611,227,421,428