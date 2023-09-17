# %%
import sympy
import math
# %%
a,b,E,F, En, Fn = sympy.symbols("a b E F En Fn")
En_eq = (a+1)*E + ((a+1)*(b-1) + 1)*F
Fn_eq = a*E + (a*(b-1) + 1)*F
# %%
temp_dict = sympy.solve([En_eq - En, Fn_eq - Fn], [E, F])
E_eq = sympy.simplify(temp_dict[E])
F_eq = sympy.simplify(temp_dict[F])
# %%
E_eq_0 = E_eq.subs(b, 0)
F_eq_0 = F_eq.subs(b, 0)
E_eq_1 = E_eq.subs(a, 0)
F_eq_1 = F_eq.subs(a, 0)
# %%
def bin_to_EF(binary, print_flag=False):
    #Input binary in raw format
    e,f = 1,1
    for x in binary:
        e,f = En_eq.subs([(E,e), (F,f), (a, int(x=="0")), (b, int(x=="1"))]), Fn_eq.subs([(E,e), (F,f), (a, int(x=="0")), (b, int(x=="1"))])
        if print_flag: print((e,f))
    return e,f

# %%
bin_to_EF(bin(240)[2::])
# Solve in terms of making F & E equal
a_eq_0 = sympy.solve(E_eq_0 - F_eq_0, a) #No return 
b_eq_1 = sympy.solve(E_eq_1 - F_eq_1, b)[0] # E > F seems to be the controlling factor
# Solve in terms of making F = 1?
a_eq_0 = sympy.solve(F_eq_0 - 1, a)
sympy.solve(E_eq_0 - 1, a)

E_eq_0 - F_eq_0 #E > F, E - F > 0, always true
E_eq_1 - F_eq_1

# %%

def test(e,f, digit, allow_small_E=False):
    # digit of zero or 1,
    # return a flag, then e and f
    # flag indicates success in using the digit
    subs = [(En, e), (Fn, f), (a, int(digit==0)), (b, int(digit==1))]
    e_temp,f_temp = E_eq.subs(subs), F_eq.subs(subs)
    #Test for completion
    if e_temp == 1 and f_temp == 1:
        return True, e_temp, f_temp
    #Otherwise test normal things
    if e_temp >= 1 and f_temp >= 1 and (e_temp > f_temp or allow_small_E):
        return True, e_temp, f_temp
    # Failed, don't mutate e & f
    return False, e_temp, f_temp


def EF_to_bin_slow(e,f, print_flag=False, binary=""):
    #Need to establish initial binary elsewhere
    print((e,f))
    #Back calculate a binary from e & f
    while True:
        ret0 = test(e,f,0)
        ret1 = test(e,f,1)
        if ret0[0] and ret1[0]:
            raise Exception("Both true")
        elif ret0[0]:
            binary = "0" + binary
            e,f = ret0[1:3]
            if print_flag: print("0", (e, f), "reject 1", ret1[1:])
        elif ret1[0]:
            binary = "1" + binary
            e,f = ret1[1:3]
            if print_flag: print("1", (e, f), "reject 0", ret0[1:])
        else:
            raise Exception("None true")
        if e == 1 and f == 1:
            break
    return binary

p, q = 123, 321
# binary = EF_to_bin_slow(q, p, print_flag=True)
# print(int(binary, 2), binary)
# p == bin_to_EF(binary)[1]

# %% Need to play with the base asumption on the definition of Ex and Fx
# That could be what is causing errors in some number choices
Ex, Fx, Ey, Fy = sympy.symbols("Ex Fx Ey Fy")
# The final (least significant) digit is the y digit, digit just to the left (more significant) is x
#Zero case (n-1)
subs = [(E, Ex), (F, Fx), (a, 1), (b, 0)]
Ey_eq_0 = En_eq.subs(subs)
Fy_eq_0 = Fn_eq.subs(subs)
P_eq = Fy_eq_0 #Smaller is p
#One case (n)
subs = [(E, Ex), (F, Fx), (a, 0), (b, 1)]
Ey_eq_1 = En_eq.subs(subs)
Fy_eq_1 = Fn_eq.subs(subs)
Q_eq = Fy_eq_1 #Larger is q
#ABOVE does not work because the left side is not always preserved, n & n-1 can end in the same digit
# %%
#More complicated approach with chaining

def process_chain(chain, e=1, f=1):
    #Chain most significat to least significat list of (a,b) where b*ones a*zeros ...
    for link in chain:
        subs = [(E, e), (F,f), (a, link[0]), (b, link[1])]
        e,f = En_eq.subs(subs), Fn_eq.subs(subs)
    return e,f

ay, by = sympy.symbols("ay, by")
#y is the final (least significant) link in the chain
#Process the "n" chain
_, P_eq = process_chain([(ay,by)], Ex, Fx)
#Process the "n-1" chain
_, Q_eq = process_chain([(1,by-1),(0,ay)], Ex, Fx)

#Test values for ay & by; note P, Q need to be > 0 and P > Q

