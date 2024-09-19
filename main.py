from aprox_discreta import *  # Importa todas las clases y funciones del archivo aprox_discreta
from colorama import Fore, Style, init  # Importa Fore, Style e init de la biblioteca colorama
import numpy as np  # Asegúrate de importar numpy si no está ya en aprox_discreta

init(autoreset=True)  # Inicializa colorama y reestablece automáticamente los colores después de cada print

def show_exponential_menu():
    while True:
        print(Fore.BLUE + "\nIngrese el tipo de ajuste exponencial que desea realizar")
        print(Fore.GREEN + "1. Ajuste exponencial simple -> a*e^(b*x)")
        print(Fore.GREEN + "2. Ajuste exponencial cuadrático -> a*e^(a*x - b*x**2)")
        print(Fore.GREEN + "3. Ajuste exponencial con exponente inverso -> a*e^(b/x)")
        print(Fore.GREEN + "4. Volver al menú principal")  # Opción para regresar al menú principal

        exp_option = input(Fore.CYAN + "Seleccione una opción (1-4): ").strip()
        
        if exp_option == '4':
            break  # Salir del loop del menú de ajustes exponenciales y regresar al menú principal

        if exp_option not in ['1', '2', '3']:
            print(Fore.RED + "Opción no válida. Por favor, elija una opción del menú.")
            continue

        form_map = {
            '1': 'a*e^(b*x)',
            '2': 'a*e^(a*x - b*x**2)',
            '3': 'a*e^(b/x)'
        }

        form = form_map[exp_option]
        
        coeffs, y_fit = fit_and_plot(x, y, model='exponencial', exp_form=form)
        print(Fore.MAGENTA + 'Coeficientes del ajuste exponencial:')
        print(Fore.CYAN + str(coeffs))

        if form == 'a*e^(b*x)':
            print(Fore.RED + "Función: ")
            print(Fore.YELLOW + f"y = {coeffs[0]:.5f} * e^({coeffs[1]:.5f} * x)")

        elif form == 'a*e^(a*x - b*x**2)':
            print(Fore.RED + "Función: ")
            print(Fore.YELLOW + f"y = {np.exp(coeffs[2]):.5f} * e^({coeffs[0]:.5f} * x - {coeffs[1]:.5f} * x^2)")

        elif form == 'a*e^(b/x)':
            print(Fore.RED + "Función ajustada:")
            print(Fore.YELLOW + f"y = {coeffs[0]:.5f} * e^({coeffs[1]:.5f} / x)")

def main():
    global x, y  # Define x and y as global variables to be accessible in show_exponential_menu

    while True:
        print(Fore.BLUE + "\nIngrese el tipo de modelo que desea ajustar")
        print(Fore.GREEN + "1. Ajuste polinómico")
        print(Fore.GREEN + "2. Ajuste exponencial")
        print(Fore.GREEN + "3. Ajuste fraccionario")
        print(Fore.GREEN + "4. Salir")

        opcion = input(Fore.CYAN + "Seleccione una opción (1-4): ").strip()

        if opcion == '4':
            print(Fore.GREEN + "Gracias por usar el programa. ¡Adiós!")
            break

        if opcion not in ['1', '2', '3']:
            print(Fore.RED + "Opción no válida. Por favor, elija una opción del menú.")
            continue

        if opcion == '1':
            x = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de x separados por comas: ").split(','))))
            y = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de y separados por comas: ").split(','))))
            bases = input(Fore.YELLOW + "Ingrese las bases polinómicas separadas por comas: ").split(',')
            coeffs, y_fit = fit_and_plot(x, y, model='polinomica', bases=bases)
            print(Fore.MAGENTA + 'Coeficientes del ajuste polinómico con bases ingresadas:')
            print(Fore.CYAN + str(coeffs))
            polynomial_expr = ' + '.join([f'{coeff:.5f}*{base.strip()}' for coeff, base in zip(coeffs, bases)])
            print(Fore.MAGENTA + f'Función polinómica ajustada: y = {polynomial_expr}')
        
        elif opcion == '2':
            x = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de x separados por comas: ").split(','))))
            y = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de y separados por comas: ").split(','))))
            show_exponential_menu()  # Llama al menú de ajustes exponenciales

        elif opcion == '3':
            x = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de x separados por comas: ").split(','))))
            y = np.array(list(map(float, input(Fore.YELLOW + "Ingrese los valores de y separados por comas: ").split(','))))
            custom_form = input(Fore.YELLOW + "Ingrese la forma personalizada ('a*(x/(b+x))'): ").strip().lower()
            coeffs, y_fit = fit_and_plot(x, y, model='fraccion', custom_form=custom_form)
            print(Fore.MAGENTA + 'Coeficientes del ajuste: ')
            print(Fore.CYAN + str(coeffs))
            print(Fore.RED + "Función: ")  
            print(Fore.YELLOW + f"y = {coeffs[0]:.5f} * (x / ({coeffs[1]:.5f} + x))")

if __name__ == "__main__":
    main()
