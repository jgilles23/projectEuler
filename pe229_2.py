import numpy as np
import sympy
import math
import itertools 

k_options = [1, 2, 3, 7]

def test_brute(n, k):
    if n < k:
        return False
    max_a = math.isqrt(n-k)
    for a in range(1, max_a + 1):
        max_b = math.isqrt((n - a**2) // k)
        for b in range(1, max_b + 1):
            if a**2 + k*b**2 == n:
                return True
    return False

def test_fast(n, k):
    if n < k:
        return False
    b_max = math.isqrt((n-1)//k)
    for b in range(1, b_max + 1):
        a = math.isqrt(n - k*b**2)
        if a**2 + k*b**2 == n:
            return True
    return False

def test_numpy(n, k):
    if n < k:
        return False
    b_max = math.isqrt((n-1)//k)
    b_values = np.arange(1, b_max + 1)
    a_values = np.sqrt(n - k*b_values**2).astype(int)
    return np.any(a_values**2 + k*b_values**2 == n)

def multi_test(n, test_function=test_numpy):
    for k in k_options:
        if test_function(n, k) == False:
            return False
    return True

def run_tests(test_function, N):
    count = 0
    for i in range(1, N + 1):
        result = multi_test(i, test_function=test_function)
        if result:
            count += 1
    print(f"Count of numbers that can be expressed as a^2 + k*b^2 for all k in {k_options} up to {N}: {count}")
    return count

class package:
    def __init__(self, prime_mode = False):
        self.prime_powers = {}
        self.prime_allowed_n = {}
        self.prime_mode = prime_mode
    
    def score(self):
        allowed_n_count = 1
        moduli = 1
        for p in self.prime_powers:
            i, allowed_n = self.prime_powers[p], self.prime_allowed_n[p]
            allowed_n_count *= len(allowed_n)
            moduli *= p**i
        score = allowed_n_count / moduli
        return score, allowed_n_count, moduli
    
    def copy(self):
        new_package = package()
        new_package.prime_powers = self.prime_powers.copy()
        new_package.prime_allowed_n = self.prime_allowed_n.copy()
        new_package.prime_mode = self.prime_mode
        return new_package
    
    def determine_allowed_n_moduli(self, m, remove_p=None):
        overall_allowed = np.full(m, True)
        for k in k_options:
            allowed = np.full(m, False)
            a = np.arange(m).reshape(-1, 1)
            b = np.arange(m)
            n = (a**2 + k*b**2) % m
            allowed[n] = True
            overall_allowed = np.logical_and(overall_allowed, allowed)
        if remove_p is not None:
            overall_allowed[0::remove_p] = False
        return np.where(overall_allowed == True)[0]
    
    def updated(self, p, delta_i):
        new_package = self.copy()
        if p in new_package.prime_powers:
            new_i = new_package.prime_powers[p] + delta_i
        else:
            new_i = delta_i
        #Cannot compute numbers that are too large
        if p**new_i > 5000:
            return None
        new_package.prime_powers[p] = new_i
        remove = p if self.prime_mode else None
        new_package.prime_allowed_n[p] = self.determine_allowed_n_moduli(p**new_i, remove_p=remove)
        return new_package
    
    def step_package(self, n_allowed_limit, p_limit):
        new_packages = []
        new_scores = []
        for p in sympy.primerange(2, p_limit + 1):
            for delta_i in [1, 2]:
                new_package = self.copy().updated(p, delta_i)
                if new_package is not None:
                    score, allowed_n_count, moduli = new_package.score()
                    if allowed_n_count <= n_allowed_limit:
                        new_scores.append(score)
                        new_packages.append(new_package)
                    else:
                        break
        #Select the best new package
        if len(new_scores) > 0:
            best_index = np.argmin(new_scores)
            return new_packages[best_index]
        else:
            return None
        
    def optimize_package(self, n_allowed_limit, p_limit = 20, print_steps=False):
        best_package = self
        while True:
            new_package = best_package.step_package(n_allowed_limit, p_limit=p_limit)
            if new_package is None:
                break
            if print_steps:
                print(new_package)
            best_package = new_package
        return best_package
    
    def modular_test(self, n):
        for p in self.prime_powers:
            if n % p**self.prime_powers[p] not in self.prime_allowed_n[p]:
                return False
        return True
    
    def moduli(self):
        score, allowed_n_count, moduli = self.score()
        return moduli
    
    def yield_combined_remainders(self):
        primes = sorted(self.prime_powers.keys())
        powers = [self.prime_powers[p] for p in primes]
        allowed_n = [self.prime_allowed_n[p] for p in primes]
        bases = [p**i for p, i in zip(primes, powers)]
        for combination in itertools.product(*allowed_n):
            n, moduli = sympy.ntheory.modular.crt(bases, combination)
            yield n

    def combined_remainders(self):
        return list(self.yield_combined_remainders())

    def __repr__(self):
        score, allowed_n_count, moduli = self.score()
        print_dict = [f"{p}^{self.prime_powers[p]}:{len(self.prime_allowed_n[p])}" for p in self.prime_powers]
        return f"<score: {allowed_n_count:,}/{moduli:,} = {score:.5f}, {str(print_dict)}>"

N = 2*10**9
n_allowed_limit = 10**5

# #First count up the squares
def get_square_count():
    print("Counting squares...")
    square_count = 0
    for c in range(1, math.isqrt(N) + 1):
        if multi_test(c**2):
            square_count += 1
            if square_count % 2000 == 0:
                print(f"  Partial square count: {square_count:,}, c: {c:,}, c**2: {c**2:,}")
    print(f"  Square count: {square_count:,}")
    return square_count

#Now cuntup primes and their square multiples
def get_allowed_primes():
    print("Getting primes...")
    prime_moduli_package = package(prime_mode=True).optimize_package(n_allowed_limit,print_steps=False)
    print("  Package:", prime_moduli_package)
    allowed_remainders = sorted(prime_moduli_package.combined_remainders())
    if len(allowed_remainders) <= 10:
        print("  Allowed remainders:", allowed_remainders)
    allowed_primes = []
    base, modulus = 0, prime_moduli_package.moduli()
    print_modulus = 10**8//modulus*modulus
    while True:
        for remainder in allowed_remainders:
            candidate = base + remainder
            if candidate > N:
                return allowed_primes
            if sympy.isprime(candidate):
                # if multi_test(candidate):
                allowed_primes.append(candidate)
        base += modulus
        if base % print_modulus == 0:
            print(f"  Checked up to {base:,}, found {len(allowed_primes):,} allowed_primes")

complex_step_count = 0

def print_complex_step(i, j, k, complex_count):
    global complex_step_count
    complex_step_count += 1
    if complex_step_count % 10**6 == 0:
        print(f"  Tested {complex_step_count:,}, at (i: {i:,}, j: {j:,}, k: {k:,}), current complex count: {complex_count:,}")

def get_complex_count():
    #Generate allowed values and their coefficients
    allowed_primes = get_allowed_primes()
    print("Gettting complex count...")
    print(f" Allowed primes: {len(allowed_primes):,}")
    print(f" Head allowed primes: {allowed_primes[:10]}")
    # print(len(simple_allowed_primes()))
    complex_count = 0
    for i, a in enumerate(allowed_primes):
        if a > N:
            break
        print_complex_step(i, 0, 0, complex_count)
        complex_count += math.isqrt(N//(a))
        if a**2 > N:
            continue
        for j, b in enumerate(allowed_primes[i+1:], start=i+1):
            if a*b > N:
                break
            print_complex_step(i, j, 0, complex_count)
            complex_count += math.isqrt(N//(a*b))
            if a*b*b > N:
                continue
            for k, c in enumerate(allowed_primes[j+1:], start=j+1):
                if a*b*c > N:
                    break
                print_complex_step(i, j, k, complex_count)
                complex_count += math.isqrt(N//(a*b*c))
    print("  Complex count:", complex_count)
    return complex_count

def get_simple_count():
    count = 0
    for n in range(1, N + 1):
        if multi_test(n):
            count += 1
    return count

square_count = get_square_count()
complex_count = get_complex_count()
total_count = square_count + complex_count
print(f"Total count: {total_count:,}")
print("ans:", total_count)
