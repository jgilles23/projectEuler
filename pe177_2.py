# %%
import math

def sin(x):
    return math.sin(math.radians(x))
def cos(x):
    return math.cos(math.radians(x))
def asin(x):
    return math.degrees(math.asin(x))

tolerance = 10**-9

# %%
#standard form, small angles
#(b, bp, c, cp, d, dp, a, ap), alpha exists separatly

count = 0
for alpha in range(1,180):
    print_flag = True
    for b in range(1,180):
        ap = 180-alpha-b
        if ap < 1 or ap > 178 or ap > b:
            continue
        AO = sin(b)/sin(180-alpha-b)
        for a in range(1, b+1):
            dp = alpha - a
            if dp < 1 or dp > 178 or dp > b:
                continue
            DO = sin(a)*AO/sin(alpha-a)
            for d in range(1,b+1):
                cp = 180-d-alpha
                if cp < 1 or cp > 178 or cp > b:
                    continue
                CO = sin(d)*DO/sin(180 - alpha - d)
                BC = math.sqrt(1 + CO**2 - 2*CO*cos(180-alpha))
                if CO < 1:
                    bp_raw = asin(CO*sin(180-alpha)/BC)
                    bp = round(bp_raw)
                    if abs(bp_raw - bp) >= tolerance:
                        continue
                    c = alpha - bp
                else:
                    c_raw = asin(sin(180-alpha)/BC)
                    c = round(c_raw)
                    if abs(c_raw - c) >= tolerance:
                        continue
                    bp = alpha - c
                angles = (b, bp, c, cp, d, dp, a, ap)
                # Test if in maximum format e.g. perfect
                options = \
                    [tuple(angles[i:] + angles[:i]) for i in range(0,8,2)] + \
                    [tuple(angles[i::-1] + angles[:i:-1]) for i in range(1,8,2)]
                if angles != max(options):
                    continue
                #Made it here, e.g. this is a valid solution
                count += 1
                if print_flag:
                    print("alpha: {}, (b: {}, bp: {}, c: {}, cp: {}, d: {}, dp: {}, a: {}, ap: {})".format(alpha, *angles))
                    # print("BO: 1, AO: {}, DO: {}, CO: {}, BC: {}".format(AO, DO, CO, BC))
                    print_flag = False

print("ans", count)
# %%
