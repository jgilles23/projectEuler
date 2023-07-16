import sympy
import math

def perfect_square_test(n):
    _, integer_flag = sympy.integer_nthroot(n, 2)
    return integer_flag

def brute_force():
    best_sum = 10**15
    x = 2
    while True:
        x += 1
        if x % 1000 == 0: print("{:,}".format(x), end = " | ")
        if x + 2 + 1 >= best_sum:
            break
        #Iterate through y, explicit x + y
        for k in range(int(math.ceil((x+1)**0.5)), int(math.ceil((2*x)**0.5))):
            y = k**2 - x
            if x+y+1 >= best_sum:
                break
            if not perfect_square_test(x-y): continue
            #iterate through z, explicit y + z
            for j in range(int(math.ceil((y+2)**0.5)), int(math.ceil((2*y)**0.5))):
                z = j**2 - y
                if x+y+z >= best_sum:
                    break
                #Not yet solved
                if not perfect_square_test(x+z): continue
                if not perfect_square_test(x-z): continue
                if not perfect_square_test(y-z): continue
                #Solved already but double check
                if not perfect_square_test(x+y): continue
                if not perfect_square_test(y+z): continue
                #Found something that meets the conditions
                s = x + y + z
                print("")
                print("x y z", x, y, z, "sum", x+y+z)
                if s < best_sum:
                    best_sum = s
    return best_sum

s = brute_force()
print("")
print("ans", s)