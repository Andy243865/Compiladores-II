def traducir_a_tiny(archivo_codigo_p="codigo_P.txt", archivo_codigo_tiny="codigo_tiny.txt"):
    """
    Traduce instrucciones de código P a instrucciones Tiny y las guarda en un archivo.
    :param archivo_codigo_p: Archivo con las instrucciones de código P.
    :param archivo_codigo_tiny: Archivo de salida con las instrucciones Tiny.
    """
    # Mapeo de instrucciones P a Tiny
    traducciones = {
        "lda": "LD",  # Load address
        "lod": "LD",  # Load variable
        "sta": "ST",  # Store variable
        "ldc": "LDI",  # Load constant
        "adi": "ADD",  # Addition
        "sbi": "SUB",  # Subtraction
        "mpi": "MUL",  # Multiplication
        "dvi": "DIV",  # Division
        "mod": "MOD",  # Modulus
        "les": "LT",   # Less than
        "leq": "LE",   # Less or equal
        "grt": "GT",   # Greater than
        "geq": "GE",   # Greater or equal
        "equ": "EQ",   # Equal
        "neq": "NE",   # Not equal
        "and": "AND",  # Logical AND
        "or": "OR",    # Logical OR
        "not": "NOT",  # Logical NOT
        "rdi": "IN",   # Input
        "wri": "OUT",  # Output
        "lab": "LABEL",# Label
        "fjp": "JZ",   # Jump if false
        "ujp": "JMP",  # Unconditional jump
        "stp": "HALT", # Stop execution
    }

    # Leer instrucciones del archivo de código P
    with open(archivo_codigo_p, "r") as archivo:
        instrucciones_p = archivo.readlines()

    # Traducir instrucciones
    instrucciones_tiny = []
    for linea in instrucciones_p:
        partes = linea.strip().split()
        if not partes:
            continue  # Saltar líneas vacías

        instruccion_p = partes[0]
        argumentos = partes[1:] if len(partes) > 1 else []

        # Traducir instrucción
        if instruccion_p in traducciones:
            instruccion_tiny = traducciones[instruccion_p]
            instruccion_traducida = f"{instruccion_tiny} {' '.join(argumentos)}"
            instrucciones_tiny.append(instruccion_traducida)
        else:
            raise ValueError(f"Instrucción desconocida en código P: {instruccion_p}")

    # Guardar las instrucciones traducidas en el archivo de código Tiny
    with open(archivo_codigo_tiny, "w") as archivo_salida:
        archivo_salida.write("\n".join(instrucciones_tiny) + "\n")

    # Devolver el conjunto de instrucciones traducidas
    return instrucciones_tiny


# Ejecución de ejemplo
if __name__ == "__main__":
    instrucciones_tiny = traducir_a_tiny()
    print("Traducción completada. Instrucciones Tiny:")
    print("\n".join(instrucciones_tiny))
