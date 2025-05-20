'''
PE216 - Primality of 2n^2 - 1
2n^2 - 1 = f
n^2 - 1/2 = f/2
n^2 - 1 = f/2 - 1/2
(n-1)(n+1) = (f-1)/2
2(n-1)(n+1) + 1 = f

2n^2 - 1 = gh
2n^2 - (1 + gh) = 0
n = +-sqrt(-4*2*-(1 + gh))/4
n = +-sqrt(2*(1+f)/2
 > f must be odd --> f = 2*g - 1; for g >= 1
n = +-sqrt(2*(1+2*g - 1)/2
n = +-sqrt(g)
 > g must be a perfect square for n to be an integer --> g = h^2 for h >= 1
n = +-sqrt(h^2)
n = +- h
f = 2*(h^2) - 1 for h >= 1
f = 2h^2 - 1 for h >= 1

t(n) = 2n^2 - 1; when is t(n) prime?
f = (n - 1/sqrt(2))(2*n + sqrt(2))
'''