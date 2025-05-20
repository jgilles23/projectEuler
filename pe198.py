'''
PE198 - Ambiguous Numbers

best approcimation to a real number x for denominator abound d is rational number r/s with s <= d
such that any rational number p/q which is closer to x than r/s has a denominator greater than d.
q > d

9/40 is either 1/4 or 1/5 for bound 6 => ambiguous number
9/40 = 0.225 (right in the middle of 1/4 and 1/5)
1/4 = 0.25
1/5 = 0.2

this has something to do with primes and reducability
9/40, 8/40 = 1/5; 10/40 = 1/4
Would mean that there are no other fractions with a denominator less than 40 that are closer to 9/40 than 8/40 or 10/40
x/39 = 9/40
# x = 9*39/40 = 8.775

so for a center point of r/s
   Option #1: the ambiguous values are r-z/s and r+z/s; we need to prove what values of z are allowable
   Option #2: the ambiguous values have denominators that are not divisors of s; but they must be less than s; e.g. s and the new divisors must be coprime
        But thier average must be equal to r/s; let a/b be the lower ambigous number and c/d be the upper ambigous number
        Where b and d are coprime to b
        average = (a/b + c/d)/2 = (da + bc) / 2bd = r/s; again where bd are coprime to; assume that the average is not in reduced form and must be divided by g on the top and bottom to equal r and s
        da + bc = gr
        2bd = gs; where db and s are coprime
            Case #1: 2 is a factor of s: bd = g and 2 = s => It is obvious that s = 2 does not have an ambigious case as s = 1 is the only lower denominator
            Case #2: 2 is not a factor of s: 2bd = g and 1 = s; => It is obvious that s = 1 does not have an ambigious case as there is no lower denominator
Only Option #1 is valid; so we need to find the values of z that are allowable
    r-z and r+z must not be coprime to s; aka the fraction needs to be reducable; and their average must be equal to r/s
    r must be coprime to s
Maybe we should check the divisors of a particular number to get our result
    so for 40 divisors are: 1, 2, 4, 5, 8, 10, 20, 40; so we want to look at pairs of divisors

How to test if c/d is closer to r/s than a/b
abs(c/d - s/t) ?= abs(a/b - s/t)
abs(ct - sd / d) ?= abs(at - sb / b)
abs(b(ct - sd)) ?= abs(d(at - sb)) if left is smaller, its allowed, if equal its ambiguous, if bigger it's excluded

'''

import math

