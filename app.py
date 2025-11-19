from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def evaluate_function(expr, x):
    """Safely evaluate mathematical expression"""
    try:
        # Replace common math functions
        expr = expr.replace('^', '**')
        allowed_names = {
            'x': x,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'sqrt': np.sqrt,
            'abs': abs,
            'pi': np.pi,
            'e': np.e
        }
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Invalid equation: {str(e)}")

def derivative(expr, x, h=1e-8):
    """Numerical derivative"""
    return (evaluate_function(expr, x + h) - evaluate_function(expr, x - h)) / (2 * h)

def bisection_method(expr, a, b, tol, max_iter):
    """Bisection Method"""
    iterations = []
    
    try:
        fa = evaluate_function(expr, a)
        fb = evaluate_function(expr, b)
    except Exception as e:
        return {'error': str(e)}
    
    if fa * fb > 0:
        return {'error': 'f(a) and f(b) must have opposite signs'}
    
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = evaluate_function(expr, c)
        error = abs(b - a) / 2
        
        iterations.append({
            'iteration': i,
            'a': round(a, 6),
            'b': round(b, 6),
            'c': round(c, 6),
            'fc': round(fc, 6),
            'error': round(error, 6)
        })
        
        if abs(fc) < tol or error < tol:
            return {
                'iterations': iterations,
                'root': c,
                'finalError': error,
                'converged': True
            }
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    return {
        'iterations': iterations,
        'root': c,
        'finalError': error,
        'converged': False
    }

def regula_falsi_method(expr, a, b, tol, max_iter):
    """Regula Falsi Method"""
    iterations = []
    
    try:
        fa = evaluate_function(expr, a)
        fb = evaluate_function(expr, b)
    except Exception as e:
        return {'error': str(e)}
    
    if fa * fb > 0:
        return {'error': 'f(a) and f(b) must have opposite signs'}
    
    c_old = a
    
    for i in range(1, max_iter + 1):
        c = (a * fb - b * fa) / (fb - fa)
        fc = evaluate_function(expr, c)
        error = abs(c - c_old)
        
        iterations.append({
            'iteration': i,
            'a': round(a, 6),
            'b': round(b, 6),
            'c': round(c, 6),
            'fc': round(fc, 6),
            'error': round(error, 6)
        })
        
        if abs(fc) < tol or error < tol:
            return {
                'iterations': iterations,
                'root': c,
                'finalError': error,
                'converged': True
            }
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        c_old = c
    
    return {
        'iterations': iterations,
        'root': c,
        'finalError': error,
        'converged': False
    }

def secant_method(expr, x0, x1, tol, max_iter):
    """Secant Method"""
    iterations = []
    
    try:
        f0 = evaluate_function(expr, x0)
        f1 = evaluate_function(expr, x1)
    except Exception as e:
        return {'error': str(e)}
    
    for i in range(1, max_iter + 1):
        if abs(f1 - f0) < 1e-12:
            return {'error': 'Division by zero encountered'}
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = evaluate_function(expr, x2)
        error = abs(x2 - x1)
        
        iterations.append({
            'iteration': i,
            'x0': round(x0, 6),
            'x1': round(x1, 6),
            'x2': round(x2, 6),
            'f2': round(f2, 6),
            'error': round(error, 6)
        })
        
        if abs(f2) < tol or error < tol:
            return {
                'iterations': iterations,
                'root': x2,
                'finalError': error,
                'converged': True
            }
        
        x0, f0 = x1, f1
        x1, f1 = x2, f2
    
    return {
        'iterations': iterations,
        'root': x2,
        'finalError': error,
        'converged': False
    }

def newton_raphson_method(expr, x0, tol, max_iter):
    """Newton-Raphson Method"""
    iterations = []
    x = x0
    
    for i in range(1, max_iter + 1):
        try:
            fx = evaluate_function(expr, x)
            fpx = derivative(expr, x)
        except Exception as e:
            return {'error': str(e)}
        
        if abs(fpx) < 1e-12:
            return {'error': 'Derivative too small'}
        
        x_new = x - fx / fpx
        error = abs(x_new - x)
        
        iterations.append({
            'iteration': i,
            'x': round(x, 6),
            'fx': round(fx, 6),
            'fpx': round(fpx, 6),
            'x_new': round(x_new, 6),
            'error': round(error, 6)
        })
        
        if abs(fx) < tol or error < tol:
            return {
                'iterations': iterations,
                'root': x_new,
                'finalError': error,
                'converged': True
            }
        
        x = x_new
    
    return {
        'iterations': iterations,
        'root': x,
        'finalError': error,
        'converged': False
    }

def fixed_point_method(expr, x0, tol, max_iter):
    """Fixed Point Iteration Method"""
    iterations = []
    x = x0
    
    for i in range(1, max_iter + 1):
        try:
            gx = evaluate_function(expr, x)
        except Exception as e:
            return {'error': str(e)}
        
        error = abs(gx - x)
        
        iterations.append({
            'iteration': i,
            'x': round(x, 6),
            'gx': round(gx, 6),
            'error': round(error, 6)
        })
        
        if error < tol:
            return {
                'iterations': iterations,
                'root': gx,
                'finalError': error,
                'converged': True
            }
        
        x = gx
    
    return {
        'iterations': iterations,
        'root': x,
        'finalError': error,
        'converged': False
    }

def modified_secant_method(expr, x0, delta, tol, max_iter):
    """Modified Secant Method"""
    iterations = []
    x = x0
    
    for i in range(1, max_iter + 1):
        try:
            fx = evaluate_function(expr, x)
            fxd = evaluate_function(expr, x + delta * x)
        except Exception as e:
            return {'error': str(e)}
        
        if abs(fxd - fx) < 1e-12:
            return {'error': 'Division by zero encountered'}
        
        x_new = x - (fx * delta * x) / (fxd - fx)
        error = abs(x_new - x)
        
        iterations.append({
            'iteration': i,
            'x': round(x, 6),
            'fx': round(fx, 6),
            'x_new': round(x_new, 6),
            'error': round(error, 6)
        })
        
        if abs(fx) < tol or error < tol:
            return {
                'iterations': iterations,
                'root': x_new,
                'finalError': error,
                'converged': True
            }
        
        x = x_new
    
    return {
        'iterations': iterations,
        'root': x,
        'finalError': error,
        'converged': False
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    method = data.get('method')
    equation = data.get('equation')
    tol = float(data.get('tolerance', 0.0001))
    max_iter = int(data.get('maxIterations', 50))
    
    try:
        if method == 'bisection':
            a = float(data.get('a'))
            b = float(data.get('b'))
            result = bisection_method(equation, a, b, tol, max_iter)
        
        elif method == 'regulaFalsi':
            a = float(data.get('a'))
            b = float(data.get('b'))
            result = regula_falsi_method(equation, a, b, tol, max_iter)
        
        elif method == 'secant':
            x0 = float(data.get('x0'))
            x1 = float(data.get('x1'))
            result = secant_method(equation, x0, x1, tol, max_iter)
        
        elif method == 'newtonRaphson':
            x0 = float(data.get('x0'))
            result = newton_raphson_method(equation, x0, tol, max_iter)
        
        elif method == 'fixedPoint':
            x0 = float(data.get('x0'))
            result = fixed_point_method(equation, x0, tol, max_iter)
        
        elif method == 'modifiedSecant':
            x0 = float(data.get('x0'))
            delta = float(data.get('delta', 0.01))
            result = modified_secant_method(equation, x0, delta, tol, max_iter)
        
        else:
            result = {'error': 'Invalid method'}
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

    