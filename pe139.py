import sympy
a,b,c,d,k = sympy.symbols("a b c d k")
b = d + a
c = k*d
pythag = a**2 + b**2 - c**2
q = sympy.solvers.solvers.solve(pythag, a)
print(q)