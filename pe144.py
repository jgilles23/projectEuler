import sympy
import math
sympy.init_printing(use_unicode=True)




class Rational:

    def __init__(self, numerator, denominator):
        #n & d represent the factors of the numerator and denominator in dictionary format
        self.n = numerator
        self.d = denominator
        self.dfact = {}

    def simplify(self):
        # Simplify the rational number
        for i in self.n:
            if i in self.d:
                if self.n[i] > self.d[i]:
                    self.n[i] -= self.d[i]
                    del self.d[i]
                elif self.n[i] < self.d[i]:
                    self.d[i] -= self.n[i]
                    del self.n[i]
                else:
                    del self.n[i]
                    del self.d[i]

    def __str__(self):
        return "[{:}/{:}]".format(self.n, self.d)
    
    def __add__(self, rational):
        return Rational(self.n*rational.d + rational.n*self.d, self.d*rational.d)
    
    def __sub__(self, rational):
        return Rational(self.n*rational.d - rational.n*self.d, self.d*rational.d)
    
    def __truediv__(self, rational):
        return Rational(self.n*rational.d, self.d*rational.n)

# elipse 4x**2 + y**2 = 100
# (A,B) = sympy.Rational(5,1), sympy.Rational(10,1)

# Solve the quadratic equation
p = (0.0, 10.1)
q = (1.4, -9.6)

bounce_count = 0
while True:
    bounce_count += 1
    if bounce_count%1000 == 0:
        print("Bounce", bounce_count)
    #Get the new slope
    slope_old = (q[1] - p[1])/(q[0] - p[0])
    slope_elipse = -4*q[0]/q[1]
    slope_new = (2*slope_elipse - slope_old + slope_elipse**2*slope_old)/(1-slope_elipse**2+2*slope_elipse*slope_old)

    #Solve linear
    m = slope_new
    b = q[1] - q[0]*m
    # print("y = (m: {})x + (b: {})".format(m,b))
    #Solve the quadratic
    A = 4 + m**2
    B = 2*m*b
    C = b**2 - 100
    # print((A,B,C))

    k = sympy.sqrt(B**2 - 4*A*C)
    # print("k", k.evalf())

    x_new = (-B + k)/(2*A)
    if abs(x_new - q[0]) < 10**-10:
        x_new = (-B - k)/(2*A)
    y_new = m*x_new + b

    r = (x_new, y_new)
    # P.append(r)
    print("New point: ({:.4}, {:.4})".format(*r))
    if r[0] <= 0.01 and r[0] >= -0.01 and r[1] > 0:
        print("break free", r)
        break

    # Reset p & q
    p = q
    q = r

print("ans", bounce_count)



# a,b,c,d,e,f,g,h = sympy.symbols("a b c d e f g h", positive=True)
# (x1, y1) = (a/b, c/d)
# (x2, y2) = (e/f, g/h)
# m12 = (y2-y1)/(x2-x1)
# b = y1 - m12*x1
# k = (4*m12**2*b**2 - 4*(4 + m12**2)*(b**2 - 100))
# k_expand = sympy.simplify(sympy.expand(k))
# print("Full: ", k_expand)

# numerator = 16*(-a**2*d**2*f**2*g**2 + 100*a**2*d**2*f**2*h**2 + 2*a*b*c*d*e*f*g*h - 200*a*b*d**2*e*f*h**2 - b**2*c**2*e**2*h**2 + 25*b**2*c**2*f**2*h**2 - 50*b**2*c*d*f**2*g*h + 100*b**2*d**2*e**2*h**2 + 25*b**2*d**2*f**2*g**2)
# numerator = sympy.factor(numerator)
# print("Numerator", numerator)

# denominator = (d**2*h**2*(a**2*f**2 - 2*a*b*e*f + b**2*e**2))
# denominator = sympy.factor(denominator)
# denominator = sympy.simplify(sympy.sqrt(denominator))
# print("Denominator", denominator)

# print("16*(-a**2*d**2*f**2*g**2 + 100*a**2*d**2*f**2*h**2 + 2*a*b*c*d*e*f*g*h - 200*a*b*d**2*e*f*h**2 - b**2*c**2*e**2*h**2 + 25*b**2*c**2*f**2*h**2 - 50*b**2*c*d*f**2*g*h + 100*b**2*d**2*e**2*h**2 + 25*b**2*d**2*f**2*g**2)/(d**2*h**2*(a**2*f**2 - 2*a*b*e*f + b**2*e**2))".replace("**","^").replace("*",""))

