# %%
import sympy
import math

# %%
# Use maths to derive the equations of the quadralateral
# # 8 Corner angles
# CAD, BAC, ABD, CBD, ACB, ACD, BDC, ADB = sympy.symbols("CAD, BAC, ABD, CBD, ACB, ACD, BDC, ADB")
# # 4 big corner angles
# BAD, ADC, BCD, ABC = sympy.symbols("BAD, ADC, BCD, ABC")
# #Side and diagonals
# AB, BC, CD, AD, AC, BD = sympy.symbols("AB, BC, CD, AD, AC, BD")

# Four given angles
CAD, BAC, ABD, CBD = sympy.symbols("BAD, BAC, ABD, CBD")
given_angles = [CAD, BAC, ABD, CBD]
# Side length
L = 1 #sympy.symbols("L")
# Temp veriable
x  = sympy.symbols("x")

# %%
# 1 Assume that the given angles are: CAD, BAC, ABD, CBD
# 2 
BAD = BAC + CAD
ABC = ABD + CBD
# 3, easy triangels
ACB = 180 - BAC - ABC
ADB = 180 - BAD - ABD
# ACB, ADB = sympy.symbols("ACB, ADB")

# 4 - law of sines
AC = L*sympy.sin(ABC*math.pi/180)/sympy.sin(ACB*math.pi/180)
# 5 - law of sines
AD = L*sympy.sin(ABD*math.pi/180)/sympy.sin(ADB*math.pi/180)
# 6 - law of cosines & sines
CD = sympy.sqrt(AD**2 + AC**2 - 2*AD*AC*sympy.cos(CAD*math.pi/180))
# ACD = sympy.solve(AD/sympy.sin(x) - CD/sympy.sin(CAD), x)
# Need to claamp between [0,1]
temp = AD*sympy.sin(CAD*math.pi/180)/CD
ACD_eq = sympy.asin(sympy.Max(0, sympy.Min(temp, 1)))*180/math.pi
print(ACD_eq) #print
ACD = sympy.symbols("ACD")
given_angles_plus_ACD = given_angles + [ACD]

#Lambdafy the ACD equation
ACD_lambda = sympy.lambdify([CAD, BAC, ABD, CBD], ACD_eq)

#Finish the solving steps assuming a numeric solution to ACD
# 7
BCD = ACB + ACD
# 8
BDC  = 180 - CBD - BCD
# 9
# ACB = ADB + BDC

def slow_numeric_eval(equation, angles, acd=None):
    #change angles to radians
    if acd is None:
        acd = ACD_lambda(*angles)
    equation_lambda = sympy.lambdify(given_angles_plus_ACD, equation)
    return equation_lambda(*angles, acd)

# Create lambdafied equations for the other 4 smalll angles
ACB_lambda = sympy.lambdify(given_angles_plus_ACD, ACB)
ADB_lambda = sympy.lambdify(given_angles_plus_ACD, ADB)
BDC_lambda = sympy.lambdify(given_angles_plus_ACD, BDC)

def get_small_angles(angles, acd):
    #Provide the given angles & acd
    return angles + [ACB_lambda(*angles, acd), 
                     acd, 
                     BDC_lambda(*angles, acd),
                     ADB_lambda(*angles, acd)]

# %%
tolerance = 10**-9
def test_with_small_angle_return(angles):
    #Given input angles, test if ACD is within tolerence, return small angles if yes
    acd = ACD_lambda(*angles)
    if math.isnan(acd):
        print(angles, acd)
        raise Exception
        return []
    acd_integer = int(round(acd))
    if abs(acd - acd_integer) < tolerance:
        # This is where we could do some sorting
        return get_small_angles(angles, acd_integer)
    else:
        return []

# Create an ordering scheme for the small angles
def test_small_angle_perfection(small_angles:list):
    #Take a list of small angle integers in order & return a sorted list of the (4) "base"
    #angles that can be used to generate the other small angles
    #a similified list will be the maximum list
    #Return True if the small angles provides are in "maximum" format
    #Test that all angles are > 0 and less than 180
    range_flag = all(x > 0 and x < 180 for x in small_angles)
    if not range_flag:
        # print("Bad Angles:", small_angles)
        return False
    small_angles_tuple = tuple(small_angles)
    options = \
        [tuple(small_angles[i:] + small_angles[:i]) for i in range(0,8,2)] + \
        [tuple(small_angles[i::-1] + small_angles[:i:-1]) for i in range(1,8,2)]
    perfect_option = max(options)
    return small_angles_tuple == perfect_option

def is_integer_angle_quad(angles, print_flag = False):
    #Input (4) angles, tests if the angles form an integer quadralteral
    #Also tests if the resultant integer quadlateral is in "perfect format"
    small_angles = test_with_small_angle_return(angles)
    if not small_angles:
        return False
    perfection_flag = test_small_angle_perfection(small_angles)
    if perfection_flag:
        if print_flag: print("Perfect:", small_angles)
        return True
    else:
        if print_flag: print("Imperfect:", small_angles)
        return False
    

#Test cases
angles =  [90,45,31,45]#[62,59,45,31] #[45, 45, 45, 45] #[20, 60, 50, 30]
is_integer_angle_quad(angles, True)

# %%
def iterate_count(method):
    #Call on a particular method to count the number of quads that fit
    #Iterate through the possible angles and count the number of perfect
    count = 0
    for cad in range(60,179):
        for bac in range(1, min(cad, 179-cad)+1):
            for abd in range(1, min(cad+1,179-cad-bac)):
                for cbd in range(1, min(cad, 179-abd, 179-bac-abd)+1):
                    count += method([cad, bac, abd, cbd])
            if bac%20 == 1:
                print([cad, bac], "Count:", count)
    print("ans", count)
    return count



# %%
# Using the law of cosines
iterate_count(is_integer_angle_quad)
#124634
#121666
# %%
# New calculation method

