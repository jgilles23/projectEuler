# %%
import sympy
import math

# %%
x, y, z, n = sympy.symbols("x y z n")
f1 = x**(n+1) + y**(n+1) - z**(n+1)
f2 = (x*y + y*z + z*x)*(x**(n-1) + y**(n-1) - z**(n-1))
f3 = x*y*z*(x**(n-2) + y**(n-2) - z**(n-2))

eq = f1 + f2 - f3
eq = sympy.expand(eq)
eq = sympy.collect(eq, [x,y,z])
eq = sympy.factor(eq)
zero_eq = eq.subs(n, 0)

# %%
N = 36
denom = 2**5 * 3**2 * 5**2 * 7*9*11*13*17*19*23*29*31
num_mult = [0] + [denom//i for i in range(1,N+1)]


T = 10

fractions = []
fractions_dict = dict()
for b in range(2,N):
    for a in range(1,b):
        g = math.gcd(a,b)
        if g != 1:
            continue
        fractions.append((a/b, a, b))
        rounded = round(a/b, T)
        for modification in [-10**(-T), 0, 10**(-T)]:
            fractions_dict[rounded + modification] = (a,b)
fractions.sort()
print(fractions)

tolerance = 10**(-T)

s_set = set()

for x, ax, bx in fractions:
    for y, ay, by in fractions:
        if y > x:
            break
        for n in [-2, -1, 1, 2]:
            z = (x**n + y**n)**(1/n)
            rounded_z = round(z, T)
            if rounded_z in fractions_dict:
                az, bz = fractions_dict[rounded_z]
                numerator = ax*num_mult[bx] + ay*num_mult[by] + az*num_mult[bz]
                print("n: {}, (x: {}/{}, y: {}/{}, z: {}/{}), numerator: {}".format(n, ax, bx, ay, by, az, bz, numerator))
                s_set.add(numerator)
            else:
                continue

print("Length s:", len(s_set))
s_sum = sum(s_set)
g = math.gcd(s_sum, denom)
u = s_sum // g
v = denom // g
print("u/v: {}/{}".format(u,v))
print("ans:", u+v)


# %%
