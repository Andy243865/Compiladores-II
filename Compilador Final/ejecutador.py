import math
from tkinter.simpledialog import askinteger

def ejecutar_tiny(archivo_tiny):
    """
    Intérprete para el lenguaje Tiny.
    Ejecuta las instrucciones contenidas en un archivo.

    :param archivo_tiny: Ruta del archivo que contiene las instrucciones de Tiny.
    """
    memoria = {}  # Diccionario para almacenar valores de variables
    pila = []  # Simulación de la pila
    etiquetas = {}  # Mapeo de etiquetas a posiciones
    pc = 0  # Contador de programa (índice de instrucciones)

    # Leer las instrucciones del archivo
    with open(archivo_tiny, "r") as archivo:
        instrucciones = [line.strip() for line in archivo if line.strip()]

    # Parsear etiquetas antes de la ejecución
    for i, instruccion in enumerate(instrucciones):
        if instruccion.startswith("LABEL"):
            etiqueta = instruccion.split()[1]
            etiquetas[etiqueta] = i

    # Ejecutar las instrucciones
    while pc < len(instrucciones):
        partes = instrucciones[pc].split()
        comando = partes[0]
        args = partes[1:] if len(partes) > 1 else []

        try:
            if comando == "LD":  # Cargar valor de una variable
                pila.append(memoria.get(args[0], 0))
            elif comando == "LDI":  # Cargar constante
                pila.append(int(args[0]))
            elif comando == "IN":  # Leer entrada
                entrada = askinteger("Entrada requerida", f"Ingrese un valor para {args[0]}:")
                if entrada is not None:
                    memoria[args[0]] = entrada
                else:
                    print(f"Entrada cancelada para {args[0]}")
            elif comando == "ST":  # Almacenar valor en una variable
                memoria[args[0]] = pila.pop()
            elif comando == "OUT":  # Imprimir salida
                resultado = pila.pop()
                tipo = "float" if isinstance(resultado, float) else "decimal" if isinstance(resultado, int) else "desconocido"
                print(f"Salida: {resultado} (Tipo: {tipo})")
            elif comando == "ADD":  # Sumar
                b = pila.pop()
                a = pila.pop()
                resultado = a + b
                pila.append(resultado)
                print(f"ADD Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
            elif comando == "SUB":  # Restar
                b = pila.pop()
                a = pila.pop()
                resultado = a - b
                pila.append(resultado)
                print(f"SUB Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
            elif comando == "MUL":  # Multiplicar
                b = pila.pop()
                a = pila.pop()
                resultado = a * b
                pila.append(resultado)
                print(f"MUL Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
            elif comando == "DIV":  # Dividir
                b = pila.pop()
                a = pila.pop()
                if b != 0:
                    resultado = a / b
                    pila.append(resultado)
                    print(f"DIV Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
                else:
                    print("Error: División por cero.")
                    pila.append(0)
            elif comando == "MOD":  # Módulo
                b = pila.pop()
                a = pila.pop()
                resultado = a % b
                pila.append(resultado)
                print(f"MOD Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
            elif comando == "POW":  # Potencia
                b = pila.pop()
                a = pila.pop()
                resultado = a ** b
                pila.append(resultado)
                print(f"POW Resultado: {resultado} (Tipo: {'float' if isinstance(resultado, float) else 'decimal'})")
            elif comando in {"LT", "LE", "GT", "GE", "EQ", "NE"}:  # Operadores relacionales
                b = pila.pop()
                a = pila.pop()
                resultado = {
                    "LT": a < b,
                    "LE": a <= b,
                    "GT": a > b,
                    "GE": a >= b,
                    "EQ": a == b,
                    "NE": a != b
                }[comando]
                pila.append(1 if resultado else 0)
            elif comando in {"AND", "OR"}:  # Operadores booleanos
                b = pila.pop()
                a = pila.pop()
                resultado = {
                    "AND": a and b,
                    "OR": a or b
                }[comando]
                pila.append(1 if resultado else 0)
            elif comando == "NOT":  # Negación lógica
                a = pila.pop()
                pila.append(1 if not a else 0)
            elif comando == "JZ":  # Saltar si el tope de la pila es 0
                if pila.pop() == 0:
                    pc = etiquetas[args[0]] - 1
            elif comando == "JMP":  # Salto incondicional
                pc = etiquetas[args[0]] - 1
            elif comando == "LABEL":  # Etiqueta (ya procesada)
                pass
            elif comando == "HALT":  # Detener ejecución
                break
            else:
                print(f"Instrucción desconocida: {comando}")
        except Exception as e:
            print(f"Error al ejecutar la instrucción '{comando}': {e}")

        pc += 1

# Llamada al intérprete
if __name__ == "__main__":
    archivo = "codigo_tiny.txt"  # Ruta del archivo de Tiny
    ejecutar_tiny(archivo)