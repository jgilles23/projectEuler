#Method from https://en.wikipedia.org/wiki/Newton%27s_method_in_optimization#Higher_dimensions

from typing import List, Tuple, Callable
import numpy as np
import sympy

def newton(x: np.ndarray, f: Callable, gf: Callable, hf: Callable, lr=0.01, lr_decr=0.999, maxiter=100, tol=0.001) -> Tuple[np.ndarray, List[np.ndarray], int]:
    """
    Applies the Newton's method to find the minimum of a multidimensional function, using the update criterion: 
    x_k+1 = x_k - lr * inverse(hf(x)) * gf(x), for the k-th iteration.

    Args:
        x (np.ndarray): An array representing the initial point where the algorithm starts.
        f (Callable): Objective function to minimize.
        gf (Callable): Gradient of the objective function.
        hf (Callable): Hessian of the objective function.
        lr (float, optional): Initial learning rate. Default is 0.01.
        lr_decr (float, optional): Decay factor for the learning rate. Default is 0.999.
        maxiter (int, optional): Maximum number of iterations. Default is 100.
        tol (float, optional): Tolerance for the gradient norm that determines convergence. Default is 0.001.

    Returns:
        Tuple[np.ndarray, List[np.ndarray], int]: A tuple with three elements:
            - The approximate minimum point.
            - A list of intermediate points (arrays) calculated during optimization.
            - The number of iterations performed.

    Example:
    
    # Define a 2-dimensional quadratic function: f(x, y) = x^2 + 2y^2
    def objective_function(x):
        return x[0] ** 2 + 2 * x[1] ** 2

    # Define the gradient of the objective function: f'(x, y) = [2x, 4y]
    def gradient_function(x):
        return np.array([2 * x[0], 4 * x[1]])

    # Define the Hessian of the objective function: f''(x, y) = [[2, 0], [0, 4]]
    def hessian_function(x):
        return np.array([[2, 0], [0, 4]])

    # Initial point for optimization
    initial_point = np.array([3.0, 2.0])

    # Apply the Newton's method for optimization
    result, intermediate_points, iterations = newton(initial_point, objective_function, gradient_function,
                                                                                            hessian_function)
    """
    points = [x]
    nit = 0
    gradient = gf(x)
    hessian = hf(x)
    
    while nit < maxiter and np.linalg.norm(gradient) >= tol:      
        x = x - lr * np.dot(np.linalg.inv(hessian), gradient)  # Matrix multiplication using np.dot(m1, m2)
        lr *= lr_decr  # Learning rate update: tk+1 = tk * ρ, with ρ being the decay factor.
        points.append(x)
        nit += 1
        gradient = gf(x)
        hessian = hf(x)

    return x, points, nit

# # Define a 2-dimensional quadratic function: f(x, y) = x^2 + 2y^2
# def objective_function(x):
#     return x[0] ** 2 + 2 * x[1] ** 2

# # Define the gradient of the objective function: f'(x, y) = [2x, 4y]
# def gradient_function(x):
#     return np.array([2 * x[0], 4 * x[1]])

# # Define the Hessian of the objective function: f''(x, y) = [[2, 0], [0, 4]]
# def hessian_function(x):
#     return np.array([[2, 0], [0, 4]])

# # Initial point for optimization
# initial_point = np.array([3.0, 2.0])

# # Apply the Newton's method for optimization
# #def newton(x: np.ndarray, f: Callable, gf: Callable, hf: Callable, lr=0.01, lr_decr=0.999, maxiter=100, tol=0.001) -> Tuple[np.ndarray, List[np.ndarray], int]:
# result, intermediate_points, iterations = newton(initial_point, objective_function, gradient_function, hessian_function, lr=0.1, lr_decr=0.99, maxiter=1000)
# print("result", result, "iterations", iterations)


m = 10

def Q(x):
    return m - np.sum(x[2:])

def R(x):
    return np.product(x[2:]**np.arange(2,m+1))

def Rp(x, i):
    return i*R(x)/x[i]

def Rpp(x, i, j):
    if i == j:
        return i*(i-1)*R(x)/x[i]**2
    else:
        return i*j*R(x)/x[i]/x[j]

def f(z):
    x = np.concatenate([[0,0], z])
    return -1*Q(x)*R(x)

def gf(z):
    x = np.concatenate([[0,0], z])
    return np.array([-1*(-R(x) + Q(x)*Rp(x,i)) for i in range(2,m+1)])

def hf(z):
    x = np.concatenate([[0,0], z])
    return np.array([[-1*(-Rp(x,j) - Rp(x,i) + Q(x)*Rpp(x, i,j)) for j in range(2,m+1)] for i in range(2,m+1)])

Z = np.array([0.95]*(m-1))
X = np.concatenate([[0,0], Z])

# Apply the Newton's method for optimization
#def newton(x: np.ndarray, f: Callable, gf: Callable, hf: Callable, lr=0.01, lr_decr=0.999, maxiter=100, tol=0.001) -> Tuple[np.ndarray, List[np.ndarray], int]:
result, intermediate_points, iterations = newton(Z, f, gf, hf, lr=0.01, lr_decr=0.999, maxiter=10000, tol=0.001)
print("result", result, "iterations", iterations, "P", f(result), "start", f(Z))
pass

# x2, x3 = sympy.symbols("x2 x3")

# F = -1*(3 - x2 - x3)*x2**2*x3**3
# # print(F)
# GF = [F.diff(x2), F.diff(x3)]
# # print(GF)
# HF = [[F.diff(x2).diff(x2), F.diff(x2).diff(x3)],
#       [F.diff(x2).diff(x3), F.diff(x3).diff(x3)]]
# # print(HF)


# print("Evaluation Tests")
# subs = {x2:Z[0], x3:Z[1]}
# print(f(Z), F.evalf(subs=subs))
# print(gf(Z), [a.evalf(subs=subs) for a in GF])
# print(list(hf(Z)), [[a.evalf(subs=subs) for a in b] for b in HF])

pass