import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sympy as sp

def polynomial_fit_custom_bases(x, y, bases):
    A = np.zeros((len(x), len(bases))) #define matriz A -> cada columna es el resultado de evaluar una base polinómica en x.
    for i, base in enumerate(bases):
        expr = sp.sympify(base)
        func = sp.lambdify(sp.symbols('x'), expr, 'numpy')
        A[:, i] = func(x)
    coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)  #Usa np... para resolver el sistema de ecuaciones y encontrar los coeficientes que minimizan el error cuadrático.
    return coeffs, A
def exponential_fit(x, y, form):
    if np.any(x == 0):
        raise ValueError("Los valores de x no deben ser cero para el ajuste exponencial con 'a*e^(b/x)'")

    if form == 'a*e^(b/x)':
        log_y = np.log(y)
        # Reemplaza valores cero en x con un valor muy pequeño
        x_safe = np.where(x == 0, 1e-10, x)
        A = np.vstack([1/x_safe, np.ones_like(x)]).T
        try:
            coeffs, _, _, _ = np.linalg.lstsq(A, log_y, rcond=None)
        except np.linalg.LinAlgError as e:
            raise RuntimeError(f"Error en la solución de la regresión lineal: {e}")
        a = np.exp(coeffs[1])
        b = coeffs[0]
        coeffs = [a, b]
    elif form == 'a*e^(a*x - b*x**2)':
        log_y = np.log(y)
        A = np.vstack([x, -x**2, np.ones_like(x)]).T
        try:
            coeffs, _, _, _ = np.linalg.lstsq(A, log_y, rcond=None)
        except np.linalg.LinAlgError as e:
            raise RuntimeError(f"Error en la solución de la regresión lineal: {e}")
    elif form == 'a*e^(b*x)':
        def model(x, a, b):
            return a * np.exp(b * x)
        try:
            coeffs, _ = curve_fit(model, x, y, p0=(1, 1))
        except Exception as e:
            raise RuntimeError(f"Error en el ajuste con curve_fit: {e}")
    else:
        raise ValueError("Forma exponencial no soportada. Use 'a*e^(b/x)', 'a*e^(a*x - b*x**2)', o 'a*e^(b*x)'.")
    
    return coeffs

def custom_fit(x, y, form): #
    if form == 'a*(x/(b+x))':
        def model(x, a, b):
            return a * (x / (b + x))
        popt, _ = curve_fit(model, x, y, p0=(1, 1))  # modelo a ajustar con curve_fit y valores iniciales de los parámetros
        return popt
    else:
        raise ValueError("Forma personalizada no soportada. Use 'a*(x/(b+x))'.")

def fit_and_plot(x, y, model='polinomica', bases=None, exp_form=None, custom_form=None): #Ajusta y grafica los datos segun el modelo especificado.
    if model == 'polinomica' and bases:
        coeffs, A = polynomial_fit_custom_bases(x, y, bases) #Ajusta los datos con los bases personalizados.
        y_fit = A @ coeffs  #Aplica los coeficientes a los datos y obtiene los valores ajustados.
        label = 'Arreglo de polinomios con bases personalizadas' #etiqueta del gráfico
        # Reemplazar en la función polinómica
        func_str = ' + '.join([f"{coeff:.5f} * x^{i}" for i, coeff in enumerate(coeffs)])
        print("Función ajustada:", func_str)

    elif model == 'exponencial' and exp_form:
        coeffs = exponential_fit(x, y, exp_form) 
        if exp_form == 'a*e^(b/x)':
            y_fit = coeffs[0] * np.exp(coeffs[1] / x) #Aplica el modelo exponencial a los datos y obtiene los valores ajustados.
            label = 'Arreglo exponencial: a*e^(b/x)'
        elif exp_form == 'a*e^(a*x - b*x**2)':
            y_fit = np.exp(coeffs[2]) * np.exp(coeffs[0] * x - coeffs[1] * x**2) #Aplica el modelo exponencial a los datos y obtiene los valores ajustados.
            label = 'Arreglo exponencial: a*e^(a*x - b*x**2)'
        elif exp_form == 'a*e^(b*x)':
            y_fit = coeffs[0] * np.exp(coeffs[1] * x)
            label = 'Arreglo exponencial: a*e^(b*x)'

    elif model == 'fraccion' and custom_form:
        if custom_form == 'a*(x/(b+x))':
            def model(x, a, b):
                return a * (x / (b + x))
            popt, _ = curve_fit(model, x, y, p0=(1, 1))  # Ajuste inicial de los parámetros
            coeffs = popt #Obtiene los coeficientes de la función ajustada.
            y_fit = model(x, *popt) #Aplica la función ajustada a los datos y obtiene los valores ajustados.
            label = 'Arreglo fraccionario: a*(x/(b+x))'

    else:
        raise ValueError("Modelo no especificado correctamente.")
    
    plt.scatter(x, y, color='red', label='Data Points')
    plt.plot(x, y_fit, label=label)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'{label}')
    plt.legend()
    plt.savefig('grafico.png')
    
    return coeffs, y_fit
    