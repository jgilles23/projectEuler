import sympy

prime_adders = [1, 3, 7, 9, 13, 27]
not_prime_adders = [5, 11, 15, 17, 19, 21, 23, 25]

N = 150*10**6

s = 0

for n in range(2, N, 2):
    if n % 10**6 == 0:
        print("n: {:,}".format(n))
    n2 = n**2
    for prime_adder in prime_adders:
        if sympy.isprime(n2 + prime_adder) == False:
            break
    else:
        for not_prime_adder in not_prime_adders:
            if sympy.isprime(n2 + not_prime_adder) == True:
                break
        else:
            #Passed all the tests
            s += n
print("ans", s)