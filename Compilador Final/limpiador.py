def clean_comments(input_file, output_file):
    """
    Lee un archivo línea por línea, elimina todo después del símbolo '#' en cada línea,
    y guarda el resultado en un nuevo archivo.

    :param input_file: Nombre del archivo de entrada.
    :param output_file: Nombre del archivo de salida.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Divide la línea en partes antes y después de '#'
                clean_line = line.split('#')[0].strip()
                if clean_line:  # Si hay contenido antes de '#'
                    outfile.write(clean_line + '\n')
        print(f"Archivo procesado y guardado en {output_file}.")
    except FileNotFoundError:
        print(f"El archivo {input_file} no existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Uso de la función
# clean_comments('codigo_intermedio.txt', 'codigo_P.txt')
