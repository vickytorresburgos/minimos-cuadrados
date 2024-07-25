# Aproximación discreta por mínimos cuadrados

## María Victoria Torres Burgos - Análisis Numérico - Universidad de Mendoza - 3° 2024

Este programa permite ajustar diferentes tipos de modelos matemáticos a conjuntos de datos. Ofrece soporte para ajuste polinómico, exponencial y fraccionario. Utiliza la biblioteca numpy para cálculos numéricos y colorama para una interfaz de usuario colorida en la terminal.

Características
- Ajuste Polinómico: Permite ajustar modelos polinómicos con bases personalizadas.
- Ajuste Exponencial: Ofrece varios tipos de ajustes exponenciales:
    - Exponencial simple: a * e^(b * x)
    - Exponencial cuadrático: a * e^(a * x - b * x^2)
    - Exponencial con exponente inverso: a * e^(b / x)
- Ajuste Fraccionario: Ajusta modelos fraccionarios personalizados como a * (x / (b + x)).

## Requisitos

Para poder ejecutar el programa, se debe instalar las librerías necesarias:
- scipy==1.13.1
- matplotlib==3.6.2
- sympy==1.12.1
- colorama==0.4.6

las cuales se pueden instalar con el comando:
$ pip3 install -r requirements.txt

Para ejecutar el programa, se debe ejecutar el archivo main.py con el comando:
$ python3 main.py

El programa se ejecutará en la consola y se mostrará la salida en la consola.