import itertools
import sympy
import math
N = 9

def find_px(inner, ax, bx, m):
    outx = 0
    while inner % m == 0:
        outx += 1
        inner = inner // m
    px = (n + outx) - (ax + bx)
    return px, inner

overall_count = 0
for n in range(1,N+1):
    count = 0
    solutions = []

    n_bump = int(math.log(1 + 5**n)/math.log(2))
    for a2, b2, a5, b5 in itertools.product(*[range(0,n+n_bump+1) for _ in range(4)]):
        # print((a2,b2,a5,b5))
        # Ensure that a is less than b
        if 2**a2*5**a5 > 2**b2*5**b5:
            continue
        # Calculate the inner value
        # if (a2-b2)*(a5-b5) >= 0:
        #     inner = 2**abs(a2-b2)*5**abs(a5-b5) + 1
        # else:
        #     inner = 2**abs(a2-b2) + 5**abs(a5-b5) + 1
        inner = 2**a2*5**a5 + 2**b2*5**b5
        inner_save = inner
        # Remove 2 and 5 from the inner value to the left side of the equation
        p2, inner = find_px(inner, a2, b2, 2)
        # Now remove fives
        p5, inner = find_px(inner, a5, b5, 5)
        # Halt if p2 or p5 is less than zero
        if p2 < 0 or p5 < 0:
            continue
        # Now discern p_prime and d from inner
        for p_prime in sympy.divisors(inner):
            d = inner//p_prime
            p = 2**p2*5**p5*p_prime
            # Solution found
            a = 2**a2*5**a5*d
            b = 2**b2*5**b5*d
            # print("(a: {:,}, b: {:,}, p: {:,})".format(a,b,p))
            solutions.append((a,b,p))
            count += 1
            if (a,b,p) == (2,2,20):
                pass

    print("n: {:,}, count: {:,}".format(n,count))
    # solutions.sort()
    # print(solutions)
    overall_count += count

print("ans", overall_count)

