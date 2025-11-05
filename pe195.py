import sympy
import math

# R = 100

# print("A METHOD")
# def generate_trinagle_from_a(a):
#     ij = -12*a**2
#     triangle_count = 0
#     for i_opposite in sympy.ntheory.factor_.divisors(-ij, generator = True):
#         i = -i_opposite
#         j = ij//i
#         x_numerator = i + j + 4*a
#         if x_numerator <= 0 or x_numerator//8*8 != x_numerator:
#             # print("fail x integer", (i, j), "%8", (i%8, j%8))
#             continue #Check for integer solutions
#         y_numerator = j - i
#         if y_numerator <= 0 or y_numerator//8*8 != y_numerator:
#             # print("fail y integer", (i, j), "%8", (i%8, j%8))
#             continue #Check for integer solutions
#         b, c = x_numerator//8, y_numerator//8
#         if a == b:
#             # print("fail equilateral", (i,j), (a,b,c))
#             continue #Equilateral triangle
#         if a > b:
#             # print("Non increasing", a, b)
#             continue #Non-increasing triange
#         s = (a + b + c)/2
#         r = math.sqrt((s - a)*(s - b)*(s - c)/s)
#         if r > R:
#             if r - R < 0.00001:
#                 print("POTENTIAL FLOATING POINT ERROR")
#             continue #Triangle too big                
#         m = [i/-2, i/-6]
#         n = [j/6, j/2]
#         # print(f"triangle (a,b,c): {(a,b,c)}, r: {r}, (i,j): {(i,j)}, (m,n): {(i/-2, j/6)}&{(i/-6,j/2)}")
#         triangle_count += 1
#     return triangle_count

# # generate_trinagle_from_a(29)

# count = 0
# for a in range(int(2*math.sqrt(3)*R) + 1):
#     count += generate_trinagle_from_a(a)
# print("ans", count)
#ans 1147 with R up to 2*sqrt(3)*R. R=100
#ans 784 with a up to 2R, R=100

# a, i = sympy.symbols("a i")
# j = -12*a**2/i
# b = (i + j + 4*a)/8
# c = (j - i)/8
# s = (a + b + c)/2
# r = sympy.sqrt((s - a)*(s-b)*(s-c)/s)
# print(r.simplify())

# print()
# print("Finding radius constraint")

# m, m_p, k, r = sympy.symbols("m m_p k r", real=True, positive=True)
# n = m_p*k**2
# i = -2*m #Case A
# j = 6*n
# a = sympy.sqrt(m*n)
# b = (i + j  + 4*a)/8
# c = (j - i)/8
# s = (a + b + c)/2
# r_exp = sympy.sqrt((s - a)*(s - b)*(s-c)/s)
# r_exp = r_exp.simplify()
# print(r_exp)
# solve_dict = sympy.solve(r_exp - r, k)
# for part in solve_dict:
#     numerical = part.subs([(m ,5), (m_p, 5), ])
#     print(part.simplify())

# print()
# print("K METHOD")

# R = 100

# def iterate_k(m, m_prime, i_prefix, j_prefix, equilateral_m_prefix, n_m_compare):
#     #Handle both of the scenarios in a single function
#     i = i_prefix*m
#     n_min = m/9 # n > m; for positive x, y
#     n_max = (4*math.sqrt(3)*R + m)**2 / (9*m)
#     # n = m_prime * k^2
#     k_min = math.sqrt(n_min/m_prime)
#     k_max = math.sqrt(n_max/m_prime)
#     k_start = 2 if m % 4 == 0 else 1 #k is either even or odd based on m
#     j_min = i/-3
#     k_min = int(math.sqrt(m/m_prime/n_m_compare)) + 1
#     if k_min % 2 != k_start % 2:
#         k_min += 1 #If wrong parity change to the other one
#     for k in range(k_min, 10*R, 2):
#         n = m_prime*k**2
#         if equilateral_m_prefix*m == n:
#             continue #Equilateral
#         j = j_prefix*n
#         #print(f"k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}")
#         #Go through the same checks as before
#         a = math.isqrt(i*j//-12)
#         x_numerator = i + j + 4*a #b
#         y_numerator = j - i #c
#         if n_m_compare*n <= m:
#             raise Exception("did not expect n too small")
#         if x_numerator <= 0:
#             print(k, "fail x too small", (i, j), "%8", (i%8, j%8))
#             raise Exception("did not expect x too small")
#         if y_numerator <= 0 or y_numerator//8*8 != y_numerator:
#             print(f"k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}")
#             print(k, "fail y integer", (i, j), "%8", (i%8, j%8))
#             raise Exception("did not expect to fail on y_numerator")
#         if x_numerator//8*8 != x_numerator:
#             raise Exception("Did not expect modulus fail on x")
#         if y_numerator//8*8 != y_numerator:
#             raise Exception("Did not expect to fail on y integer")
#         b, c = x_numerator//8, y_numerator//8
#         if a == b:
#             print(f"k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}")
#             print(k, "fail equilateral", (i,j), (a,b,c))
#             raise Exception("did not expect equilateral triangle")
#         #Insert something to avoid non-increasing issue
#         if i_prefix == -2:
#             if n <= m and n >= m/9: #ensures a > c
#                 continue
#         elif i_prefix == -6:
#             if n <= 9*m and n >= m: #ensures a > c
#                 continue
#         else:
#             raise Exception("Unexpected i_prefix")
#         if a > b:
#             print(f"k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}")
#             print(k, "Non increasing")
#             continue #Non-increasing triange
#         s = (a + b + c)/2
#         r = math.sqrt((s - a)*(s - b)*(s - c)/s)
#         if r > R:
#             if r - R < 0.00001:
#                 print("POTENTIAL FLOATING POINT ERROR")
#             print(m, k - k_min)
#             return #Triangle too big, once a single too big triangle is found we are done
#         s = f"m: {m}, triangle (a,b,c): {(a,b,c)}, r: {r}, k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}"
#         # print(s)
#         if (i,j) in triangles:
#             print("Found Bonus Triangle")
#             print(s)
#             bonus_count[0] += 1
#         else:
#             triangles.add((i,j))
#         count[0] += 1
#     return

