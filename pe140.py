import math

class recurseGenerator:
    def __init__(self, Ax, Ay, Q = [0,0,0,0,0,0]) -> None:
        # Input in the form:
        # Q" The Overall equation is input in the form 0 = Q[0]*x^2 + Q[1]*xy + Q[2]*y^2 + Q[3]*x + Q[4]*y + Q[5]
        # x_n+1 = Ax[0]*x_n + Ax[1]*y_n + Ax[2]
        # y_n+1 = Ay[0]*x_n + Ay[1]*y_n + Ay[2]
        self.Ax = Ax
        self.Ay = Ay
        self.Q = Q
        self.P = [0,0]
    def seed(self, P):
        # P is the starting point in form [x,y]
        # n is number of iterations to print, if 0 will not print & will only return
        self.P = P
        while True:
            yield self.P
            self.P = [self.Ax[0]*self.P[0] + self.Ax[1]*self.P[1] + self.Ax[2],
                    self.Ay[0]*self.P[0] + self.Ay[1]*self.P[1] + self.Ay[2]]
    def printX(self, P):
        i = 0
        for a in self.seed(P):
            if i == 0:
                print(a, "seed", end=" ")
            else:
                print(a, end=" ")
            print("check:", self.checkPrint())
            i = i + 1
            if i >= 10:
                break
    def checkPrint(self):
        # Checks if self.P is acutally a solution to the equation
        zeroCheck = self.Q[0]*self.P[0]**2 + self.Q[1]*self.P[0]*self.P[1] + self.Q[2]*self.P[1]**2 + self.Q[3]*self.P[0] + self.Q[4]*self.P[1] + self.Q[5]
        return zeroCheck

print("ITERATE 1")
iterate1 = recurseGenerator([-9, -4, -14], [-20,-9,-28], [5, 0, -1, 14, 0, 1])
iterate1.printX([2,-7])
iterate1.printX([0,-1])
iterate1.printX([0,1])
iterate1.printX([-4,5])
iterate1.printX([-3,2])
iterate1.printX([-3,-2])

print("")
print("ITERATE 2")
iterate2 = recurseGenerator([-9, 4, -14], [20, -9, 28])
iterate2.printX([2,-7])
iterate2.printX([0,-1])
iterate2.printX([0,1])
iterate2.printX([-4,5])
iterate2.printX([-3,2])
iterate2.printX([-3,-2])

