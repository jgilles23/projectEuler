# Method source: https://www.alpertron.com.ar/METHODS.HTM#Ellipse

import math

# Methods to solve quadratic Diophantine equations
# Alpertron  Number Theory  Methods to solve quadratic Diophantine equations
# by Dario Alejandro Alpern

# The purpose of this article is to show how to solve the Diophantine Equation Ax2 + Bxy + Cy2 + Dx + Ey + F = 0. The term Diophantine Equation means that the solutions (x, y) should be integer numbers. For example, the equation 4y2 - 20y + 25 = 0 has solutions given by the horizontal line y = 2.5, but since 2.5 is not an integer number, we will say that the equation has no solutions.

# There are several cases that depend on the values of A, B and C. The names are taken from the figures represented by the equation in the plane xy: a line, an ellipse, a parabola or a hyperbola (or two lines). These figures are the set of real solutions. In our situation, the set of solutions are represented by isolated point/s in the plane xy.

'''Helper functions'''
def bezout_coefficients(a,b):
    # Input a,b the integers for which to solve the equation for x & y
    # ax+by=+/-1
    #Return:
    # (x,y) the bezout coefficients
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    # function extended_gcd(a, b)
    # (old_r, r) := (a, b)
    # (old_s, s) := (1, 0)
    # (old_t, t) := (0, 1)
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)
    # while r ≠ 0 do
    while r != 0:
        #     quotient := old_r div r
        quotient = old_r // r
        #     (old_r, r) := (r, old_r − quotient × r)
        #     (old_s, s) := (s, old_s − quotient × s)
        #     (old_t, t) := (t, old_t − quotient × t)
        (old_r, r) = (r, old_r - quotient*r)
        (old_s, s) = (s, old_s - quotient*s)
        (old_t, t) = (t, old_t - quotient*t)
    # output "Bézout coefficients:", (old_s, old_t)
    # output "greatest common divisor:", old_r
    # output "quotients by the gcd:", (t, s)
    return (old_s, old_t)

class Generator:
    def __init__(self):
        pass   
    def __next__(self):
        return_value = self.a
        self.a, self.b = self.b, self.a+self.b
        return return_value
    def __iter__(self):
        return self

def print_count_cutoff(generator, cutoff):
    # Print a set number of yields of the generator function set by count_cutoff
    i = 0
    for output in generator:
        if i >= cutoff:
            break
        i += 1
        print(output)

def print_magnitude_cutoff(generator, cutoff_x = math.inf, cutoff_y = math.inf):
    # Print until magnitude of either x or y exceeds the magnitude cutoff specificed
    for output in generator:
        if abs(output[0]) > cutoff_x:
            break
        if abs(output[1]) > cutoff_y:
            break
        print(output)


def generator_square(x_value = "all", y_value = "all"):
    # All points either x, y or both are valid, generate starting with magnitude 0 and expand from there, if value not set to "all", must be set to a specific integer
    if x_value == "all": x_min, x_max = (0,0)
    else: x_min, x_max = (x_value, x_value)
    if y_value == "all": y_min, y_max = (0,0)
    else: y_min, y_max = (y_value, y_value)
    while True:
        #Corners
        for x in set([x_min, x_max]):
            for y in set([y_min, y_max]):
                yield(x,y)
        if x_value == "all" and y_value == "all":
            #Left / Right
            for x in [x_min, x_max]:
                for y in range(y_min + 1, y_max):
                    yield (x,y)
            #Top / Bottom
            for y in [y_min, y_max]:
                for x in range(x_min + 1, x_max):
                    yield (x,y)
        if x_value == "all":
            x_min -= 1
            x_max += 1
        if y_value == "all":
            y_min -= 1
            y_max += 1
        if x_value != "all" and y_value != "all":
            return

        