# count = [0]
# bonus_count = [0]
# triangles = set()
# m_max = 10*R
# for m in range(1, m_max):
#     m_factor_dict = sympy.ntheory.factor_.factorint(m)
#     m_prime_factor_dict = {a: 1 for a in m_factor_dict if m_factor_dict[a]%2==1}
#     m_prime = 1 #The sqare compliment to n
#     for a in m_prime_factor_dict:
#         m_prime = m_prime* a**m_prime_factor_dict[a]
#     # print(f"m: {m}, factors: {m_factor_dict}, m_prime: {m_prime}, factors: {m_prime_factor_dict}")
#     # i = -6m, j = 2n
#     if m % 3 != 0:
#         iterate_k(m, m_prime, -2, 6, 1, 9)
#     iterate_k(m, m_prime, -6, 2, 9, 1)
        
# print("ans", count[0], "bonus_count", bonus_count[0])

    # i = -2m, j = 6n


print()
print("K METHOD")

R = 1053779

def iterate_k(m, m_prime, i_prefix, j_prefix, equilateral_m_prefix, n_m_compare):
    #Handle both of the scenarios in a single function
    i = i_prefix*m
    k_start = 2 if m % 4 == 0 else 1 #k is either even or odd based on m
    k_min = int(math.sqrt(m/m_prime/n_m_compare)) + 1
    if k_min % 2 != k_start % 2:
        k_min += 1 #If wrong parity change to the other one
    for k in range(k_min, 10*R, 2):
        n = m_prime*k**2
        if equilateral_m_prefix*m == n:
            continue #Equilateral
        j = j_prefix*n
        #print(f"k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}")
        #Go through the same checks as before
        a = math.isqrt(i*j//-12)
        x_numerator = i + j + 4*a #b
        y_numerator = j - i #c
        b, c = x_numerator//8, y_numerator//8
        #Insert something to avoid non-increasing issue
        if i_prefix == -2:
            if n <= m and n >= m/9: #ensures a > c
                continue
        elif i_prefix == -6:
            if n <= 9*m and n >= m: #ensures a > c
                continue
        s = (a + b + c)/2
        r = math.sqrt((s - a)*(s - b)*(s - c)/s)
        if r > R:
            if r - R < 0.00001:
                print("POTENTIAL FLOATING POINT ERROR")
            return #Triangle too big, once a single too big triangle is found we are done
        s = f"m: {m}, triangle (a,b,c): {(a,b,c)}, r: {r}, k: {k}, (m,n): {(m,n)}, (i,j): {(i,j)}"
        # print(s)
        count[0] += 1
    return

count = [0]
m_max = 10*R
for m in range(1, m_max):
    if m%10000 == 0:
        print(m, count[0])
    m_factor_dict = sympy.ntheory.factor_.factorint(m)
    m_prime_factor_dict = {a: 1 for a in m_factor_dict if m_factor_dict[a]%2==1}
    m_prime = 1 #The sqare compliment to n
    for a in m_prime_factor_dict:
        m_prime = m_prime* a**m_prime_factor_dict[a]
    # print(f"m: {m}, factors: {m_factor_dict}, m_prime: {m_prime}, factors: {m_prime_factor_dict}")
    # i = -6m, j = 2n
    if m % 3 != 0:
        iterate_k(m, m_prime, -2, 6, 1, 9)
    iterate_k(m, m_prime, -6, 2, 9, 1)
        
print("ans", count[0])
#75085391 is CORRECT!