def continuedFraction(r):
    # Find the continued fraction to some level of percision of r
    A = [] # Coefficients of the continued fraction (non-repeated section)
    B = [] # Coefficients of the continued fraction (repeated section)
    N = [r, 1] # Numerator denominator terms
    R = [] # Ratio with decimal
    for n in range(10):
        r = round(N[n] / N[n+1],10)
        if r in R:
            #continued fraction repeats
            i = R.index(r)
            B = A[i:]
            A = A[:i]
            print("Continued fraction repeats.")
            break
        R.append(r)
        A.append(int(N[n] // N[n+1]))
        N.append(N[n] % N[n+1])
        if (abs(N[-1]) <= 10**-13):
            print("Continued fraction terminates.")
            #Continued fraction terminates
            break
    else:
        print("End of continued fraction not found.")
    #Find the convergents
    H = [0, 1] #numerator of the convergents
    K = [1, 0] #denominator of the continued fractions
    for n in range(len(A)):
        H.append(A[n]*H[-1] + H[-2])
        K.append(A[n]*K[-1] + K[-2])
    for n in range(len(B)):
        H.append(B[n]*H[-1] + H[-2])
        K.append(B[n]*K[-1] + K[-2])
    for n in range(len(B)):
        H.append(B[n]*H[-1] + H[-2])
        K.append(B[n]*K[-1] + K[-2])
    print("   Continued fraction:", A, B)
    print("   Convergent numerator  :", H)
    print("   Convergent denominator:", K)
    return(A,B,H,K)
    # print(N)
    # print(R)

def eval(Q, x, y):
    (A,B,C,D,E,F) = Q
    z = A*x**2 + B*x*y + C*y**2 + D*x + E*y + F
    return z

#Guide: https://www.alpertron.com.ar/METHODS.HTM#Hyperb
Q = (5,0,-1,14,0,1) # Orgional equation
(A,B,C,D,E,F) = Q
discriminant = B**2 - 4*A*C
print("discriminant > 0", discriminant)
# Hyperbolic Case
# F != 0
# discriminant not a perfect square 
#GCD = 1, so no division required
print("4 F2 < B2 - 4AC", 4*F**2 < B**2 - 4*A*C)
#solutions of the equation will be amongst the convergents of the continued fraction of the roots of the equation At2 + Bt + C = 0.

#Re-baseline the equation since D, E must = 0
Q = (1, 0, -5, 0 , 0, -44) # Orgional equation
(A,B,C,D,E,F) = Q

discriminant = B**2 - 4*A*C
print("discriminant:", discriminant)
# Let's consider now the case F ≠ 0 and B2 - 4AC not a perfect square.
print("gcd(A, B, C):", math.gcd(A,B,C))
print("4*F^2:", 4*F**2)

S = []
for s in range(0,F, F//abs(F)):
    if (A*s**2 + B*s + C)%F == 0:
        S.append(s)
print("S satisfying (A*s**2 + B*s + C) mod F == 0: ", S)

#continued fraction expansions of the roots of -(As2 + Bs + C) t2 / F + (2As + B)t - AF = 0
pairs = set() #set of x,y pairs that satisfy the equations
for s in S:
    a = -1*(A*s**2 + B*s + C) // F
    b = (2*A*s + B)
    c = -1*A*F
    print("solve ({})t**2 + ({})t + ({}) = 0".format(a,b,c))
    #Find continued fractions of the equation
    #Positive case
    t = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
    (_, _, H, K) = continuedFraction(t)
    for (y,z) in zip(H[2:], K[2:]):
        x = s*y - F*z
        print("x:", x, "y:", y, "eq:", eval(Q,x,y))
    for (z,y) in zip(H[2:], K[2:]):
        x = s*y - F*z
        print("x:", x, "y:", y, "eq:", eval(Q,x,y)) 
    #Negative case
    t = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
    (_, _, H, K) = continuedFraction(t)
    for (y,z) in zip(H[2:], K[2:]):
        x = s*y - F*z
        print("x:", x, "y:", y, "eq:", eval(Q,x,y))
    for (z,y) in zip(H[2:], K[2:]):
        x = s*y - F*z
        print("x:", x, "y:", y, "eq:", eval(Q,x,y))



# TRY AGAIN
# A New Look at an Old Equation
# R. E. Sawilla, A. K. Silvester & H. C. Williams 
# Conference paper
# Part of the Lecture Notes in Computer Science book series (LNTCS,volume 5011)
# https://link.springer.com/chapter/10.1007/978-3-540-79456-1_2

print()
print("######################################################")
print()

Q = (5,0,-1,14,0,1) # Orgional equation
(a,b,c,d,e,f) = Q
D = b**2 - 4*a*c
print("D:", D, "-> Case 2")
alpha = 2*c*d - b*e
beta = 2*a*e - b*d
Delta = D # Save the origional discriminant
k = -D*(a*e**2 - b*e*d + c*d**2 + f*D)
print("alpha {}, beta {}, k {}".format(alpha, beta, k))
# t = math.gcd(a,b,c)
# print("t", t, "-> Case d.ii")

# print("Find least positive solution of phi**2 - {}*psi**2 = 1".format(D))
# (phi, psi) = (9,2)
# print("phi: ", phi, ", psi:", psi, "check", phi**2 - D*psi**2 == 1)
# print("multiply fundamental solution", a*phi**2 + b*phi*psi + c*psi**2)

# print(phi + alpha, psi + beta)

# print()
# for (F,G) in [(1,0), (-1,0), (phi, psi), (-phi, -psi)]:
#     print("F: {}, G: {}".format(F,G))
#     (gamma, epsilon) = (phi, psi)
#     delta = -(c*epsilon + (b/2)*gamma)
#     zeta = (b/2)*epsilon + a*gamma
#     print((gamma*F + delta*G + alpha)/D, (epsilon*F + zeta*G + beta)/D)

print()
# https://crypto.stanford.edu/pbc/notes/ep/pell.html

D = a
N = -k
print("x**2 - (D:{})*y**2 = (N:{})".format(D,N))

P = (9,4)
(t,u) = P
print("Pell Solution for D = {}: {}".format(D, (t,u)))

L1 = math.sqrt(-N/D)
L2 = math.sqrt(-N*(t+1)/(2*D)) * 2 #Completely arbitrary * 2 here since we seem to miss a fundamental solution...
print("L1: {}, L2: {}".format(L1,L2))
fundamental_solutions = []
for y in range(int(L1), int(L2) + 1):
    try:
        x = math.sqrt(N + D*y**2)
        if x == int(x):
            x = int(x)
            Qp = (-c,0,-a,0,0,-N)
            print((x,y), "test", x**2 - (D)*y**2 == (N))
            if eval(Qp,x,y) == 0:
                fundamental_solutions.append((x,y))
            if eval(Qp,-x,y) == 0:
                fundamental_solutions.append((-x,y))
            if eval(Qp,x,-y) == 0:
                fundamental_solutions.append((x,-y))
            if eval(Qp,-x,-y) == 0:
                fundamental_solutions.append((-x,-y))
    except:
        pass
print("fundamental solutions", fundamental_solutions)

print("Recursion: x' = ({})x + ({})y, y' = ({})x + ({})y".format(t, D*u, u, t))

def next_solution(X, P):
    # X = (x,y) previous solution
    # P = (t,u) solution to the pell equation
    (x,y) = X
    (t,u) = P
    X = (t*x + D*u*y, u*x + t*y)
    return X

xy_fundamental = []

#By inspection, every other solution of the usable roots results in a solution -> Sometimes the odd roots, sometimes the even roots
#Solutions are strictly increacing (by inspection), removed solutions that are strictly decreasing
#Create generators that will produce results & then can be manipulated for ordered results
def generator_even(Q, F, P):
    # Q = coefficeints for checking the results
    # F = (x,y) the fundamental solution
    # P = (t,s) the pell solution
    X = F
    # 1) swap x & y
    (y,x) = X
    # 2) use alpha, beta translation
    Xf = ((x+alpha)//Delta, (y+beta)//Delta)
    if eval(Q, *Xf) != 0:
        # See if it's the odd solutions
        X = next_solution(X,P)
        (y,x) = X
        Xf = ((x+alpha)//Delta, (y+beta)//Delta)
        if eval(Q, *Xf) != 0:
            raise Exception("Attempted to return broken evaluation in generator, fundamental.")
    yield Xf #First solution is the fundamental solution
    while True:
        # Return every other result
        for _ in range(2):
            X = next_solution(X,P)
        #Translate the answer
        # 1) swap x & y
        (y,x) = X
        # 2) use alpha, beta translation
        Xf = ((x+alpha)//Delta, (y+beta)//Delta)
        #Yield the answer
        if eval(Q, *Xf) != 0:
            raise Exception("Attempted to return broken evaluation in generator, following.")
        yield Xf

def eval_translate(X, fundamental_flag = False):
    # Find translated solution
    # 0) Test solution
    print("eval", eval((-c,0,-a,0,0,-N), *X), end=" ")
    # 1) swap x & y
    (y,x) = X
    # 2) use alpha, beta translation
    (xf, yf) = ((x+alpha)/Delta, (y+beta)/Delta)
    print("->", (xf,yf), end=" ")
    # Add fundamental solution
    if all([int(z) == z for z in [xf,yf]]):
        if fundamental_flag:
            xy_fundamental.append((int(xf),int(yf)))
            # xy_generators.append(generator_even(Q,X,P))
        # 3) Check
        print("eval:", eval(Q,int(xf),int(yf)))
        # 4) Check if they satisfy the origional equation -> They always do because x only needs to be rational, and this is a rational solution
        # x === A
    else:
        print()
        pass

for F in fundamental_solutions:
    print(F, end=" ")
    eval_translate(F, fundamental_flag=True)
    X = F
    for _ in range(10):
        Xp = next_solution(X, P)
        if all(xp < x for xp, x in zip(Xp, X)):
            break
        X = Xp
        print("     ", Xp, end=" ")
        eval_translate(Xp)
    else:
        pass



print()
print("Fundamental solutions:", fundamental_solutions)

#Create the generators
xy_generators = []
for F in fundamental_solutions:
    xy_generators.append(generator_even(Q, F, P))

print("Generators", len(xy_generators))

# Iterate throug generators, picking higher and higher cutoffs until the desired number of solutions are found
golden_nuggets = []
cutoff = 10
golden_nuggets_target = 30
while len(golden_nuggets) < golden_nuggets_target:
    cutoff = cutoff * 10
    last_AGs = [0 for _ in xy_generators]
    for i, gen in enumerate(xy_generators):
        last_AG = last_AGs[i]
        if last_AG > cutoff:
            break
        if last_AG < 0:
            break
        for (AG,BG) in gen:
            last_AGs[i] = AG
            golden_nuggets.append(AG)
            print((BG,AG))
            if abs(AG) > cutoff:
                break
    print("all", golden_nuggets)
    #Filter the golden nuggets
    golden_nuggets = set(golden_nuggets)
    golden_nuggets = [gn for gn in golden_nuggets if gn >= 0 ]
    golden_nuggets = sorted(golden_nuggets)
    print("reduced", golden_nuggets)
    print()
print("20th",golden_nuggets[20], "")
print("ans", sum(golden_nuggets[0:31]))