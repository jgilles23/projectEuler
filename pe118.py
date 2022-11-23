from itertools import permutations
import sympy

answers = set()

def recurse_comma(digits, so_far, answers, level):
    # print(" -"*level, "digits", digits, len(digits))
    if len(digits) == 0:
        #found all primes
        so_far.sort()
        # print(" -"*level, "COUNT", so_far)
        answers.add(tuple(so_far))
        return
    for pos in range(1, len(digits)+1):
        n = int("".join(digits[:pos]))
        # print(" -"*level, "test", n, "pos", pos)
        if not sympy.isprime(n):
            # print(" -"*level, "CONTINUE")
            continue
        inner_so_far = so_far + [n]
        recurse_comma(digits[pos:], inner_so_far, answers, level+1)

i = 0
N = 9*8*7*6*5*4*3*2*1
for series in permutations([*"254789631"], 9):
    i += 1
    if i%(1024*16) == 0:
        print(i, "of", N, "(", i/N, ")", "count", len(answers), ":", series)
    recurse_comma(series, [], answers, 1)


print(len(answers))