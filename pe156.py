import math

def brute_count(n, d):
    #Count digits up to and including n
    d = str(d)
    count = 0
    for a in range(0,n+1):
        count += str(a).count(d)
    return count

def brute_recurse(n, d):
    if n == 0:
        return 0
    e = int(math.log10(n))
    a  = n//10**e
    b = n - a*10**e
    count = a*brute_recurse(10**e - 1, d) + brute_recurse(b, d)
    if a == d:
        count += b + 1
    elif a > d:
        count += 10**e
    return count

def fast_digit(n, d):
    count = 0
    string_n = str(n)
    # last i = 0 special case
    if int(string_n[-1]) >= d:
        count += 1
    for i in range(1, len(string_n)):
        if n == 10:
            pass
        n_i = int(string_n[-i-1])
        count += n_i*i*10**(i-1)
        if n_i == d:
            count += int(string_n[-i::]) + 1
        elif n_i > d:
            count += 10**i
    return count

def fast_h(n, d):
    return n - fast_digit(n, d)


f = brute_recurse

N = 4000
d = 1
# print(brute_count(N,2))
# print(N - brute_recurse(N,d))
print("h({}): {}".format(N, N - fast_digit(N,d)))

def find_max(n_min, n_max, d, weights=[], level=0):
    # Exit when n_max is 0
    if n_max <= 9:
        if weights[-1] <= 0:
            print("    "*level + "Found: n: 0, total: 0")
            return 0, 0 #total, number
        elif n_max >= d:
            print("    "*level + "Found: n: {}, total: {}".format(n_max, weights[-1]*n_max + 1))
            return n_max, weights[-1]*n_max - 1
        else:
            print("    "*level + "Found: n: {}, total: {}".format(n_max, weights[-1]*n_max))
            return n_max, weights[-1]*n_max #total, number
    # Find the max h(n) for n in range [n_min, n_max]
    E = int(math.log10(n_max))
    if len(weights) ==0:
        weights = tuple([int(10**(e-1)*(10-e)) for e in range(E+1)])
    print("    "*level + "(n_min: {}, n_max: {}), weights: {}".format(n_min, n_max, weights[::-1]))
    sub_options = {} #Dict of digit to lower weights, can delete unused weights
    # Iterate through the possible digits
    for digit in range(int(str(n_min)[0]), int(str(n_max)[0]) + 1):
        total = weights[-1]*digit
        if digit < d:
            # Sub weights not updated
            sub_weights = weights[:-1]
            # Total + 0
        elif digit == d:
            sub_weights = tuple([w - 10**e for w, e in zip(weights[:-1], range(0, E))])
            # Total adjusted by -1
            total -= 1
        else: # digit > d
            sub_weights = weights[:-1]
            # Total adjusted by power of 10
            total -= 10**E
        #Get the sub max
        if digit == int(str(n_max)[0]):
            sub_max = int(str(n_max)[1:])
        else:
            sub_max = 10**(E) - 1
        #Save the option
        sub_options[digit] = {"total": total, 
                              "weights": sub_weights,
                              "n_max": sub_max}
        print("    "*level + "    digit: {}, total: {}, weights: {}, n_max: {}".format(digit, sub_options[digit]["total"], sub_options[digit]["weights"][::-1], sub_options[digit]["n_max"]))
    # Eliminate redundant guesses
    # OF the form (weights, n_max):(total,digit)
    options_by_parameters = {}
    for digit in sub_options:
        t = (sub_options[digit]["weights"], sub_options[digit]["n_max"])
        if t in options_by_parameters:
            if options_by_parameters[t][0] < sub_options[digit]["total"]:
                options_by_parameters[t] = (sub_options[digit]["total"], digit)
        else:
            options_by_parameters[t] = (sub_options[digit]["total"], digit)
    print("    "*level + "  Iterate on the following")
    #Sub_iterate through the sub_options
    best_total = -1*math.inf
    best_n = 0
    for t in options_by_parameters:
        sub_weights, sub_max = t
        total, digit = options_by_parameters[t]
        print("    "*level + "    digit: {}, total: {}, weights: {}, n_max: {}".format(digit, total, sub_weights[::-1], sub_max))
        sub_total, sub_digits = find_max(0, sub_max, d, sub_weights, level+1)
        new_n = sub_digits + digit*10**E
        new_total = sub_total + total
        if new_total > best_total:
            best_total = new_total
            best_n = new_n
    print("    "*level + "Found: n: {}, total: {}".format(best_n, best_total))
    return best_total, best_n


class Extremes:
    def __init__(self):
        self.min_n = 0
        self.min_h = math.inf
        self.max_n = 0
        self.max_h = -1*math.inf
    
    @property
    def min(self):
        return (self.min_n, self.min_h)
    @property
    def max(self):
        return (self.max_n, self.max_h)
    
    def update(self, n, h):
        #Update min & max with an "n" and and "h" = n - f(n,d)
        if h < self.min_h:
            self.min_h = h
            self.min_n = n
        if h > self.max_h:
            self.max_h = h
            self.max_n = n
    
    def str_n_h(self, n_h_tuple):
        return "(n: {:,}, h: {:,})".format(*n_h_tuple)

    def str_min(self):
        return "Min: {}".format(self.str_n_h(self.min))
    
    def str_max(self):
        return "Max: {}".format(self.str_n_h(self.max))
    
    def __repr__(self):
        return self.str_min() + ", " + self.str_max()



def find_extremes_brute(n_min, n_max, d):
    # Brute force find maximum in [n_min, n_max]
    extremes = Extremes()
    for n in range(n_min, n_max+1):
        h = fast_h(n, d)
        extremes.update(n, h)
    # print("Max: (n: {}, h: {})".format(best_n, max_h))
    return extremes


def apply_sieve(n, d, mode="min"):
    if mode == "min":
        fill = "9"
    else: # mode == "max"
        fill = "0"
    str_n = str(n)
    L = len(str_n)
    str_d = str(d)
    options = []
    for i in range(len(str_n)):
        options.append(str_n[:i] + str_d + fill*(L - i - 1))
    options.append(str_n)
    options = [int(x) for x in options]
    # print(options)
    return options

def get_extremes(n_min, n_max, d):
    options_min = apply_sieve(n_min, d, "min") + apply_sieve(n_max, d, "min")
    options_max = apply_sieve(n_min, d, "max") + apply_sieve(n_max, d, "max")
    options = options_min + options_max
    # print(options)
    extremes = Extremes()
    for option in options:
        if option >= n_min and option <= n_max:
            extremes.update(option, fast_h(option, d))
    # print("Max: (n: {}, h: {})".format(max_n, max_total))
    return extremes, options

def test(n_min, n_max, d):
    extremes, options = get_extremes(n_min, n_max, d)
    modifiers = ["<"*(x < n_min) + ">"*(x > n_max) + "*v"*(x == extremes.min_n) + "*^"*(x == extremes.max_n) for x in options]
    options_with_modifiers = ["{}{:,}".format(x,y) for x,y in zip(modifiers, options)]
    brute_extremes = find_extremes_brute(n_min, n_max, d)
    "< > *v *^"
    print("[{:,}, {:,}], {}, Options: [{}]".format(n_min, n_max, extremes, ", ".join(options_with_modifiers)))
    if extremes.min_h != brute_extremes.min_h or extremes.max_h != brute_extremes.max_h:
        raise Exception("Different answer than brute force method")
    

d = 3
test(27940, 450000, d)



# find_max_brute(100, 899, d)
# find_max(100,899,d)
# print("0"*-1 == "")

