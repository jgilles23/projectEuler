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
# print("h({}): {}".format(N, N - fast_digit(N,d)))

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


def apply_sieve(n, L, d, mode="min"):
    # n, number to apply the sieve onz
    # L: length of the sieve
    if mode == "min":
        fill = "9"
    else: # mode == "max"
        fill = "0"
    str_n = str(n).rjust(L, "0")
    str_d = str(d)
    options = []
    for i in range(len(str_n)):
        options.append(str_n[:i] + str_d + fill*(L - i - 1))
    options.append(str_n)
    options = [int(x) for x in options]
    new_options = []
    for option in options:
        if int(math.log10(option)) == 9:
            for j in range(1,10):
                new_options.append(j*10**10 + option)
    # print(options)
    return options + new_options

def get_extremes(n_min, n_max, d):
    L = len(str(n_max))
    options_min = apply_sieve(n_min, L, d, "min") + apply_sieve(n_max, L, d, "min")
    options_max = apply_sieve(n_min, L, d, "max") + apply_sieve(n_max, L, d, "max")
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

def find_zero(a,b,d,level=-1*math.inf):
    # Find the nearest zero to a in the range of a to b, with digit d
    # Check if answer has been found
    h = fast_h(a, d)
    if h == 0:
        if level >=0: print("Found zero at n: {:,}".format(a))
        return a
    # 1) Test range
    extremes, _ = get_extremes_recurse(a,b,d)
    if level >=0: print("| "*level + "Range: [{:,}, {:,}], {}".format(a,b,extremes), end=", ")
    if (h > 0 and extremes.min_h > 0) or (h < 0 and extremes.max_h < 0):
        #Reject this partition, there is no zero crossing
        if level >=0: print("no zeros")
        return 0
    if level >=0: print("subdivide")
    # b_new is the new minimum or maximum
    if h > 0:
        b_new = extremes.min_n
    else:
        b_new = extremes.max_n
    # subdivide the range
    c = (a + b_new)//2
    # Test if first half contains the zero [a,c]
    zero_n = find_zero(a, c, d, level+1)
    if zero_n == 0:
        # Test the upper half of the range [c, b_new]
        zero_n = find_zero(c+1, b_new, d, level+1)
        if zero_n == 0:
            return -1*b_new # Full breaking code, skipped past a zero
    return zero_n

# LOOK HERE FOR THE ZERO FINDING CODE
# N = 10**13
# total = 0
# for d in range(1,10):
#     sum_d = 0
#     print("d: {}".format(d))
#     zero_n = 0
#     while True:
#         zero_n = find_zero(zero_n + 1, N, d)
#         if zero_n > 0:
#             print("    Zero found: {:,}".format(zero_n))
#             sum_d += zero_n
#         elif zero_n < 0:
#             zero_n *= -1 # Flip the sign where a skip was found
#             print("    Zero skip: {:,}.".format(zero_n))
#         else:
#             print("    No more zeros found.".format())
#             break
#     print("Sum for {}: {:,}".format(d, sum_d))
#     total += sum_d
# print("ans", total)


# d = 5
# print(n := find_zero(1, 10**13, d, level=0))
# print(fast_h(-1*n, d))
# print(get_extremes(-1*n+1, 16*10**10, d))

# n = 5_555_555_554
# print(fast_h(n, d))
# print(n - brute_recurse(n, d))

# n = 5_555_555_555
# print(fast_h(n, d))
# print(n - brute_recurse(n, d))


# test(, 1000000, d)

#WRONG
# 1783583701357
# 394371965312
# 1328912900887


