#Project Euler #66
from sympy import primefactors
import math

"""
#VERY SLOW and somehow still wrong solution
N = 1000
ans_x = 0
ans_D = 0
for D in range(2,N+1):
    if (D**0.5)%1 == 0:
        #Ignore square numbers
        continue
    print(D,end=": ",flush=True)
    d = primefactors(D)[-1] #get largest prime factor
    k = 1 #iterate through values of k, if k=0, x=1,y=0
    while True:
        x = d*k - 1
        y = ((x**2-1)/D)**0.5
        if y%1==0 and y!=0:
            y = int(y)
            break
        x = d*k + 1
        y = ((x**2-1)/D)**0.5
        if y%1==0 and y!=0:
            y = int(y)
            break
        k += 1
    if x > ans_x:
        ans_x = x
        ans_D = D
    print("({x:,})^2 - {D:}x({y:,})^2 = 1".format(D=D,x=int(x),y=y))

print("max x",ans_x,"D", ans_D)

#max x 23596759470 D 991
"""


def closest_square(D):
    #Minimize |m^2 - D|, return m
    z = math.sqrt(D)
    x = abs(math.floor(z)**2 - D)
    y = abs(math.ceil(z)**2 - D)
    if x < y:
        return math.floor(z)
    else:
        return math.ceil(z)

def find_m(D,a,b,k):
    #find m>0 s.t. a+bm|k and |m^2 - D| is minimal
    #search down - until a solution is found
    m = int(D**0.5)
    residual = math.inf
    while m > 0:
        if (a + b*m)%k == 0:
            best_m = m
            residual = abs(m**2 - D)
            #print("Found solution down at m = {:}, residual {:}".format(best_m,residual))
            break 
        m -= 1
    #search up - only until 
    m = int(D**0.5) + 1
    while abs(m**2 - D) < residual:
        if (a + b*m)%k == 0:
            best_m = m
            residual = abs(m**2 - D)
            #print("Found solution up at m = {:}, residual {:}".format(best_m,residual))
            break 
        m += 1
    #m has been found
    return best_m

def iterate(D,a,b,k):
    m = find_m(D,a,b,k)
    new_a = (a*m + D*b)//abs(k)
    new_b = (a + b*m)//abs(k)
    new_k = (m**2 - D)//k
    return(D,new_a,new_b,new_k)

def solve(D):
    #Solve the equation a^2 - D*b^2 = 1
    #For integers a,b
    a = int(D**0.5)
    b = 1
    k = a**2 - D*b**2
    i = 1
    while k != 1:
        D,a,b,k = iterate(D,a,b,k)
        i += 1
    print("D:{D:} ({x:,})^2 - {D:}x({y:,})^2 = 1, in {i:} iterations".format(D=D,x=a,y=b,i=i))
    return a,b


max_x = 0
D_ans = 0
for D in range(2,1000):
    if (D**0.5)%1 == 0:
        continue
    x,y = solve(D)
    if x > max_x:
        max_x = x
        D_ans = D

print("max_x", max_x,"D_ans",D_ans)




