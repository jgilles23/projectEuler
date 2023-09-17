import itertools
import math
import sympy

def brute_f(n):
    largest = int(math.log2(n))
    count = 0
    for combination in itertools.product(*[(0, 2**p, 2*2**p) for p in range(largest+1)]):
        if sum(combination) == n:
            count += 1
    return count

def n_to_zipped(n):
    binary = bin(n)[2:]
    stream = [0]
    state = 0
    for b in binary[::-1]:
        if int(b) == state:
            stream[-1] += 1
        else:
            stream.append(1)
            state = (state + 1) % 2
    zipped = [(x,y) for x,y in zip(stream[0::2], stream[1::2])]
    return zipped

def n_to_singleton_zipped(n):
    return [(int(x=="0"),int(x=="1")) for x in bin(n)[2:][::-1]]

def tree_zipped(product, pair, zipped):
    # Take in the product to this point, a pair, zip
    # Return the completed product
    if len(zipped) == 0:
        return product * (pair[0] * pair[1] + 1)
    new_pair = zipped[0]
    total = 0
    #Split into 0 side
    total += tree_zipped(product*pair[0], (new_pair[0] + 1, new_pair[1]), zipped[1:])
    #Split into 1
    total += tree_zipped(product*(pair[0]*(pair[1] - 1) + 1), new_pair, zipped[1:])
    return total
    


def tree_f(n):
    zipped = n_to_zipped(n)
    return tree_zipped(1, zipped[0], zipped[1:])

def binary_zipped(zipped):
    E,F = 1,1
    for a,b in zipped[::-1]:
        E,F = (a + 1)*E + ((a + 1)*(b - 1) + 1)*F, a*E + (a*(b - 1) + 1)*F
        print("EF", (E,F))
    return E, F #Return only the F component

def binary_f(n):
    zipped = n_to_zipped(n)
    E, F = binary_zipped(zipped)
    return F

P = 123456789
Q = 987654321
print(Q-P)

n = 241# int("11100111111000001", 2)
print("n:", n, bin(n), n_to_zipped(n))
# print("brute", brute_f(n))
print("tree ", tree_f(n))
print("bin  ", binary_f(n))
print("regular  ", n_to_zipped(n), binary_zipped(n_to_zipped(n)))
print("singleton", n_to_singleton_zipped(n), binary_zipped(n_to_singleton_zipped(n)))


# Lets do some symbolic math

E, F, En, Fn, a, b = sympy.symbols("E, F, En, Fn, a, b")
zero_E = (a+1)*E + ((a+1)*(b-1) + 1)*F - En
zero_F = a*E + (a*(b-1) + 1)*F - Fn

zero_E = zero_E.subs(b,0)
zero_F = zero_F.subs(b,0)

D = sympy.solve([zero_E, zero_F], [E, F], dict=True)
for key in D[0]:
    print(key, "=", sympy.factor(D[0][key]))

E_solved = D[0][E]
F_solved = D[0][F]

zero_less_equal = E_solved - F_solved
print("0 <= ", zero_less_equal)

print("E = 1 => a = ", sympy.solve(E_solved - 1, a))
print("F = 1 => a = ", sympy.solve(F_solved - 1, a)) 
print("E >= 0")

#F = 1 => a =  [(Fn - 1)/(En - Fn)] USE THIS EQUATION for b = 0

def reverse_zipped(E,F):
    zipped = [(0,1)]
    while True:
        #One mode
        b_float = (E - F)/F
        b = (E - F)//F
        if b >= 1:
            E, F = E - b*F, F
            zipped.append((0,b))
            print("b", b, b_float, "EF", (E,F))
        #Check exit
        if E <= 1 and F <= 1:
            break
        #Zero mode mode
        a_float = (F - 1)/(E - F)
        a = (F - 1)//(E - F)
        if a >= 1:
            E, F = (1-a)*E + a*F, -a*E + (a+1)*F
            print("a", a, a_float, "EF", (E,F))


reverse_zipped(Q,P)

exit()


def reverse_binary(E, F):
    binary_string = "1"
    while E > 1 or F > 1:
        #Try 0
        E0, F0 = F, 2*F - E
        zero_valid = E0 >= 1 and F0 >= 1 and E0 >= F0
        #Try 1
        E1, F1 = E - F, F
        one_valid = E1 >= 1 and F1 >= 1 and E1 >= F1
        #Set E,F to the correct values
        if zero_valid and one_valid:
            raise Exception("Both zero and one found as valid solutions")
        elif zero_valid:
            binary_string = "0" + binary_string
            E,F = E0,F0
        elif one_valid:
            binary_string = "1" + binary_string
            E,F = E1, F1
        else:
            raise Exception("Neither found as valid solution")
    return int(binary_string,2)

# P,Q = 13,17
new_n = reverse_binary(Q,P)
print("reverse binary", n, bin(n))

exit()

def expand(iterable):
    return [sympy.expand(i) for i in iterable]

a0, b0, a1, b1 = sympy.symbols("a0 b0 a1 b1")
before_zipped = [(a0,b0)]
after_zipped = [(0, a0), (1,b0-1)]
before_EF = expand(binary_zipped(before_zipped))
after_EF = expand(binary_zipped(after_zipped))
print("before_EF", before_EF)
print("after_EF", after_EF)
print("delta_EF", [after_EF[0] - before_EF[0], after_EF[1] - before_EF[1]])