class Digit_Iterator:

    def __init__(self, digit, previous_total, previous_weights, previous_n_min, previous_n_max, d, range_check_flag=True):
        # Holds a digit, future weights, current total, and mins/maxes for the h(n) equation solution on a particular range
        # Could probably be solved more quickly using direct reculrsion and a lookup table, but may be good enough
        self.digit = digit
        self.d = d
        self.total = previous_total + previous_weights[-1]*digit
        self.my_weight = previous_weights[-1]
        self.weights = previous_weights[:-1:]
        if digit < d:
            # Weights do not need to be changed; nor total
            pass
        elif digit == d:
            # Weights need to be changed
            self.total -= 1
            for e in range(0, len(self.weights)):
                self.weights[e] -= 10**e
        else: #digit > d:
            self.total -= 10**len(self.weights)
        #Update the minimum and maximum values for the next digit iteration
        # Assume that the digit fits within the previous n_min and previous n_max
        if digit > previous_n_min//10**len(self.weights):
            self.n_min = 0
        else:
            self.n_min = previous_n_min % 10**len(self.weights)
        if digit < previous_n_max//10**len(self.weights):
            self.n_max = 10**(len(self.weights)) - 1
        else:
            self.n_max = previous_n_max % 10**len(self.weights)
        if range_check_flag:
            # Raise an exception if attempting to use a digit outside of the previous allowable range
            if digit*10**len(self.weights) > previous_n_max:
                raise Exception("Attempted to use digit greter than n_max")
            if (digit+1)*10**len(self.weights) - 1 < previous_n_min:
                raise Exception("Attempred to use digit less than n_min")
            if self.n_max < self.n_min:
                raise Exception("maximum less than minimum.")
    
    def __repr__(self):
        return "<digit: {}, total: {:,}, range: [{:,}, {:,}], weights: {:,}~{}, extremes:[{:,}, {:,}]>".format(
            self.digit, self.total, self.n_min, self.n_max, self.my_weight, self.weights[::-1],
            self.min_possible_total(), self.max_possible_total())
    
    def compare(self, other:"Digit_Iterator"):
        # Compare self to another Digit Iterator
        # Return    -1 if SELF is always equal to or LESS than OTHER
        #           0 if cannot make a guarenteed statement about the relative sizes of self & other
        #           +1 if SELF is always equal to or GREATER than OTHER
        if self.total < other.min_possible_total():
            return -1
        if self.total > other.max_possible_total():
            return 1
        return 0

    def min_possible_total(self):
        # Return the minimum possible total for the DI
        # Assume that all of the g(n) components are as small as possible 10^e
        # Negative weights get a 9, positive weights get a zero
        # Ignore bounds; filter later
        min_total = self.total
        for w, e in zip(self.weights, range(0, len(self.weights))):
            if w*9 - 10**e < 0:
                #Beneficial to use a high digit for the min
                min_total += 9*w - 10**e
            # Else assume digit is zero
        return min_total

    def max_possible_total(self):
        # Return the maximum possible total for the DI
        # Assume that all of the g(n) components are as small as possible 10^e
        # Negative weights get a 9, positive weights get a zero
        # Ignore bounds; filter later
        max_total = self.total
        for w, e in zip(self.weights, range(0, len(self.weights))):
            if w > 0:
                # Make more positive; choose 9 for the digit
                max_total += 9*w #Ignore the negative component as maybe that won't exist for future digits based on n_min & n_max
            else:
                #choose 0 for the digit
                pass
        return max_total
    
    def generate_next_DI(self, digit):
        return Digit_Iterator(digit, self.total, self.weights, self.n_min, self.n_max, self.d)
    
    def sub_digit_range(self):
        E = len(self.weights) - 1
        for digit in range(self.n_min//10**E, self.n_max//10**E + 1):
            yield digit
    
def sub_digit_range(n_min, n_max):
    if n_max == 0:
        yield 0
        return
    E = int(math.log10(n_max))
    

class Digit_Iterator_Baseline(Digit_Iterator):

    def __init__(self, n_min, n_max, d):
        E = int(math.log10(n_max)) + 1
        weights = [int((10-e)*10**(e-1)) for e in range(E + 1)]
        super().__init__(0, 0, weights, n_min, n_max, d, False)




def expand_and_select_min(DI: Digit_Iterator, mode = "min", level = 0, print_flag = False):
    if print_flag: print(" |"*level, DI)
    if len(DI.weights) == 0:
        if print_flag: 
            extremes = Extremes()
            extremes.update(DI.digit, 0)
            print(" |"*level, "returning {}".format(extremes))
        return DI.total, 0
    outcomes: list[Digit_Iterator] = []
    for digit in DI.sub_digit_range():
        q = DI.generate_next_DI(digit)
        outcomes.append(q)
    extremes = Extremes()
    #Get the smallest of the DI
    while len(outcomes) > 0:
        best_in_list = outcomes[0]
        for a in outcomes:
            if (mode =="min" and a.total < best_in_list.total) or (mode=="max" and a.total > best_in_list.total):
                best_in_list = a
        #Remove the best from the outcomes
        outcomes.remove(best_in_list) 
        # See if better than previously found total
        if (mode=="min" and best_in_list.min_possible_total() < extremes.min_h) or (mode=="max" and best_in_list.max_possible_total() > extremes.max_h):
            sub_total, sub_digits = expand_and_select_min(best_in_list, mode, level+1, print_flag)
            sub_digits += best_in_list.digit*10**(len(best_in_list.weights))
            extremes.update(sub_digits, sub_total)
    if mode=="min":
        if print_flag: print(" |"*level, "returning {}".format(extremes.str_min()))
        return extremes.min_h, extremes.min_n
    else:
        if print_flag: print(" |"*level, "returning {}".format(extremes.str_max()))
        return extremes.max_h, extremes.max_n

def get_extremes_recurse(n_min, n_max, d, print_flag = False):
    extremes = Extremes()
    # print("MINIMUM:")
    h, n = expand_and_select_min(Digit_Iterator_Baseline(n_min, n_max, d), mode="min", print_flag=print_flag)
    extremes.update(n, h)
    # print("MAXIMUM")
    h, n = expand_and_select_min(Digit_Iterator_Baseline(n_min, n_max, d), mode="max", print_flag=print_flag)
    extremes.update(n, h)
    # print(extremes)
    return extremes, 0

# d = 3
# n_min, n_max = (1137, 6567)
# print([n_min, n_max])
# get_extremes_recurse(n_min, n_max, d)
# print(fast_h(6574, d))


# LOOK HERE FOR THE ZERO FINDING CODE
N = 10**11
total = 0
latest_zero_found = -1
for d in range(1,10):
    sum_d = 0
    print("d: {}".format(d))
    zero_n = 0
    while True:
        zero_n = find_zero(zero_n + 1, N, d)
        if zero_n > 0:
            if zero_n - latest_zero_found > 1:
                if latest_zero_found >= 0:
                    print()
                    latest_zero_found = -1
                print("    Zero found: {:,}".format(zero_n), end="   ")
            else:
                print("{:,}".format(zero_n), end="   ")
            latest_zero_found = zero_n
            sum_d += zero_n
        elif zero_n < 0:
            zero_n *= -1 # Flip the sign where a skip was found
            if latest_zero_found >= 0:
                print()
                latest_zero_found = -1
            print("    Zero skip: {:,}.".format(zero_n))
        else:
            if latest_zero_found >= 0:
                print()
                latest_zero_found = -1
            print("    No more zeros found.".format())
            break
    if latest_zero_found >= 0:
        print()
        latest_zero_found = -1
    print("Sum for {}: {:,}".format(d, sum_d))
    total += sum_d
print("ans", total)

exit()

if a.total > max_DI.total:
    max_DI = a
print("{}:".format(a.digit), end=" ")
for b in outcomes:
    r = a.compare(b)
    if r < 0:
        print("< {}".format(b.digit), end=", ")
    elif r == 0:
        print("? {}".format(b.digit), end=", ")
    else:
        print("> {}".format(b.digit), end=", ")