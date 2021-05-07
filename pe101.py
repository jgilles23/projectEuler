#Projetc Euler problem 101
import numpy as np
#numpy.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
#numpy.polyval(p, x)

def fit(ys):
    #Find OP of a sequence
    f = np.polyfit(range(1,len(ys)+1), ys, len(ys)-1)
    f = np.around(f,5) #Round away floating point errors
    start = 0
    while f[start]==0.0: 
        start += 1
    return f[start:]

def gen(coef):
    #Generate sequence from coeficients
    vals = np.polyval(coef, range(1,len(coef)+1))
    return vals

def val_at(coef,x):
    val = np.polyval(coef,x)
    return val

def FIT(coef, correct_coef):
    #Find the fist incorrect term of poly coef aganist correct_coef
    if len(coef) == len(correct_coef):
        return None
    k = len(coef)+1
    while val_at(coef,k) == val_at(correct_coef,k):
        k += 1
        print("UNEXPECTED Got into this while statement")
    return val_at(coef,k)

def sum_FIT(correct_coef):
    #Find the sum of the incorrect fits
    s = 0
    correct_vals = gen(correct_coef)
    for k in range(1,len(correct_vals)):
        coef = fit(correct_vals[:k])
        s += FIT(coef,correct_coef)
    return s

def val_exact(coef,x):
    return sum([c*x**i for i,c in enumerate(coef[::-1])])

def FIT_exact(coef,k):
    #print("input coef", coef)
    #Find first incorrect term for k degree polynomial
    x = k + 1 #ANCHOR
    a = 0 #tracked sum
    for i in range(0,k):
        x_i = i + 1
        b_num = 1 #Rolling numerator
        b_den = 1 #Rolling denominator
        for j in range(0,k):
            if i == j:
                continue
            x_j = j + 1
            #print("i = {:}, j = {:}".format(i,j))
            #print("x_i,x_j",x_i,x_j)
            b_num *= (x) - x_j
            b_den *= x_i - x_j
        y_i = val_exact(coef,x_i)
        #print("y_i",y_i)
        #print("a,b_num,y,b_den",a,b_num,y,b_den)
        b = b_num*y_i//b_den #product value
        if (b_num*y_i/b_den) != b:
            raise Exception("Got a non-integer...")
        a += b
    return a

test_vals = np.array([1,8,27,64,125,216], dtype=np.float64)
given_coef_int = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
given_coef = np.array(given_coef_int, dtype=np.float64)
#given_coef = fit(test_vals)
#given_coef_int = [int(w) for w in given_coef]
print("given_coef",given_coef)

print("Algo with floating point errors:")
ans = sum_FIT(given_coef)
print("ans", ans)

print("Algo with exact integer math:")
s = 0
for k in range(1,len(given_coef_int)):
    q = FIT_exact(given_coef_int,k)
    #print(q)
    s += q

print("ans", s)