import math
#Use the pell equation
#https://mathworld.wolfram.com/PellEquation.html
#Arrange (x(x-1))/(y(y-1)) = 1/2
#Let X = 2y-1, Y = 2x-1
#Then X^2 - 2Y^2 = -1
#Therefore D = 2
#Use pell equation with start of x=15, y=21 therefore X=41, Y=29

def XYn(D,p,q,n):
    plus = (p + q*D**0.5)**n
    minus = (p - q*D**0.5)**n
    Xn = (plus + minus)/2
    Yn = (plus - minus)/2/D**0.5
    xn = (Yn+1)/2
    yn = (Xn+1)/2
    return xn, yn

y = 0
n = 1
while y < 10**12:
    x,y = XYn(D=2, p=1, q=1, n=n)
    print(n, x, y)
    n += 2

print("ans", int(round(x,0)))