for A in range(4):
    for B in range(4):
        subs = [(ay, A), (by,B)]
        delta_temp = Q_eq - P_eq
        print("(a: {}, b: {}), p: {}, q: {}, 0 < {}".format(A, B, P_eq.subs(subs), Q_eq.subs(subs), delta_temp.subs(subs)))
# Only works when a = 0 and b >= 1
# %%
#When ay=0 and by >= 1; solve for Ex, Fx in terms of P, Q, and by
P, Q = sympy.symbols("P, Q")
temp_dict = sympy.solve([P_eq - P, Q_eq - Q], [Ex, Fx])
Ex_eq = temp_dict[Ex].subs(ay, 0)
Fx_eq = temp_dict[Fx].subs(ay, 0)
#so able to use by up to the point that Ex is just > Fx
by_max_eq = sympy.solve(Ex_eq - Fx_eq, by)[0]
# %%
# Create a branching EF model that allows E < F (as long as >  0)
def branching_EF_to_bin_slow(e,f, print_flag=False, binary=""):
    #Need to establish initial binary elsewhere
    if print_flag: print((e,f))
    if e == 1 and f == 1:
        if print_flag: print(binary)
        return [binary]
    elif e == f:
        return []
    #Back calculate a binary from e & f
    options = []
    for digit in range(2):
        flag, new_e, new_f = test(e,f,digit, allow_small_E=False)
        if new_e >= e and new_f >= f:
            continue
        if flag:
            #Passed, recursive call
            options.extend(branching_EF_to_bin_slow(new_e, new_f, print_flag=print_flag, binary=str(digit)+binary))
    return options

# Solve with a test by >= 1
p, q = 1371, 6548
g = math.gcd(p,q)
p, q = p//g, q//g
print("p: {}, q: {}, g: {}".format(p,q, g))

By_max = by_max_eq.subs([(P, p), (Q, q)])
for By in range(1, 2):
    subs = [(P,p), (Q,q), (by, By)]
    options = branching_EF_to_bin_slow(Ex_eq.subs(subs), Fx_eq.subs(subs),print_flag=True, binary="1"*By)
    print("By:", By, ", SUCCESS", options)
#Test to confirm option success is real
print(p == bin_to_EF(options[0])[1])
# %%

#Try the non branching version for clarity
p, q = 1371, 6548
g = math.gcd(p,q)
p, q = p//g, q//g
print("p: {}, q: {}, g: {}".format(p,q, g))
binary = EF_to_bin_slow(q, p, print_flag=True, binary="1")
print(binary)
print(p == bin_to_EF(binary)[1])

# %%
# math to determine the stopping points, F = 1
stop_a_eq = sympy.solve(F_eq.subs(b, 0) - 1, a)[0]
# E = F
stop_b_eq = sympy.solve(E_eq.subs(a,0) - F_eq.subs(a,0), b)[0]

# %%
#Create a fast version
# Stop for 1s is when f < 1
# Stop for 0s is when e <= f

def fast_pq_to_chain(p, q, print_flag=False):
    # First remove gcd from p, q
    g = math.gcd(p,q)
    f, e = p//g, q//g
    #Always ends in a 1
    chain = [(0,1)]
    while True:
        #Ones first e.g a = 0
        subs = [(En , e), (Fn, f)]
        B = int(stop_b_eq.subs(subs))
        subs += [(a, 0), (b, B)]
        e, f = E_eq.subs(subs), F_eq.subs(subs)
        chain.insert(0, (0, B))
        #Check if finished
        if e==1 and f==1:
            break
        #Add Zeros e.g. b = 0
        subs = [(En , e), (Fn, f)]
        A = int(stop_a_eq.subs(subs))
        subs += [(a, A), (b, 0)]
        e, f = E_eq.subs(subs), F_eq.subs(subs)
        chain.insert(0, (A, 0))
    return chain

def chain_to_sequence(chain):
    #Convert chain into a project euler style sequence
    sequence = []
    most_recent = 0
    for a, b in chain:
        if most_recent == 0:
            if b == 0:
                sequence[-1] += a
                most_recent = 0
            else:
                sequence.append(b)
                if a == 0:
                    most_recent = 1
                else:
                    most_recent = 0
                    sequence.append(a)
        else: #most_recent = 1
            if a == 0:
                sequence[-1] += b
                most_recent = 1
            else:
                if b == 0:
                    most_recent = 0
                    sequence.append(a)
                else:
                    sequence.append(b)
                    sequence.append(a)
                    most_recent = 0
    return sequence

    #Remove zeros
    sequence = [x for x in sequence if x > 0]
    return sequence

p, q = 123456789, 987654321
chain = fast_pq_to_chain(p,q)
print("chain", chain)
print("check", p == process_chain(chain)[1])
sequence = chain_to_sequence(chain)
print("sequnece", sequence)
ans = str(sequence)[1:-1].replace(" ","")
print("ans", ans)

#1,13717420,7,1
# %%

