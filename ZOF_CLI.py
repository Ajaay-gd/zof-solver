import math
import numpy as np

def get_function():
    """Get function from user input"""
    print("\nEnter the function f(x) = 0")
    print("Use ** for power, e.g., x**3 - x - 2")
    func_str = input("f(x) = ")
    
    def f(x):
        return eval(func_str)
    
    return f, func_str

def derivative(f, x, h=1e-8):
    """Numerical derivative"""
    return (f(x + h) - f(x - h)) / (2 * h)

def bisection_method(f, a, b, tol, max_iter):
    """Bisection Method"""
    print("\n" + "="*70)
    print("BISECTION METHOD")
    print("="*70)
    
    if f(a) * f(b) > 0:
        print("Error: f(a) and f(b) must have opposite signs")
        return None
    
    print(f"{'Iter':<6} {'a':<12} {'b':<12} {'c':<12} {'f(c)':<12} {'Error':<12}")
    print("-"*70)
    
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        error = abs(b - a) / 2
        
        print(f"{i:<6} {a:<12.6f} {b:<12.6f} {c:<12.6f} {fc:<12.6f} {error:<12.6f}")
        
        if abs(fc) < tol or error < tol:
            print("\n" + "="*70)
            print(f"Root found: {c:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return c
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    print("\nMax iterations reached")
    return c

def regula_falsi_method(f, a, b, tol, max_iter):
    """Regula Falsi (False Position) Method"""
    print("\n" + "="*70)
    print("REGULA FALSI METHOD")
    print("="*70)
    
    if f(a) * f(b) > 0:
        print("Error: f(a) and f(b) must have opposite signs")
        return None
    
    print(f"{'Iter':<6} {'a':<12} {'b':<12} {'c':<12} {'f(c)':<12} {'Error':<12}")
    print("-"*70)
    
    c_old = a
    fa = f(a)
    fb = f(b)
    
    for i in range(1, max_iter + 1):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        error = abs(c - c_old)
        
        print(f"{i:<6} {a:<12.6f} {b:<12.6f} {c:<12.6f} {fc:<12.6f} {error:<12.6f}")
        
        if abs(fc) < tol or error < tol:
            print("\n" + "="*70)
            print(f"Root found: {c:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return c
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        c_old = c
    
    print("\nMax iterations reached")
    return c

def secant_method(f, x0, x1, tol, max_iter):
    """Secant Method"""
    print("\n" + "="*70)
    print("SECANT METHOD")
    print("="*70)
    
    print(f"{'Iter':<6} {'x0':<12} {'x1':<12} {'x2':<12} {'f(x2)':<12} {'Error':<12}")
    print("-"*70)
    
    f0 = f(x0)
    f1 = f(x1)
    
    for i in range(1, max_iter + 1):
        if abs(f1 - f0) < 1e-12:
            print("Error: Division by zero")
            return None
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = f(x2)
        error = abs(x2 - x1)
        
        print(f"{i:<6} {x0:<12.6f} {x1:<12.6f} {x2:<12.6f} {f2:<12.6f} {error:<12.6f}")
        
        if abs(f2) < tol or error < tol:
            print("\n" + "="*70)
            print(f"Root found: {x2:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return x2
        
        x0, f0 = x1, f1
        x1, f1 = x2, f2
    
    print("\nMax iterations reached")
    return x2

def newton_raphson_method(f, x0, tol, max_iter):
    """Newton-Raphson Method"""
    print("\n" + "="*70)
    print("NEWTON-RAPHSON METHOD")
    print("="*70)
    
    print(f"{'Iter':<6} {'x':<12} {'f(x)':<12} {'f\'(x)':<12} {'x_new':<12} {'Error':<12}")
    print("-"*70)
    
    x = x0
    
    for i in range(1, max_iter + 1):
        fx = f(x)
        fpx = derivative(f, x)
        
        if abs(fpx) < 1e-12:
            print("Error: Derivative too small")
            return None
        
        x_new = x - fx / fpx
        error = abs(x_new - x)
        
        print(f"{i:<6} {x:<12.6f} {fx:<12.6f} {fpx:<12.6f} {x_new:<12.6f} {error:<12.6f}")
        
        if abs(fx) < tol or error < tol:
            print("\n" + "="*70)
            print(f"Root found: {x_new:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return x_new
        
        x = x_new
    
    print("\nMax iterations reached")
    return x

def fixed_point_method(g, x0, tol, max_iter):
    """Fixed Point Iteration Method"""
    print("\n" + "="*70)
    print("FIXED POINT ITERATION METHOD")
    print("="*70)
    
    print(f"{'Iter':<6} {'x':<12} {'g(x)':<12} {'Error':<12}")
    print("-"*70)
    
    x = x0
    
    for i in range(1, max_iter + 1):
        gx = g(x)
        error = abs(gx - x)
        
        print(f"{i:<6} {x:<12.6f} {gx:<12.6f} {error:<12.6f}")
        
        if error < tol:
            print("\n" + "="*70)
            print(f"Root found: {gx:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return gx
        
        x = gx
    
    print("\nMax iterations reached")
    return x

def modified_secant_method(f, x0, delta, tol, max_iter):
    """Modified Secant Method"""
    print("\n" + "="*70)
    print("MODIFIED SECANT METHOD")
    print("="*70)
    
    print(f"{'Iter':<6} {'x':<12} {'f(x)':<12} {'x_new':<12} {'Error':<12}")
    print("-"*70)
    
    x = x0
    
    for i in range(1, max_iter + 1):
        fx = f(x)
        fxd = f(x + delta * x)
        
        if abs(fxd - fx) < 1e-12:
            print("Error: Division by zero")
            return None
        
        x_new = x - (fx * delta * x) / (fxd - fx)
        error = abs(x_new - x)
        
        print(f"{i:<6} {x:<12.6f} {fx:<12.6f} {x_new:<12.6f} {error:<12.6f}")
        
        if abs(fx) < tol or error < tol:
            print("\n" + "="*70)
            print(f"Root found: {x_new:.8f}")
            print(f"Final error: {error:.8f}")
            print(f"Iterations: {i}")
            print("="*70)
            return x_new
        
        x = x_new
    
    print("\nMax iterations reached")
    return x

def main():
    """Main CLI application"""
    print("="*70)
    print(" "*20 + "ZERO OF FUNCTIONS SOLVER")
    print("="*70)
    
    methods = {
        '1': 'Bisection Method',
        '2': 'Regula Falsi Method',
        '3': 'Secant Method',
        '4': 'Newton-Raphson Method',
        '5': 'Fixed Point Iteration',
        '6': 'Modified Secant Method'
    }
    
    print("\nAvailable Methods:")
    for key, value in methods.items():
        print(f"{key}. {value}")
    
    choice = input("\nSelect method (1-6): ")
    
    if choice not in methods:
        print("Invalid choice!")
        return
    
    if choice == '5':
        print("\nEnter g(x) for fixed point iteration (x = g(x))")
        print("Example: For x^3 - x - 2 = 0, use g(x) = (x + 2)**(1/3)")
        func_str = input("g(x) = ")
        g = lambda x: eval(func_str)
        x0 = float(input("Initial guess x0: "))
    else:
        f, func_str = get_function()
        print(f"\nSolving: {func_str} = 0")
    
    tol = float(input("Tolerance: "))
    max_iter = int(input("Maximum iterations: "))
    
    if choice == '1':
        a = float(input("Lower bound a: "))
        b = float(input("Upper bound b: "))
        bisection_method(f, a, b, tol, max_iter)
    
    elif choice == '2':
        a = float(input("Lower bound a: "))
        b = float(input("Upper bound b: "))
        regula_falsi_method(f, a, b, tol, max_iter)
    
    elif choice == '3':
        x0 = float(input("Initial guess x0: "))
        x1 = float(input("Initial guess x1: "))
        secant_method(f, x0, x1, tol, max_iter)
    
    elif choice == '4':
        x0 = float(input("Initial guess x0: "))
        newton_raphson_method(f, x0, tol, max_iter)
    
    elif choice == '5':
        fixed_point_method(g, x0, tol, max_iter)
    
    elif choice == '6':
        x0 = float(input("Initial guess x0: "))
        delta = float(input("Delta (δ): "))
        modified_secant_method(f, x0, delta, tol, max_iter)

if __name__ == "__main__":
    main()