def continuedFraction(r, s):
    #Compute the continued fraction of r/s
    cf = []
    while s != 0:
        cf.append(r // s)
        r, s = s, r % s
    return cf

def bestRationalApproximations(r, s):
    #Compute the best rational approximations of r/s
    cf = continuedFraction(r, s)
    print("continued fraction", cf)
    h = [0, 1] #numerator
    k = [1, 0] #denominator
    rationalApproximation = []
    excludedApproximation = []
    ambiguousApproximation = []
    #Special case for n = 0 and n = 1
    for n in range(2, len(cf) + 2):
        a = cf[n-2]
        if a%2 == 0 and a > 0:
            half_a = a//2
            #abs(b(cr - sd)) ?= abs(d(ar - sb)) if left is smaller, its allowed, if equal its ambiguous, if bigger it's excluded
            #r/s - c/d ?= a/b - r/s
            #b(dr - sc) ?= d(sa - br);  a = test_h, b = test_k, c = h[-1], d = k[-1]
            test_h = half_a*h[n-1] + h[n-2]
            test_k = half_a*k[n-1] + k[n-2]
            left = abs(test_k*(k[n-1]*r - s*h[n-1]))
            right = abs(k[n-1]*(s*test_h - test_k*r))
            if left > right:
                rationalApproximation.append((test_h, test_k))
            elif left == right:
                rationalApproximation.append((test_h, test_k))
                ambiguousApproximation.append((h[-1], k[-1]))
                ambiguousApproximation.append((test_h, test_k))
            else:
                excludedApproximation.append((test_h, test_k))
        else:
            half_a = a//2
        for sub_a in range(half_a + 1, a):
            rationalApproximation.append((sub_a*h[n-1] + h[n-2], sub_a*k[n-1] + k[n-2]))
        h.append(a*h[n-1] + h[n-2])
        k.append(a*k[n-1] + k[n-2])
        rationalApproximation.append((h[-1], k[-1]))
    print("rational", rationalApproximation)
    print("ambiguous", ambiguousApproximation)
    print("excluded", excludedApproximation)
    return rationalApproximation

def verboseRationalApproximations(r,s):
    cf = continuedFraction(r,s)
    print("continued fraction", cf)
    h = [0, 1]
    k = [1, 0]
    for n in range(2, len(cf)+2):
        a = cf[n - 2]
        print(f"n = {n-2}, a_n = {a}")
        if a == 0:
            #Only applicable on the first pass
            h.append(a*h[n-1] + h[n-2])
            k.append(a*k[n-1] + k[n-2])
            print(f"   a_sub = {a}, best {h[n]}/{k[n]} | zero result | delta {r/s - h[n]/k[n]}")
        elif a % 2 == 0:
            #Special test for a//2
            h_sub = a//2*h[n-1] + h[n-2]
            k_sub = a//2*k[n-1] + k[n-2]
            left = abs(k_sub*(k[n-1]*r - s*h[n-1]))
            right = abs(k[n-1]*(s*h_sub - k_sub*r))
            if left > right:
                print(f" + a_sub = {a//2}, best {h_sub}/{k_sub} | half sub result | delta {r/s - h_sub/k_sub}")
            elif left == right:
                print(f" * a_sub = {a//2}, best {h_sub}/{k_sub} | half sub result AMBIGUOUS | delta {r/s - h_sub/k_sub} **********")
            else:
                print(f" - a_sub = {a//2}, NOT BEST {h_sub}/{k_sub} | half sub result fails | delta {r/s - h_sub/k_sub}")
            #Then continue with the normal test
            for a_sub in range(a//2+1, a):
                h_sub = a_sub*h[n-1] + h[n-2]
                k_sub = a_sub*k[n-1] + k[n-2]
                print(f"   a_sub = {a_sub}, best {h_sub}/{k_sub} | even sub result | delta {r/s - h_sub/k_sub}")
            h.append(a*h[n-1] + h[n-2])
            k.append(a*k[n-1] + k[n-2])
            print(f"   a_sub = {a}, best {h[n]}/{k[n]} | even full result | delta {r/s - h[n]/k[n]}")
        else:
            for a_sub in range(a//2 + 1, a):
                h_sub = a_sub*h[n-1] + h[n-2]
                k_sub = a_sub*k[n-1] + k[n-2]
                print(f"   a_sub = {a_sub}, best {h_sub}/{k_sub} | odd sub result | delta {r/s - h_sub/k_sub}")
            h.append(a*h[n-1] + h[n-2])
            k.append(a*k[n-1] + k[n-2])
            print(f"   a_sub = {a}, best {h[n]}/{k[n]} | odd full result | delta {r/s - h[n]/k[n]}")

# verboseRationalApproximations(49, 40)

def isAmbiguous(r, s):
    cf = continuedFraction(r, s)
    hm2, hm1 = 0, 1
    km2, km1 = 1, 0
    h0 = cf[0] # a[n]*h[n-1] + h[n-2]
    k0 = 1 # a[n]*k[n-1] + k[n-2]
    for n in range(0, len(cf)):
        if cf[n]%2 == 0 and cf[n] > 0 and n > 1:
            #If n is even, check for ambiguity
            test_h = cf[n]//2*hm1 + hm2
            test_k = cf[n]//2*km1 + km2
            left = abs(test_k*(km1*r - s*hm1))
            right = abs(km1*(s*test_h - test_k*r))
            if left == right:
                adjustmentFactor = s//test_k
                adjustedNumerator = test_h*adjustmentFactor
                extra = f"difference is {r - adjustedNumerator}/{s}"
                return True, f"ambiguous, previous {hm1}/{km1} and test {test_h}/{test_k}, n {n}, {extra}", r - adjustedNumerator
        h0 = cf[n]*hm1 + hm2
        k0 = cf[n]*km1 + km2
        hm2, hm1 = hm1, h0
        km2, km1 = km1, k0
    return False, "normal", 0

N = 50
frac = 1
for r in range(1,N):
    for s in range(max(r+1, r*frac), N):
        if math.gcd(r,s) == 1:
            flag, result, delta = isAmbiguous(r,s)
            if flag:
                print(f"{r}/{s} : {result}")
# print(isAmbiguous(9, 40))

#Try 1/101 and 1/51 as the things
#52/101 + 101/52 = /(52*101)
# print(isAmbiguous(3,40))

# verboseRationalApproximations(22,35)

# exit()
'''
For this to be ambiguous we can instead maybe work backwards and build a partial fraction that produces the same results --- maybe not easily
We need to prove that r+1/s and r-1/s are the only options for ambiguous numbers;
    Consider the next option r+2/s can we show that if there is an ambiguous number that the bounds must be greater than x
let's think of it this way... develop a field of numbers <d, and ask, what is the maximum spacing of two numbers in that field
    So we will have points spaced at 1/1, 1/2, 1/3, 1/4, 1/5, 1/6, ... intervals
    so our field would be (0/1, 1/1, 1/2, 2/2, 1/3, 2/3, 3/3, 1/4, 2/4, 3/4, 4/4, 1/5, 2/5, 3/5, 4/5, 5/5, ...)
    On the number line, what is the maximum spacing between two numbers in that field
    No worse than 1/5 - 1/6 = 1/30; so the multiplication of the two denominators
I think we could construct a case where the ambiguous factors are 1/2 and 1/3 by choosing their average as 5/12
    Max gap between these is 1/6; +/- 1/6 = 2*1/6 = 1/12 which is exactly the denominator of thier constructed ambiguous number
    9/40; d=6; 1/6 mean 1/5 = 1/30 
Still working on this proof here, so what if the number is 1/60 then what do we do?
What about 1/2 and 2/3 the average of which is 7/12; therefore 7/12 is ambiguous
Consider two numbers a/d and b/d-1 for these to be the best approximation of r/s they must be the best approximation with d as a bound.
    The average of these two number is (d-1 + d)/(2d(d-1)) = (2d + 1)/(2d^2 - 2d) ~ 1/d; for which this is the best approximation of r/s
    Average is actually [a(d-1) + db]/[2d(d-1)] = (ad - a + bd)/[2d(d-1)]
1) There is a threshold d for which the average of the two numbers could never have a denominator as large as "s"
2) There is a threshold w/s for which any estiamtes must be closer to r/s by w/s than any other option
    It's the d at which any bound of d higher must necessarily have a solution closer to r/s than w/s + r/s

LETS JUST TAKE THE +-1 THING TO BE TRUE FOR REASONS?
    This means that for a given denominator the numerator only works if it has two divisors that are separated by exactly two with the number in the middle not being a divisor
    8/40 9/40 10/40 => 
    '''



def bruteDivisors(x):
    divisors = []
    for i in range(1, x+1):
        if x % i == 0:
            divisors.append(i)
    return divisors

#Let's try a method where we start with the numerator if the fraction & then generate denominators that may work
#Note that all the numerators appear to be odd for some reason and all the denominators appear to be even, not really sure what is up with that
# start with 12 => (11,13) so this may work for 12/(11*13) (but i doubt that it will)
# print(isAmbiguous(11, 5 * 3))
'''
I really must be missing something fundamentally mathmatical here that would make this work like something other than bad
I wonder if there is some sort of matrix of continued fraction parameters that we can solve for that make this work
h
'''

verboseRationalApproximations(7,3)

exit()

import sympy

r, s = sympy.symbols('r s')
A = sympy.symbols('a1 a2 a3 a4')
A = [0] + [*A]
H = [0, 1]
K = [1, 0]
X = []

for n in range(4):
    h_n = A[n]*H[n-1] + H[n-2]
    k_n = A[n]*K[n-1] + K[n-2]
    H.insert(-2, h_n)
    K.insert(-2, k_n)
    X.append(h_n/k_n)
print(H)
print(K)
print(X)

n = 2
half = h_n = (A[n]/2*H[n-1] + H[n-2]) / (A[n]/2*K[n-1] + K[n-2])
zero = -2*r/s + X[n-1] + half
print(sympy.simplify(sympy.expand(zero)))



exit()

#This method does not work because it ignores cases where the numerator of the approximation is something other than 1
frac = 1
def ambiguityCount(s):
    if s == 12:
        pass
    divisors = bruteDivisors(s)
    for i in range(0, len(divisors)-1):
        if divisors[i] + 1 > s//frac:
            print("breaking")
            break 
        if divisors[i+1] - divisors[i] == 2:
            #Check if there is an ambiguous number between them
            flag, result, delta = isAmbiguous(divisors[i]+1, s)
            if flag:
                print(f"{divisors[i]+1}/{s}", result)

for i in range(1, 50):
    ambiguityCount(i)




exit()