class Diophantine:
    # Class for holding the diophantine equation
    def __init__(self, Q):
        # Q: coefficients of the diaophantine equations of the form
        #   (a, b, c, d, e, f) where
        #   ax**2 + bxy + cy**2 + dx + ey + f = 0
        #Set properties:
        # base_points: base solutions to the equation of the form set((x,y), (x,y), (x,y), ...)
        # recursive_coefficients: reccurance relationships for the base solutions of the form: set((Rx, Ry), ...)
        #   where Rx/y specifies the next entry in relationship e.g.
        #   Rx = (a,b,c)
        #   x_n+1 = ax + by + c 
        # linear_coefficients: solutions of the form 
        # generators: list of generators used to output points in (x,y) that satisft the equation
        self.Q = Q
        (a, b, c, d, e, f) = self.Q
        # Setup the other variables
        self.base_points = set()
        self.recursive_coefficients = set()
        self.generator = []
        #Print equation
        print("Equation: ({})x**2 + ({})xy + ({})y**2 + ({})x + ({})y + ({}) = 0".format(*self.Q))
        #Determine the "case" that the solution will take the form of
        self.discriminant = b**2 - 4*a*c
        # Linear case: A = B = C = 0.
        if a==0 and b==0 and c==0:
            self.case = self.linear
        # Simple hyperbolic case: A = C = 0; B ≠ 0.
        elif a == 0 and c == 0 and b != 0:
            self.case = self.simple_hyperbolic
        # Elliptical case: B2 - 4AC < 0.
        elif self.discriminant < 0:
            self.case = self.elliptical
        # Parabolic case: B2 - 4AC = 0.
        elif self.discriminant == 0:
            self.case = self.parabolic
        # Hyperbolic case: B2 - 4AC > 0.
        elif self.discriminant > 0:
            self.case = self.hyperbolic
        # No case found, error
        else:
            raise Exception("Case not recognized.")
        #Print the found case
        print("Case:", self.case.__name__)
        #Call the solver for the case in question
        self.case()
    
    def test_point(self, P):
        #Return: true if the point fits the equation, and false otherwise
        (x,y) = P
        (a, b, c, d, e, f) = self.Q
        zero_test = a*x**2 + b*x*y + c*y**2 + d*x + e*y + f
        return zero_test == s0
    
    def print_count_cutoff(self, cutoff):
        # For each generator in the generator list, print the results up to the count cutoff
        # Test for true results
        i = 0
        for output in self.generator[0]():
            if i >= cutoff:
                break
            i += 1
            print(output, self.test_point(output))


    """ LINEAR """ 
    def linear(self):
        # Linear case: A = B = C = 0
        (a, b, c, d, e, f) = self.Q
        # The equation is now: Dx + Ey + F = 0. There are several cases:
        # If D = 0 and E = 0 there will be solutions only if F = 0. In this case all values of x and y are solutions.
        if d==0 and e==0 and f==0:
            print("Solution : all x & all y")
            self.generator += [generator_square(x_value="all", y_value="all")]
            return
        # If D = 0 and E ≠ 0 we have:
        elif d==0 and e!=0:
            # Ey + F = 0 => y = -F/E, x = any integer.
            # This means that there will be solutions if and only if F is a multiple of E.
            if f % e == 0:
                y = -f//e
                print("Solution: all x & y = {}".format(y))
                self.generator += [generator_square("all", y)]
                return
            else:
                print("Solution: none")
                return
        # If D ≠ 0 and E = 0 we have:
        elif d!=0 and e==0:
            # Dx + F = 0 => x = -F/D, y = any integer.
            # This means that there will be solutions if and only if F is a multiple of D.
            if f % d == 0:
                x = -f//d
                print("Solution: x = {} & all y".format(x))
                self.generator += [generator_square(x, "all")]
                return
            else:
                print ("Soltion: none")
                return
        # If D ≠ 0 and E ≠ 0 the situation is slighty more complicated:
        elif d!=0 and e!=0:
            # Let g = gcd(D, E). Since both D and E are multiple of g, the expression Dx + Ey will be also a multiple of g for any integer value of x and y, so if F is not a multiple of g the equation has no solutions.
            g = math.gcd(d,e)
            if f % g != 0:
                print("Solutions: none")
                return
            # If F is multiple of g we can divide all three coefficients by g thus obtaining:
            # dx + ey = -f (where d=D/g, e=E/g and f=F/g). We will use now the Extended Euclid's Algorithm that can be used to find integers u' and v' such that uu'+vv' = ±gcd(u, v) (where the sign depends on the sign of d and e and the exact implementation of the algorithm).
            D = d//g
            E = e//g
            F = f//g
            # We can let u = d, v = e. Once the values of u' and v' are found so that du'+ev' = ±1 (since gcd(d, e)=1) we can multiply the equation by -f to obtain:
            (up, vp) = bezout_coefficients(D, E)
            # du'+ev' = ±1 => d(±fu')+e(±fv') = -f => d(±fu')+det+e(±fv')-det = -f => d(et±fu')+e(-dt±fv') = f
            # So the general solution set is:
            # x = et ± fu'
            # y = -dt ± fv'
            # t = any integer
            #Determine the sign
            sign = 1 if self.test_point((F*up, F*vp)) else -1
            def generator_parametric():
                t = 0
                while True:
                    #Use a set to eliminate duplicate answers
                    results = []
                    results.append((E*t + sign*F*up, -D*t + sign*F*vp)) #+t, +sign
                    if t != 0:
                        results.append((E*-1*t + sign*F*up, -D*-1*t + sign*F*vp)) #-t, +sign
                    for r in results:
                        yield r
                    t += 1
            print("Solutions: x = ({})*t + ({}) & y = -({})*t + ({}) for t = integer".format(E, sign*F*up, D, sign*F*vp))
            self.generator += [generator_parametric]

        # Example 1: Solve 10x + 84y + 16 = 0.
        # gcd(D, E) = gcd(10, 84) = 2. Since the constant term is also multiple of 2, we will divide the equation by this gcd.

        # The equation is now: 5x + 42y + 8 = 0.

        # Now we must apply the Generalized Euclidean algorithm:

        # Step 1: 1 * 5 + 0 * 42 = 5
        # Step 2: 0 * 5 + 1 * 42 = 42
        # Step 3: 1 * 5 + 0 * 42 = 5
        # Step 4: (-8) * 5 + 1 * 42 = 2
        # Step 5: 17 * 5 + (-2) * 42 = 1
        # Multiplying the last equation by -F = -8 we obtain:
        # (-136) * 5 + 16 * 42 = -8

        # Adding and subtracting de t = 5 * 42 t we obtain:
        # (-136 + 42 t) * 5 + (16 - 5 t) * 42 = -8

        # So, the solution is given by the set:

        # x = -136 + 42 t
        # y = 16 - 5 t
        # where t is any integer number.

    """Hyperbolic"""
    def simple_hyperbolic(self):
        pass

    # Simple Hyperbolic case A = C = 0; B ≠ 0
    # Since A = C = 0 the original equation is reduced to Bxy + Dx + Ey + F = 0, so:
    # Bxy + Dx + Ey + F	0
    # Bxy + Dx + Ey	-F
    # B2xy + BDx + BEy	-BF
    # B2xy + BDx + BEy + DE	DE - BF
    # (Bx + E) (By + D)	DE - BF
    # There are two cases: DE - BF = 0 (two lines parallel to x and y axes respectively) and DE - BF ≠ 0 (a hyperbola whose asymptotes are parallel to x and y axes).

    # In the first case a necessary condition to have solutions occurs when one of the parentheses equal zero, i.e., Bx + E = 0 or By + D = 0. Since B ≠ 0, we have solutions for:

    # x = - 
    # E
    # B
    # , y = any integer (if E is multiple of B)
    # x = any integer, y = - 
    # D
    # B
    # (if D is multiple of B)
    # In the second case the values of x and y are found by finding all divisors of DE - BF. Let d1, d2, ..., dn be the set of divisors of DE - BF. Then,

    # Bx + E	0
    # Bx	di - E
    # By + D	(DE - BF) / di
    # By	(DE - BF) / di - D
    # x = 
    # di - E
    # B
    # , y = 
    # (DE - BF) / di - D
    # B
    # Example 2: Solve 2xy + 5x + 56y + 7 = 0.

    # In this case the divisors of DE - BF = 5*56 - 2*7 = 266 are: ±1, ±2, ±7, ±14, ±19, ±38, ±133, ±266.

    # Since (2x + 56) (2y + 5) = 266 we obtain:

    # d1 = 1: x = (1-56)/2 = -55/2, y = (266/1-5)/2 = 261/2
    # d2 = -1: x = (-1-56)/2 = -57/2, y=[266/(-1)-5]/2 = 271/2
    # d3 = 2: x = (2-56)/2 = -27, y = (266/2-5)/2 = 64
    # d4 = -2: x = (-2-56)/2 = -29, y = [266/(-2)-5]/2 = -69
    # d5 = 7: x = (7-56)/2 = -49/2, y = (266/7-5)/2 = 33/2
    # d6 = -7: x = (-7-56)/2 = -63/2, y = [266/(-7)-5]/2 = -43/2
    # d7 = 14: x = (14-56)/2 = -21, y = (266/14-5)/2 = 7
    # d8 = -14: x = (-14-56)/2 = -35, y = [266/(-14)-5]/2 = -12
    # d9 = 19: x = (19-56)/2 = -37/2, y = (266/19-5)/2 = 9/2
    # d10 = -19: x = (-19-56)/2 = -75/2, y = [266/(-19)-5]/2 = -19/2
    # d11 = 38: x = (38-56)/2 = -9, y = (266/38-5)/2 = 1
    # d12 = -38: x = (-38-56)/2 = -47, y = [266/(-38)-5]/2 = -6
    # d13 = 133: x = (133-56)/2 = 77/2, y = (266/133-5)/2 = -3/2
    # d14 = -133: x = (-133-56)/2 = -189/2, y = [266/(-133)-5]/2 = -7/2
    # d15 = 266: x = (266-56)/2 = 105, y = (266/266-5)/2 = -2
    # d16 = -266: x = (-266-56)/2 = -161, y = [266/(-266)-5]/2 = -3
    # The only 8 solutions to the requested equations are marked above in red.

    """Elliptical"""
    def elliptical(self):
        pass

    # Elliptical case B2 - 4AC < 0
    # Since the ellipse is a closed figure, the number of solutions will be finite.

    # Operating with the original quadratic equation:

    # Ax2 + Bxy + Cy2 + Dx + Ey + F = 0

    # Cy2 + (Bx + E)y + (Ax2 + Dx + F) = 0

    # y = 
    # -(Bx + E) ± (Bx + E)2 - 4C(Ax2 + Dx + F)
    # 2C
    #     (*)

    # For any value of x there will be two values of y except at the left and right extremes of the ellipse. In this case there will be only one value of y. To determine the location of the left and right extremes we should equal the square root to zero, so the previous expression returns only one value of y.

    # (Bx + E)2 - 4C(Ax2 + Dx + F) = 0

    # (B2 - 4AC)x2 + 2(BE - 2CD)x + (E2 - 4CF) = 0

    # So the values of x should be between the roots of this equation. If the roots are not real, there will be no solutions to the original equation, else, all integer values of x should be replaced in equation (*) in order to find an integer value of y.

    # Example 3: Solve 42x2 + 8xy + 15y2 + 23x + 17y - 4915 = 0.

    # Since B2 - 4AC = 82 - 4*42*15 = -2456 < 0 the equation is elliptical.

    # The values of x should be between the roots of (B2 - 4AC)x2 + 2(BE - 2CD)x + (E2 - 4CF) = -2456x2 - 1108x + 295189 = 0. The roots equal -11.19... and 10.74..., so we have to check the values of x from -11 to 10.

    # The only value of x that replaced in (*) makes y integer occurs for x = -11, where y = -1, therefore this is the only solution to this problem.

    """Parabolic"""
    def parabolic(self):
        pass

    # Parabolic case B2 - 4AC = 0
    # Let g = gcd(A,C), a = A/g ≥ 0, b = B/g, c = C/g ≥ 0.
    # Since b2 = 4ac is positive, we can choose g with the same sign of A. In this way a and c will be positive (or one of them zero).

    # The expression b2 - 4ac = 0 implies that b2/4 = ac. Since gcd(a,c) = 1, both a and c are perfect squares.

    # Multiplying the original equation by :

    # g(ax2 + bxy + cy2) + Dx + Ey + F = 0

    # g(x + y)2 + Dx + Ey + F = 0

    # where for the sign of B/A is taken.

    # Adding and subtracting Dy:

    # g(x + y)2 + D(x + y) - Dy + Ey + F = 0

    # Let u = x + y:    (i)

    # gu2 + Du + (E - D)y + F = 0

    # (D - E)y = gu2 + Du + F (ii)

    # There are two cases: D - E = 0 (two parallel lines) or D - E ≠ 0 (a parabola).

    # In the first case, D - E = 0.

    # From (ii): gu2 + Du + F = 0

    # Since x and y should be integer numbers, the equation (i) implies that the number u (the root of the above equation) should be also integer. Let u1 and u2 be the roots of the above equation.

    # From (i) we have: x + y - u1 = 0 and x + y - u2 = 0 which can be solved with the methods for the linear equation.

    # In the second case, gu2 + Du + F should be multiple of D - E.

    # Let u0, u1,... the values of u in the range 0 ≤ u < |D - E| for which the above condition holds.

    # So u = ui + (D - E)t, where t is any integer number.   (iii)

    # Replacing (iii) in (ii):

    # (D - E)y = g[ui + (D - E)t]2 + D[ui + (D - E)t] + F

    # y = g(D - E)t2 + (D + 2gui)t + 
    # gui2 + Dui + F
    # D - E

    # From (i) and (iii):

    # u = x + y = ui + (D - E)t

    # x = g(E - D)t2 + (D - E - 2gui - D)t + ui -  
    # gui2 + Dui + F
    # D - E

    # x = g(E - D)t2 + (- E - 2gui)t + 
    # ui(D - E) - gui2 - Dui - F
    # D - E

    # x = g(E - D)t2 + (- E - 2gui)t - 
    # gui2 + Eui + F
    # D - E

    # x = g(E - D)t2 - (E + 2gui)t - 
    # gui2 + Eui + F
    # D - E

    # y = g(D - E)t2 + (D + 2gui)t + 
    # gui2 + Dui + F
    # D - E

    # Example 4: Find the solutions for 8 x2 - 24 xy + 18 y2 + 5x + 7y + 16 = 0

    # We have to calculate the values g, a, c, , , D - E and gu2 + Du + F.

    # g = gcd(8, 18) = 2
    # a = 8/2 = 4
    # c = 18/2 = 9
    # = 2
    # = -3 (since B/A = -24/8 < 0)
    # D - E = -3 * 5 - 2 * 7 = -29 (second case)
    # gu2 + Du + F = 4u2 + 5u + 32

    # We have to determine the values of u in the range 0 ≤ u < 29 for which 4u2 + 5u + 32 is multiple of 29.

    # The values of u are: u0 = 2 and u1 = 4.

    # For u0 = 2:

    # x = -174 t2 - 17 t - 2
    # y = -116 t2 - 21 t - 2
    # For u0 = 4:

    # x = -174 t2 - 41 t - 4
    # y = -116 t2 - 37 t - 4


    """Hyperbolic"""
    def hyperbolic(self):
        # Hyperbolic case B2 - 4AC > 0
        # Contents:
        # Find solutions of the homogeneous equation Ax2 + Bxy + Cy2 + F = 0
        self.hyperbolic_homogeneous_solutions()
        # Find recurrences among the solutions of the homogeneous equation
        # Find solutions of the general quadratic equation
        # Find recurrences among the solutions of the general quadratic equation

    def hyperbolic_homogeneous_solutions(self):
        # Find solutions of the homogeneous equation Ax2 + Bxy + Cy2 + F = 0
        (a, b, c, d, e, f) = self.Q
        # If F = 0 we have the trivial solution x = 0 and y = 0. Now we will investigate if there are more solutions.
        if f == 0:
            self.base_points.add((0,0))
            # Ax2 + Bxy + Cy2 = -F
            # Multiplying by 4A:
            # 4A2x2 + 4ABxy + 4ACy2 = -4AF
            # 4A2x2 + 4ABxy + B2y2 - B2y2 + 4ACy2 = -4AF
            # (2Ax + By)2 - (B2 - 4AC)y2 = -4AF
            # This can be interpreted as a difference of squares:
            # (2Ax + By +  B2 - 4AC y) (2Ax + By -  B2 - 4AC y) = -4AF
            # (2Ax + (B +  B2 - 4AC )y) (2Ax + (B -  B2 - 4AC )y) = -4AF
            # Since -4AF = 0, the condition to have more solutions is that B2 - 4AC should be a perfect square.
            if not math.sqrt(self.discriminant).is_integer():
                print("Solutions: none")
                return
            # Now the same method used for the linear equation (since the equation are represented by two lines in the plane xy intersecting at the point (0, 0)) can be used in order to find the solutions.
            diophantine_1 = Diophantine((0,0,0,2*a,int(math.sqrt(self.discriminant)),b))

        # If F ≠ 0 and B2 - 4AC = k2 for some integer k, the parentheses in the equation above should be factors of -4AF.

        # Let u1, u2,... be the positive and negative divisors of -4AF.

        # Then we have the following set of two linear equations in two unknowns:

        # 2Ax + (B+k)y = ui
        # 2Ax + (B-k)y = -4AF/ui

        # So we have:

        # y = 
        # ui + 4AF/ui
        # 2k

        # x = 
        # ui - (B+k)y
        # 2A

        # We should discard the values of ui that makes x or y non-integer.

        # Let's consider now the case F ≠ 0 and B2 - 4AC not a perfect square.

        # If F is not a multiple of gcd(A, B, C), the equation has no solutions, otherwise we can divide all coefficients of the equation by this gcd.

        # If 4 F2 < B2 - 4AC, the solutions of the equation will be amongst the convergents of the continued fraction of the roots of the equation At2 + Bt + C = 0.

        # The continued fraction expansion of a quadratic irrationality is periodic. Since B2 - 4AC is not a perfect square the number of solutions will be infinite or none.

        # In the other hand, if 4 F2 ≥ B2 - 4AC solutions can be obtained as follows:

        # Let G = gcd(x,y), x = Gu and y = Gv.

        # The original equation is then: AG2u2 + BG2uv + CG2v2 + F = 0, so F will be multiple of G2.

        # Dividing the equation by G2:

        # Au2 + Buv + Cv2 + F/G2 = 0    (1).

        # Once the values of u and v are found, we can easily determine x = Gu and y = Gv.

        # So we can assume that gcd(x,y) = 1.

        # Let x = sy - Fz    (2).

        # Replacing in the original equation:

        # A(sy - Fz)2 + B(sy - Fz)y + Cy2 + F = 0

        # As2y2 - 2AFsyz + AF2z2 + Bsy2 - BFyz + Cy2 = -F

        # (As2 + Bs + C) y2 + (-2As - B)Fyz + AF2z2 = - F

        # Dividing by -F:

        # -(As2 + Bs + C) y2 / F + (2As + B)yz - AFz2 = 1    (3)

        # Now we must determine the values of s between 0 and F - 1 such that As2 + Bs + C ≡ 0 (mod F). Once the values of y and z are found using continued fraction expansions of the roots of -(As2 + Bs + C) t2 / F + (2As + B)t - AF = 0, the value of x is found by (2). If no solutions are found amongst the convergents, there will be no solutions to (1).

        # If the original equation has solutions, there should be a solution to the previous congruence, except when gcd(A,B,F) > 1. In this case, if gcd(B,C,F) = 1 we should make the substitution y = sx - Fz    (4), so replacing in the original equation:

        # Ax2 + Bx(sx - Fz) + C(sx - Fz)2 + F = 0

        # Ax2 + Bsx2 - BFxz + Cs2x2 - 2CFsxz + CF2z2 = -F

        # (Cs2 + Bs + A) x2 + (-2Cs - B)Fxz + CF2z2 = - F

        # Dividing by -F:

        # -(Cs2 + Bs + A) x2 / F + (2Cs + B)xz - CFz2 = 1    (5).

        # Now we must determine the values of s between 0 and F - 1 such that Cs2 + Bs + A ≡ 0 (mod F). Once the values of x and z are found using continued fraction expansions of the roots of -(Cs2 + Bs + A) t2 / F + (2Cs + B)t - CF = 0, the value of y is found by (4). If no solutions are found amongst the convergents, there will be no solutions to (1).

        # The equations (4) and (5) have no solutions when both gcd(A,B,F) and gcd(B,C,F) are greater than 1. In this case we will use the following approach:

        # Let i, j, m and n be four integers such that in - jm = 1    (6).

        # If x = iX + jY and y = mX + nY    (7) we obtain X = nx - jy and Y = -mx + iy    (8).

        # Since the transformation is reversible, we can convert any (x,y) to (X,Y) and vice versa. So we will work with (X,Y) and with these solutions will can compute the values of (x,y) that satisfies the original equation.

        # Ax2 + Bxy + Cy2 =
        # = A(iX+jY)2 + B(iX+jY)(mX+nY) + C(mX+nY)2 =
        # = aX2 + bXY + cY2
        # where:

        # a = Ai2 + Bim + Cm2    (9)
        # b = 2Aij + Bin + Bjm + 2Cmn    (10)
        # c = Aj2 + Bjn + Cn2    (11)
        # So we have to find the values of i and m such that a = Ai2 + Bim + Cm2 is relatively prime to F.

        # Since gcd(C, F) > 1 we have gcd(Ai2 + Bim + Cm2, C) = 1, so gcd(i, C) = 1 and gcd(Ai+Bm, C) = 1.

        # Since gcd(A, F) > 1 we have gcd(Ai2 + Bim + Cm2, A) = 1, so gcd(m, A) = 1 and gcd(Bi+Cm, A) = 1.

        # From (6), gcd(i, m) = 1.

        # If F ≡ 0 (mod p) (p prime):

        # i and m from a, b and c
        # A	B	C	i, m	Examples
        # A ≡ 0	B ≡ 0	C ≡ 0	Not applicable (gcd(A, B, C) = 1)
        # A ≡ 0	B ≡ 0	C not congruent to 0	m not congruent to 0	i ≡ 0, m ≡ 1
        # A ≡ 0	B not congruent to 0	C ≡ 0	i not congruent to 0, m not congruent to 0	i ≡ 1, m ≡ 1
        # A ≡ 0	B not congruent to 0	C not congruent to 0	m not congruent to 0, i not congruent to -Cm/B	i ≡ 1-C, m ≡ B
        # A not congruent to 0	B ≡ 0	C ≡ 0	i not congruent to 0	i ≡ 1, m ≡ 0
        # A not congruent to 0	B ≡ 0	C not congruent to 0	i not congruent to 0 or m not congruent to 0	i ≡ 1, m ≡ 1
        # A not congruent to 0	B not congruent to 0	C ≡ 0	i not congruent to 0, m not congruent to -Ai/B	i ≡ B, m ≡ 1-A
        # A not congruent to 0	B not congruent to 0	C not congruent to 0	i not congruent to 0 or m not congruent to 0	i ≡ 1, m ≡ 1
        # While it is possible to generate the values of i and m from their values modulo different primes, it is very tedious and it is not necessary, because from the table above, almost all values of i and m can be used. So it is better to use the following pseudocode in order to find both values:

        #   for i=0 to |F|-1
        #     for m=0 to i+1
        #       if gcd(i, m) = 1
        #         k = Ai2 + Bim + Cm2
        #         if gcd(k, F) = 1, end.
        #       end if
        #     next m
        #   next i

        # With the values of i and m just found, we can compute the values of j and n from (6) using the methods for the linear equation. Then we have to compute a, b and c using (9), (10) and (11), from which the set of solutions (X,Y) can be found. With the formula (7) we can find the set of solutions (x,y).

        # Credits:
        # This method was e-mailed to me by Iain Davidson.

        # Example 5: Find some solutions for 18 x2 + 41 xy + 19 y2 - 24 = 0

        # First of all we must determine the gcd of all coefficients but the constant term, that is: gcd(18, 41, 19) = 1.

        # Dividing the equation by the greatest common divisor we obtain:
        # 18 x2 + 41 xy + 19 y2 - 24 = 0

        # Let x = sy - fz, so [-(as2 + bs + c)/f]y2 + (2sa + b)yz - afz2 = 1.

        # So 18 s2 + 41 s + 19 should be multiple of 24.

        # This holds for s = 19.

        # Let s = 19. Replacing in the above equation:
        # 304 y2 + 725 yz + 432 z2 = 1
        # We have to find the continued fraction expansion of the roots of 304 t2 + 725 t + 432 = 0, that is, t = 
        # √313 - 725
        # 608

        # The continued fraction expansion is:
        # -2 + //1, 5, 8, 5, 1, 3, 1, 1, 2, 2, 1, 1, 3, 1, 5, 8, 1, 2, 17, 2, 1//

        # where the periodic part is marked in bold (the period has 19 coefficients).

        # The following table shows how the values of Y0 and Z0 are found (the third column are the values for P(y, z) = 304 y2 + 725 yz + 432 z2):

        # Terms of the continued fraction and convergents
        # cn	yn	zn	P(yn, zn)
        #  	1	0	
        # -2	-2	1	198
        # 1	-1	1	11
        # 5	-7	6	-2
        # 8	-57	49	3
        # 5	-292	251	-12
        # 1	-349	300	4
        # 3	-1339	1151	-9
        # 1	-1688	1451	8
        # 1	-3027	2602	-6
        # 2	-7742	6655	6
        # 2	-18511	15912	-8
        # 1	-26253	22567	9
        # 1	-44764	38479	-4
        # 3	-160545	138004	12
        # 1	-205309	176483	-3
        # 5	-1 187090	1 020419	2
        # 8	-9 702029	8 339835	-11
        # 1	-10 889119	9 360254	6
        # 2	-31 480267	27 060343	-1
        # 17	-546 053658	469 386085	6
        # 2	-1123 587583	965 832513	-11
        # 1	-1669 641241	1435 218598	2
        # 8	-14480 717511	12447 581297	-3
        # 5	-74073 228796	63673 125083	12
        # 1	-88553 946307	76120 706380	-4
        # 3	-339735 067717	292035 244223	9
        # 1	-428289 014024	368155 950603	-8
        # 1	-768024 081741	660191 194826	6
        # 2	-1 964337 177506	1 688538 340255	-6
        # 2	-4 696698 436753	4 037267 875336	8
        # 1	-6 661035 614259	5 725806 215591	-9
        # 1	-11 357734 051012	9 763074 090927	4
        # 3	-40 734237 767295	35 015028 488372	-12
        # 1	-52 091971 818307	44 778102 579299	3
        # 5	-301 194096 858830	258 905541 384867	-2
        # 8	-2461 644746 688947	2116 022433 658235	11
        # 1	-2762 838843 547777	2374 927975 043102	-6
        # 2	-7987 322433 784501	6865 878383 744439	1
        # 17	-138547 320217 884294	119094 860498 698565	-6
        # 2	-285081 962869 553089	245055 599381 141569	11
        # 1	-423629 283087 437383	364150 459879 840134	-2
        # Notice that yn = cn yn-1 + yn-2 and zn = cn zn-1 + zn-2.

        # The signs in the third column are alternated, so the numbers will repeat after an even number of convergents. Therefore two entire periods should be considered if the period length is odd. If it is even, only one period should be considered. With these solutions and the recurrence relation to be developed in the next section we can find all solutions of the homogeneous equation.

        # Y0 = -7987 322433 784501 16
        # Z0 = 6865 878383 744439 16
        # Since X0 = 19 Y0 + 24 Z0:
        # X0 = 13021 954967 961017 17
        # Y0 = -7987 322433 784501 16
        # Since the equation Ax2 + Bxy + Cy2 + F = 0 does not change when x is replaced by -x and y is replaced by -y simultaneously we have another solution:

        # X0 = -13021 954967 961017 17
        # Y0 = 7987 322433 784501 16
        # Now we must consider the continued fraction of the other root: t = -
        # √313 + 725
        # 608

        # The expansion is -2 + //1, 3, 1, 1, 17, 2, 1, 8, 5, 1, 3, 1, 1, 2, 2, 1, 1, 3, 1, 5, 8, 1, 2// (the period has 19 coefficients).

        # The following table shows how the values of Y0 and Z0 are found (the third column are the values for P(y, z) = 304 y2 + 725 yz + 432 z2):

        # Terms of the continued fraction and convergents
        # cn	yn	zn	P(yn, zn)
        #  	1	0	
        # -2	-2	1	198
        # 1	-1	1	11
        # 3	-5	4	12
        # 1	-6	5	-6
        # 1	-11	9	1
        # 17	-193	158	-6
        # 2	-397	325	11
        # 1	-590	483	-2
        # 8	-5117	4189	3
        # 5	-26175	21428	-12
        # This table is not complete, but there are no solutions in the section not shown.

        # Y0 = 11
        # Z0 = -9
        # Since X0 = 19 Y0 + 24 Z0:

        # X0 = -7
        # Y0 = 11

        # X0 = 7
        # Y0 = -11
        # Since 2 * 2 is a divisor of the constant term (-24), the solutions should be 2 times the solutions of 18 u2 + 41 uv + 19 v2 - 6 = 0.
        # We have to find the continued fraction expansion of the roots of 18 t2 + 41 t + 19 = 0, that is, t = 
        # √313 - 41
        # 38

        # The continued fraction expansion is:
        # -1 + //2, 1, 5, 8, 1, 2, 17, 2, 1, 8, 5, 1, 3, 1, 1, 2, 2, 1, 1, 3//

        # where the periodic part is marked in bold (the period has 19 coefficients).

        # The following table shows how the values of U0 and V0 are found (the third column are the values for P(u, v) = 18 u2 + 41 uv + 19 v2):

        # Terms of the continued fraction and convergents
        # cn	un	vn	P(un, vn)
        #  	1	0	
        # -1	-1	1	-4
        # 2	-1	2	12
        # 1	-2	3	-3
        # 5	-11	17	2
        # 8	-90	139	-11
        # 1	-101	156	6
        # 2	-292	451	-1
        # 17	-5065	7823	6
        # 2	-10422	16097	-11
        # 1	-15487	23920	2
        # 8	-134318	207457	-3
        # 5	-687077	1 061205	12
        # 1	-821395	1 268662	-4
        # 3	-3 151262	4 867191	9
        # 1	-3 972657	6 135853	-8
        # 1	-7 123919	11 003044	6
        # 2	-18 220495	28 141941	-6
        # 2	-43 564909	67 286926	8
        # 1	-61 785404	95 428867	-9
        # 1	-105 350313	162 715793	4
        # 3	-377 836343	583 576246	-12
        # 1	-483 186656	746 292039	3
        # 5	-2793 769623	4315 036441	-2
        # 8	-22833 343640	35266 583567	11
        # 1	-25627 113263	39581 620008	-6
        # 2	-74087 570166	114429 823583	1
        # 17	-1 285115 806085	1 984888 620919	-6
        # 2	-2 644319 182336	4 084207 065421	11
        # 1	-3 929434 988421	6 069095 686340	-2
        # 8	-34 079799 089704	52 636972 556141	3
        # 5	-174 328430 436941	269 253958 467045	-12
        # 1	-208 408229 526645	321 890931 023186	4
        # 3	-799 553119 016876	1234 926751 536603	-9
        # 1	-1007 961348 543521	1556 817682 559789	8
        # 1	-1807 514467 560397	2791 744434 096392	-6
        # 2	-4622 990283 664315	7140 306550 752573	6
        # 2	-11053 495034 889027	17072 357535 601538	-8
        # 1	-15676 485318 553342	24212 664086 354111	9
        # 1	-26729 980353 442369	41285 021621 955649	-4
        # 3	-95866 426378 880449	148067 728952 221058	12
        # As explained above, x = 2u and y = 2v, so:

        # X0 = -202
        # Y0 = 312

        # X0 = 202
        # Y0 = -312

        # X0 = -10130
        # Y0 = 15646

        # X0 = 10130
        # Y0 = -15646

        # X0 = -14 247838 8
        # Y0 = 22 006088 8

        # X0 = 14 247838 8
        # Y0 = -22 006088 8

        # X0 = -9245 980567 328630 16
        # Y0 = 14280 613101 505146 17

        # X0 = 9245 980567 328630 16
        # Y0 = -14280 613101 505146 17
        # The other root of the equation 18 t2 + 41 t + 19 = 0 is t = -
        # √313 + 41
        # 38

        # Its continued fraction expansion is:
        # -2 + //2, 1, 2, 2, 1, 1, 3, 1, 5, 8, 1, 2, 17, 2, 1, 8, 5, 1, 3, 1//

        # where the periodic part is marked in bold (the period has 19 coefficients).

        # The following table shows how the values of U0 and V0 are found (the third column are the values for P(u, v) = 18 u2 + 41 uv + 19 v2):

        # Terms of the continued fraction and convergents
        # cn	un	vn	P(un, vn)
        #  	1	0	
        # -2	-2	1	9
        # 2	-3	2	-8
        # 1	-5	3	6
        # 2	-13	8	-6
        # 2	-31	19	8
        # 1	-44	27	-9
        # 1	-75	46	4
        # 3	-269	165	-12
        # 1	-344	211	3
        # 5	-1989	1220	-2
        # 8	-16256	9971	11
        # 1	-18245	11191	-6
        # 2	-52746	32353	1
        # 17	-914927	561192	-6
        # 2	-1 882600	1 154737	11
        # 1	-2 797527	1 715929	-2
        # 8	-24 262816	14 882169	3
        # 5	-124 111607	76 126774	-12
        # 1	-148 374423	91 008943	4
        # 3	-569 234876	349 153603	-9
        # 1	-717 609299	440 162546	8
        # 1	-1286 844175	789 316149	-6
        # 2	-3291 297649	2018 794844	6
        # 2	-7869 439473	4826 905837	-8
        # 1	-11160 737122	6845 700681	9
        # 1	-19030 176595	11672 606518	-4
        # 3	-68251 266907	41863 520235	12
        # 1	-87281 443502	53536 126753	-3
        # 5	-504658 484417	309544 154000	2
        # 8	-4 124549 318838	2 529889 358753	-11
        # 1	-4 629207 803255	2 839433 512753	6
        # 2	-13 382964 925348	8 208756 384259	-1
        # 17	-232 139611 534171	142 388292 045156	6
        # 2	-477 662187 993690	292 985340 474571	-11
        # 1	-709 801799 527861	435 373632 519727	2
        # 8	-6156 076584 216578	3775 974400 632387	-3
        # 5	-31490 184720 610751	19315 245635 681662	12
        # 1	-37646 261304 827329	23091 220036 314049	-4
        # 3	-144428 968635 092738	88588 905744 623809	9
        # 1	-182075 229939 920067	111680 125780 937858	-8
        # As explained above, x = 2u and y = 2v, so:

        # X0 = 10
        # Y0 = -6

        # X0 = -10
        # Y0 = 6

        # X0 = 6582 595298 10
        # Y0 = -4037 589688 10

        # X0 = -6582 595298 10
        # Y0 = 4037 589688 10

        # X0 = 9 258415 606510 13
        # Y0 = -5 678867 025506 13

        # X0 = -9 258415 606510 13
        # Y0 = 5 678867 025506 13

        # X0 = 464 279223 068342 15
        # Y0 = -284 776584 090312 15

        # X0 = -464 279223 068342 15
        # Y0 = 284 776584 090312 15
        # Find recurrences among the solutions of the homogeneous equation
        # Now that some solutions of the original equation were found, we will find other solutions, in fact, a family of infinite solutions, where:
        # Xn+1 = P Xn + Q Yn
        # Yn+1 = R Xn + S Yn

        # where P, Q, R and S should be determined.

        # Let M(x, y) = Ax2 + Bxy + Cy2 = M and N(u, v) = u2 + Buv + ACv2 = N.

        # M(p, q) = Ap2 + Bpq + Cq2

        # M(p, q)/A = p2 + (B/A)pq + (C/A)q2

        # M(p, q)/A = p2 + Dpq + Eq2

        # M(p/q, 1)/A = (p/q)2 + D(p/q) + E    (12)

        # The roots of M(p/q, 1)/A = (p/q - J) (p/q - J') = 0  (13) are:

        # J = 
        # -B +  B2 - 4AC
        # 2A
        #  and J' = 
        # -B -  B2 - 4AC
        # 2A

        # It can be easily shown by equating (12) and (13) that:

        # J2 = -DJ - E    (14)
        # J'2 = -DJ' - E    (15)
        # J + J' = -D    (16)
        # JJ' = E    (17)

        # The roots of N(p/q, 1) = (p/q - K) (p/q - K') = 0 are:

        # K = 
        # -B +  B2 - 4AC
        # 2A
        #  and K' = 
        # -B -  B2 - 4AC
        # 2A

        # so K = AJ, K' = AJ'    (18)

        # M(p, q)/A = (p - Jq)(p - J'q) = M    (19)

        # N(r, s) = (r - Ks)(r - K's) = N    (20)

        # From (18) we obtain:

        # (p - Jq)(r - Ks) = (p - Jq)(r - AJs) = (pr - AJps - Jqr + AJ2qs)

        # From (14) we obtain:

        # [pr - AJps - Jqr + A(-DJ - E)qs] = (pr - AEqs) - (Aps + qr + AEqs)J = (pr - Cqs) - (Aps + qr + Bqs)J    (21)

        # From (18) we obtain:

        # (p - J'q)(r - K's) = (p - J'q)(r - AJ's) = (pr - AJ'ps - J'qr + AJ'2qs)

        # From (15) we obtain:

        # [pr - AJ'ps - J'qr + A(-DJ' - E)qs] = (pr - AEqs) - (Aps + qr + AEqs)J' = (pr - Cqs) - (Aps + qr + Bqs)J'    (22)

        # Let X = pr - Cqs and Y = Aps + qr + Bqs    (23).

        # Multiplying (21) by (22) we obtain:

        # (M(p, q)/A) N(r, s) = (X - YJ) (X - YJ') = X2 - (J + J')XY + JJ'Y2

        # Multiplying equations (16) and (17) we obtain: (M(p, q)/A) N(r, s) = X2 + DY + EY2

        # Multiplying by A we get (from (19) and (20)):

        # AX2 + BXY + CY2 = MN

        # Letting M = -F and N = 1 we can see that X and Y are also solutions of the original equation.

        # Let r and s be a solution to N(r, s) = r2 + Brs + ACs2 = 1,
        # Xn = p, Yn = q, Xn+1 = X and Yn+1 = Y (since the last two pairs of numbers are solutions to the original equation).

        # From (23) we obtain:

        # Xn+1 = rXn - CsYn+1
        # Yn+1 = AsXn + rYn+1 + BsYn+1

        # This means that:

        # Xn+1 = P Xn + Q Yn

        # Yn+1 = R Xn + S Yn

        # P = r    (24)
        # Q = -Cs    (25)
        # R = As    (26)
        # S = r + Bs    (27)
        # where
        # r2 + Brs + ACs2 = 1    (28)

        # Credits: This method was e-mailed to me by Iain Davidson. I've made some modifications.

        # Find solutions of the general quadratic equation
        # Ax2 + Bxy + Cy2 + Dx + Ey + F = 0
        # Multiplying the equation by 4A:

        # 4A2x2 + 4ABxy + 4ACy2 + 4ADx + 4AEy + 4AF = 0
        # (2Ax + By + D)2 - (By + D)2 + 4ACy2 + 4AEy + 4AF = 0
        # (2Ax + By + D)2 + (4AC - B2)y2 + (4AE - 2BD)y + (4AF - D2) = 0

        # Let x1 = 2Ax + By + D
        # and g = gcd(4AC - B2, 2AE - BD).

        # Multiplying by 
        # 4AC - B2
        # g
        # :

        # 4AC - B2
        # g
        # x12 + 
        # (4AC - B2)2
        # g
        # y2 + 
        # 2(4AC - B2) (2AE - BD)
        # g
        # y + 
        # (4AC - B2) (4AF - D2)
        # g
        #  = 0

        # 4AC - B2
        # g
        # x12 + g y12 + 
        # (4AC - B2) (4AF - D2) - (2AE - BD)2
        # g
        #  = 0

        # 4AC - B2
        # g
        # x12 + g y12 + 
        # 4A(4ACF - AE2 - B2F + BDE - CD2)
        # g
        #  = 0

        # where:

        # y1 = 
        # 4AC - B2
        # g
        #  y + 
        # 2AE - BD
        # g

        # Find recurrences among the solutions of the general quadratic equation
        # We will assume that the solutions will have the form:
        # Xn+1 = P Xn + Q Yn + K
        # Yn+1 = R Xn + S Yn + L

        # Replacing in the original equation x by Px + Qy + K and y by Rx + Sy + L:

        # A(Px + Qy + K)2 + B(Px + Qy + K) (Rx + Sy + L) + C(Rx + Sy + L)2 + D(Px + Qy + K) + E(Rx + Sy + L) + F = 0

        # (AP2 + BPR + CR2)x2 + (2APQ + B(PS+QR) + 2CRS)xy + (AQ2 + BQS + CS2)y2 + (2AKP + B(KR+LP) + 2CLR + DP + ER)x + (2AKQ + B(KS+LQ) + 2CLS + DQ + ES)y + (AK2 + BKL + CL2 + DK + EL + F) = 0    (29)

        # Now we will investigate the values inside the parentheses.

        # From (24) and (26) we obtain:
        # AP2 + BPR + CR2 = Ar2 + BrAs + CA2s2 = A(r2 + Brs + ACs2)

        # From equation (28) we obtain:

        # AP2 + BPR + CR2 = A    (30)

        # From (24) to (27) we obtain:
        # 2APQ + B(PS+QR) + 2CRS = 2Ar(-Cs) + B[r(r+Bs)+(-Cs)As] + 2CAs(r+Bs) = -2ACrs + B(r2+Bs-ACs2) + 2ACrs + 2ABCs2 = B(r2+Bs+ACs2)

        # From equation (28) we obtain:

        # 2APQ + B(PS+QR) + 2CRS = B    (31)

        # From (25) and (27) we obtain:
        # AQ2 + BQS + CS2 = AC2s2 + B(-Cs)(r+Bs) + C(r+Bs)2 = AC2s2 - BCrs - B2Cs2 + Cr2 + 2BCrs + B2Cs2 = AC2 + BCrs + Cr2 = C(r2 + Brs + ACs2)

        # From equation (28) we obtain:

        # AQ2 + BQS + CS2 = C    (32)

        # This means that 2AKP + B(KR+LP) + 2CLR + DP + ER = D and 2AKQ + B(KS+LQ) + 2CLS + DQ + ES = E.

        # These two equations are equivalent to:

        # (2AP+BR)K + (BP+2CR)L = -D(P-1) - ER
        # and (2AQ+BS)K + (BQ+2CS)L = -DQ - E(S-1)

        # Solving the equation system for K and L:

        # K = 
        # D[BQ - 2C(PS-QR-S)] + E[B(PS-RQ-P) - 2CR]
        # 4AC (PS - QR) + B2 (QR - PS)

        # L = 
        # D[B(PS-RQ-S) - 2AQ] + E[BR - 2A(PS-RQ-P)]
        # 4AC (PS - QR) + B2 (QR - PS)

        # Since PS - QR = r(r+Bs) - (-Cs)As = r2 + Brs + ACs2 = 1, these equations can be simplified to:

        # K = 
        # D[BQ - 2C(1-S)] + E[B(1-P) - 2CR]
        # 4AC - B2

        # L = 
        # D[B(1-S) - 2AQ] + E[BR - 2A(1-P)]
        # 4AC - B2
        # Now we must show that the expression inside the right parentheses of (29) equals F. This means that we have to prove that the values of K and L just found verify the equation Z = AK2 + BKL + CL2 + DK + EL = 0    (33).

        # The expansion is very complicated and will not be reproduced here, but fortunately it is a multiple of 4AC-B2, so it cancels the square in the denominator, since it is (4AC-B2)2.

        # This means that Z(4AC-B2) is an integer number and it is equal to:

        # AD2Q2 - 2ADEPQ + AE2P2 - AE2 + BD2QS - BDEPS - BDEQR + BDE + BE2PR + CD2S2 - CD2 - 2CDERS + CE2R2

        # Reordering terms:

        # AD2Q2 + BD2QS + CD2S2 - CD2 - 2ADEPQ - BDEPS - BDEQR - 2CDERS + BDE + AE2P2 + BE2PR + CE2R2 - AE2

        # D2(AQ2 + BQS + CS2) - CD2 - DE(2APQ + BPS + BQR + 2CRS) + BDE + E2(AP2 + BPR + CR2) - AE2

        # From (30), (31) and (32):

        # Z(4AC-B2) = CD2 - CD2 - BDE + BDE + AE2 - AE2 = 0

        # This means that Z = 0, so (33) holds, then (29) holds too.

        # Let K = 
        # KDD + KEE
        # 4AC - B2
        #  and L = 
        # LDD + LEE
        # 4AC - B2
        #     (34)

        # To continue simplifying the expressions we should note the following:

        # KD = BQ - 2C(1 - S)
        # KD = B(-Cs) - 2C(1 - r - Bs)
        # KD = -BCs - 2C + 2Cr + 2BCs
        # KD = C(-2 + 2r + Bs)    (35)
        # KD = C(P + S - 2)

        # LE = BR - 2A(1 - P)
        # LE = ABs - 2A + 2Ar
        # LE = A(-2 + 2r + Bs)
        # LE = A(P + S - 2)

        # KE = B(1 - P) - 2CR
        # KE = B(1 - r) - 2ACs
        # KE = B - Br - 2ACs    (36)

        # LD = B(1 - S) - 2AQ
        # LD = B(1 - r - Bs) + 2ACs
        # LD = B - Br - B2s + 2ACs

        # LD - KE = (4AC - B2)s    (37)

        # So:

        # K = 
        # CD(P+S-2) + E(B-Br-2ACs)
        # 4AC - B2

        # L = 
        # D(B-Br-2ACs) + AE(P+S-2)
        # 4AC - B2
        #  + Ds
        # Generally the numerators will not be multiple of 4AC - B2, so using this formula we cannot find a recurrence for all values of D and E.

        # For some values of D and E there will be solutions, as shown below. Using equations (24) - (27):

        # KDLE - KELD = 4ACr2 + 4ABCrs + 4A2C2s2 - B2r2 - B3rs - AB2Cs2 - 4ABCs - B3s + 4AC - B2 - 8ACr + 2B2r =

        # = (4AC - B2) (r2 + Brs + ACs2) - (4AC - B2)Bs + (4AC - B2) - (4AC - B2)2r =

        # = (4AC - B2) (2 - 2r - Bs)

        # The equal signs shown below mean congruence mod 4AC - B2.

        # KDLE - KELD = 0 => KD/KE = LD/LE    (38)

        # Since K and L must be integers they should be (from (34)):

        # KDD + KEE = 0 => E = (-KD/KE)D    (39)

        # LDD + LEE = 0 => E = (-LD/LE)D

        # These equations are consistent because of equation (38).

        # In some cases (see example 6) we can find a recurrence by using the solutions -r and -s since (-r)2 + B(-r)(-s) + AC(-s)2 = r2 + Brs + ACs2 = 1.

        # If no solutions were found (as in example 7), we should use the next pair of solutions (r1, s1) of r2 + Brs + ACs2 = 1 because there will always be solutions as shown below.

        # First we should find r1 and s1 from r and s. To do that we use the formulas (24) - (28).

        # r1 = r r + (-ACs)s = r2 - ACs2
        # s1 = s r + (r + Bs)s = 2rs + Bs2

        # Now the values of r and s should be replaced by r1 and s1.

        # From (24): P1 = r1 = r2 - ACs2
        # From (25): Q1 = -Cs1 = -C(2rs + Bs2)
        # From (26): R1 = As1 = A(2rs + Bs2)
        # From (27): S1 = r1 + Bs1 = r2 + 2Brs + (B2 - AC)s2

        # From (35):

        # K1D = C(-2 + 2r1 + Bs1)
        # K1D = C[-2 + 2(r2 - ACs2) + B(2rs + Bs2)]
        # K1D = C[-2 + 2(r2 + Brs + ACs2) - 4ACs2 + B2s2]
        # K1D = C[-2 + 2 + (B2 - 4AC)s2]
        # K1D = (B2 - 4AC)Cs2

        # From (36):

        # K1E = B - Br1 - 2ACs1
        # K1E = B - Br2 + ABCr2 - 4ACrs - 2ABCr2
        # K1E = B - B(r2 + ACs2) - 4ACrs
        # K1E = B - B(r2 + ACs2 + Brs - Brs) - 4ACrs
        # K1E = B - B(1 - Brs) - 4ACrs
        # K1E = (B2 - 4AC)rs

        # From (37):

        # L1D - K1E = (4AC - B2)s1
        # L1D = (B2 - 4AC) (rs - 2rs - Bs2)
        # L1D = (B2 - 4AC) (-rs - Bs2)

        # Therefore:

        # K1 = 
        # K1DD + K1EE
        # 4AC - B2
        #  = -CDs2 - Ers

        # L1 = 
        # L1DD + L1EE
        # 4AC - B2
        #  = Ds(r + Bs) - AEs2

        # So, finally:

        # Xn+1 = (r2 - ACs2)Xn - Cs(2r+Bs)Yn - CDs2 - Ers    (40)

        # Yn+1 = As(2r+Bs)Xn + [r2 + 2Brs + (B2-AC)s2]Yn + Ds(r+Bs) - AEs2    (41)
        # Notice that in this case, in order to find the solutions using the continued fraction method, we will need to compute two entire periods if the period length is even and four if it is odd.

        # Example 6: 3x2 + 13xy + 5y2 + Dx + Ey + F = 0

        # The first solution of r2 + Brs + ACs2 = r2 + 13 rs + 15 s2 = 1 using the continued fraction method is r = -8351 and s = 6525.

        # P = r = -8351
        # Q = -Cs = -32625
        # R = As = 19575
        # S = r + Bs = 76474

        # K = 
        # CD(P+S-2) + E(B-Br-2ACs)
        # 4AC-B2
        #  = 
        # -340605
        # 109
        # D + 
        # 87174
        # 109
        # E

        # L = 
        # D(B-Br-2ACs) + AE(P+S-2)
        # 4AC-B2
        #  + Ds = 
        # 798399
        # 109
        # D - 
        # 204363
        # 109
        # E

        # The numerator of K (or L) is not a multiple of the denominator (4AC - B2 = -109), so there is no recurrence with the values of P, Q, R, S shown above, except for special cases (according to (39), when E ≡ 93 D (mod 109)).

        # Using the solution r = 8351, s = -6525 we get:

        # P = r = 8351
        # Q = -Cs = 32625
        # R = As = -19575
        # S = r + Bs = -76474

        # K = 
        # CD(P+S-2) + E(B-Br-2ACs)
        # 4AC-B2
        #  = 3125 D - 800 E

        # L = 
        # D(B-Br-2ACs) + AE(P+S-2)
        # 4AC-B2
        #  + Ds = -7325 D + 1875 E

        # So, the recursive relation between solutions is:

        # Xn+1 = 8351 Xn - 32625 Yn + (3125 D - 800 E)

        # Yn+1 = -19575 Xn - 76474 Yn + (-7325 D + 1875 E)
        # Check: Knowing that x = 2, y = 3 is a solution of 3x2 + 13xy + 5y2 - 11x - 7y - 92 = 0, find other two solutions.

        # Replacing D = -11 and E = -7 in the previous equations:

        # Xn+1 = 8351 Xn - 32625 Yn - 28775
        # Yn+1 = -19575 Xn + 76474 Yn + 67450

        # So, replacing here X0 = 2 and Y0 = 3, we find X1 = 85802 and Y1 = -201122.

        # and replacing X1 = 85802 and Y1 = -201122, we find X2 = -5845 101523 and Y2 = 13701 097128.

        # Replacing these values in the original equation we can check that these values are correct.

        # Example 7: 3x2 + 14xy + 6y2 + Dx + Ey + F = 0

        # The first solution of r2 + Brs + ACs2 = r2 + 14 rs + 18 s2 = 1 using the continued fraction method is r = -391 and s = 273.

        # P = r = -391
        # Q = -Cs = -1638
        # R = As = 819
        # S = r + Bs = 3431

        # K = 
        # CD(P+S-2) + E(B-Br-2ACs)
        # 4AC-B2
        #  = -147 D + 35 E

        # L = 
        # D(B-Br-2ACs) + AE(P+S-2)
        # 4AC-B2
        #  + Ds = 308 D - 
        # 147
        # 2
        # E

        # The numerator of L is not a multiple of the denominator (4AC - B2 = -124), so there is no recurrence with the values of P, Q, R, S shown above, except for special cases (when E is even).

        # Using the solution r = 391, s = -273 we get:

        # P = r = 391
        # Q = -Cs = 1638
        # R = As = -819
        # S = r + Bs = -3431

        # K = 
        # CD(P+S-2) + E(B-Br-2ACs)
        # 4AC-B2
        #  = 
        # -4563
        # 31
        # D - 
        # 1092
        # 31
        # E

        # L = 
        # D(B-Br-2ACs) + AE(P+S-2)
        # 4AC-B2
        #  + Ds = 
        # 4563
        # 62
        # D - 
        # 9555
        # 31
        # E

        # The numerator of K (or L) is not a multiple of the denominator (4AC - B2 = -124), so there is no recurrence with the values of P, Q, R, S shown above, except for special cases.

        # Using (40) and (41):

        # P1 = r2 - ACs2 = -1188641
        # Q1 = -Cs(2r+Bs) = -4979520
        # R1 = As(2r+Bs) = 2489760
        # S1 = r2 + 2Brs + (B2-AC)s2 = 10430239
        # K1 = -CDs2 - Ers = -106743 D + 447174 E
        # L1 = Ds(r+Bs) - AEs2 = 936663 D - 223587 E

        # So, the recursive relation between solutions is:

        # Xn+1 = -1188641 Xn - 4979520 Yn + (106743 D - 447174 E)

        # Yn+1 = 2489760 Xn + 10430239 Yn + (936663 D - 223587 E)
        # Check: Knowing that x = 4, y = 7 is a solution of 3x2 + 14xy + 6y2 - 17x - 23y - 505 = 0, find other two solutions.

        # Replacing D = -17 and E = -23 in the previous equations:

        # Xn+1 = -1188641 Xn - 4979520 Yn + 5146869

        # Yn+1 = 2489760 Xn + 10430239 Yn - 10780770

        # So, replacing here X0 = 4 and Y0 = 7, we find X1 = -34 464335 and Y1 = 72 189943.

        # and replacing X1 = -34 464335 and Y1 = 72 189943, we find X2 = -318 505538 201756 and Y2 = 667 150425 396007.

        # Replacing these values in the original equation we can check that these values are correct.

'''TESTS'''
# diophantine((5,0,-1,14,0,1))

diophantine = Diophantine((3,10,3,0,0,0))
diophantine.print_count_cutoff(20)
# print_magnitude_cutoff(generator_square(x_value="all", y_value="all"), cutoff_x=1, cutoff_y=1)

# print(bezout_coefficients(240, 46))