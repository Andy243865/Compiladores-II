from prettytable import PrettyTable
# Tabla de símbolos inicial (vacía)
tabla_simbolos = {}
tabla_errores=[]

loc=1



def fn_check_tipo(tipo, valor):
    print("tipo: ", tipo,"valor: ", valor)
    if((tipo=='int' and (isinstance(valor,float) or isinstance(valor,str))) or
       (tipo=='double' and (isinstance(valor,str))) or
       (tipo=='str' and (isinstance(valor,float) or isinstance(valor,int)))
       ):
        return True
    else:
        return False

    
resultado = ""

def mostrar_tabla_simbolos():
    global resultado
    resultado = ""
    
    # Crear la tabla
    tabla = PrettyTable()
    tabla.field_names = ["Locacion", "Variable", "Tipo", "Valor", "Líneas"]

    if not tabla_errores:
        for var, info in tabla_simbolos.items():
            # Agregar filas a la tabla
            tabla.add_row([info['locacion'], var, info['tipo'], info['valor'], info['lineas']])
            resultado += f"{info['locacion']} | {var}, {info['tipo']} | {info['valor']} | {info['lineas']}\n"
        print(tabla)  # Imprimir la tabla en la consola
    else:
        for error in tabla_errores:
            with open("errores_de_ejecucion.txt", "a", encoding="utf-8") as f:
                f.write(f"{error}\n")
            print(error, '\n')
    return tabla

def hash_table():
    global resultado
    return resultado

def insertar_variable(nombre, tipo, valor, linea, tipo_accion):
    global loc
    # Si es una declaración
    if tipo_accion == "dec":
        if nombre in tabla_simbolos:
            tabla_errores.append(f"Error: La variable '{nombre}' ya ha sido declarada.")
            print(f"Error: La variable '{nombre}' ya ha sido declarada.")
            return 0 # Salir si la variable ya existe
        else:
            # Si la variable no existe, se inserta una nueva entrada en la tabla de símbolos
            tabla_simbolos[nombre] = {
                'locacion': loc,
                'tipo': tipo,
                'valor': valor,
                'lineas': linea
            }
            print(f"Variable '{nombre}' agregada a la tabla de símbolos.")
            loc+=1

    # Si es una asignación
    elif tipo_accion == "asi":
        if nombre not in tabla_simbolos:
            print(f"Error: La variable '{nombre}' no ha sido declarada.")
            tabla_errores.append(f"Error: La variable '{nombre}' no ha sido declarada.")
            return  # Salir si la variable no existe

        variable = tabla_simbolos[nombre]

        if valor == None:
            tabla_errores.append(f"Error: Tipo de dato incompatible para la variable '{nombre}'. Esperado: {variable['tipo']}, recibido: {valor}.")
            return

        valor_aux=variable['valor']
        variable['valor'] = valor
        
        if  fn_check_tipo(variable['tipo'],variable['valor']):
            variable['valor'] = valor_aux
            tipo_aux = str(type(valor))

            if isinstance(valor, int):
                tipo_aux = 'int'
            elif isinstance(valor,float) or isinstance(valor, int):
                tipo_aux = 'double'
            elif isinstance(valor,str):
                tipo_aux = 'string'
            else:
                tipo_aux = 'unkwown'
            
            tabla_errores.append(f"Error: Tipo de dato incompatible para la variable '{nombre}'. Esperado: {variable['tipo']}, recibido: {tipo_aux}.")
            return

        # Actualizar el valor de la variable y agregar la línea donde aparece
        
       


def fn_getValor(nombre):
    print(nombre)
    if nombre in tabla_simbolos:
        #print("----------------->",tabla_simbolos[nombre],"<-----------------")
        return tabla_simbolos[nombre]

def fn_reset():
    global tabla_errores, tabla_simbolos, loc
    loc=1
    tabla_errores=[]
    tabla_simbolos={}
