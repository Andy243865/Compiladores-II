import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from tkinter.filedialog import asksaveasfilename, askopenfilename
from PIL import Image, ImageTk
from prettytable import PrettyTable
from analisis_de_tokens import *
from sintactico import setup_syntax_analysis, sint_analyzer,semantic_analyzer
from semantico import mostrar_tabla_simbolos, hash_table, fn_reset
import re

# Funciones de menú
def open_file():
    global path
    path = askopenfilename(filetypes=[('Kodiak Files', '.kd'), ('Text Files', '.txt'), ('All Files', '.')])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', tk.END)
            editor.insert('1.0', code)

def save_as():
    path = asksaveasfilename(filetypes=[('Kodiak Files', '.kd'), ('Text Files', '.txt'), ('All Files', '.')])
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0', tk.END)
            file.write(code)

def save_file():
    global path
    if path:
        with open(path, 'w') as file:
            file.write(editor.get('1.0', tk.END))
    else:
        save_as()

# Funciones adicionales
def posicion_cursor(event=None):
    posicion = editor.index(tk.INSERT)
    row, col = map(int, posicion.split('.'))
    label_col.config(text=f"Columna: {col}")
    label_row.config(text=f"Fila: {row}")

def actualizar_numeros_linea(event=None):
    conte = editor.get("1.0", tk.END)
    num_lineas = conte.count('\n')

    numeros_linea.config(state=tk.NORMAL)
    numeros_linea.delete("1.0", tk.END)
    numeros_linea.insert(tk.END, '\n'.join(map(str, range(1, num_lineas + 1))))
    numeros_linea.config(state=tk.DISABLED)

    desplazamiento_y = editor.yview()[0]
    numeros_linea.yview_moveto(desplazamiento_y)

def highlight_words(text_widget, patterns):
    content = text_widget.get("1.0", tk.END)
    for tag, pattern, color in patterns:
        text_widget.tag_remove(tag, "1.0", tk.END)
        matches = re.finditer(pattern, content)
        for match in matches:
            start = match.start()
            end = match.end()
            text_widget.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")
            text_widget.tag_config(tag, foreground=color)

def highlight_words_callback(event=None):
    highlight_words(editor, patterns)
    posicion_cursor()

# Patrones de análisis léxico
patterns = [
    ('ERROR', r'.+', "red"),
    ('SYMBOL', r"[\[\];:,{}\(\)]", "green"),
    ('NUMBER', r'[+-]?\d+', "#FF8000"),
    ('REALNUMBER', r"[+-]?\d+\.\d+", "#FF8000"),
    ('OPERATOR', r'[+\-*/%^]', "purple"),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b', "#25D9C8"),
    ('KEYWORD', r'\b(int|for|string|if|else|do|while|switch|case|double|main|cout|cin|break)\b', "#e94CC5"),
    ('STRING', r'\"([^"]*)\"', "#BDA820"),
    ('COMMENT_SINGLE', r'//.*', "#7D4218"),
]

# Funciones de análisis léxico, sintáctico y semántico
def lexico():
    global lex_analy, tokens
    # Limpiar el archivo de errores y el widget de errores
    open("errores_de_ejecucion.txt", "w").close()
    text_errores.delete('1.0', tk.END)

    content = editor.get("1.0", tk.END)
    tokens = lex_analyzer(content)
    lex_analy = ""
    unknow_tokens = ""

    for token in tokens:
        if token[0] == 'DESCONOCIDO' or token[0] == 'DESCONOCI2' or token[0] == 'NO_NUMBER':
            unknow_tokens += str(token) + "\n"
        else:
            lex_analy += str(token) + "\n"

    label1.delete('1.0', tk.END)
    label1.insert('1.0', lex_analy)

    # Guardar errores en "errores.txt"
    with open("errores_de_ejecucion.txt", "w") as f:
        f.write(unknow_tokens)

    sintactico()
    fn_reset()
    semantico()

def sintactico():
    content = editor.get("1.0", tk.END)
    setup_syntax_analysis(tab_sintactico, content)
    setup_syntax_analysis(tab_semantico, content)  # Mostrar árbol también en "Semántico"

    # Leer errores y actualizar text_errores
    with open("errores_de_ejecucion.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        text_errores.delete('1.0', tk.END)
        text_errores.insert('1.0', contenido)

def semantico():
    data = hash_table()
    resultado = "Locación | Variable | Tipo | Valor | Líneas\n" + "-" * 50 + "\n" + data
    label_tabla_valores.delete('1.0', tk.END)
    label_tabla_valores.insert('1.0', resultado)

    # Leer errores y actualizar text_errores
    with open("errores_de_ejecucion.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        text_errores.delete('1.0', tk.END)
        text_errores.insert('1.0', contenido)

# Función para mostrar la tabla de valores
def mostrar_tabla_valores():
    tabla_simbolos = mostrar_tabla_simbolos()
    label_tabla_valores.delete('1.0', tk.END)
    label_tabla_valores.insert('1.0', tabla_simbolos)

# Función para mostrar código intermedio
def mostrar_codigo_intermedio():
    # Aquí deberías incluir el análisis que genera el código intermedio
    codigo_intermedio = "Código intermedio generado..."  # Sustituye con la lógica real
    label_codigo_intermedio.delete('1.0', tk.END)
    label_codigo_intermedio.insert('1.0', codigo_intermedio)

# Configuración principal de la ventana
root = tk.Tk()
root.title("Compilador R++")
root.geometry('1000x700')

# Menú principal
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir", command=open_file)
filemenu.add_command(label="Guardar", command=save_file)
filemenu.add_command(label="Guardar como", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

compilermenu = Menu(menubar, tearoff=0)
compilermenu.add_command(label="Compilar", command=lexico)
menubar.add_cascade(label="Compilar", menu=compilermenu)

root.config(menu=menubar)

# Frame principal
content = ttk.Frame(root)
content.pack(fill='both', expand=True)

# Editor de código
frame_editor = ttk.Frame(content)
frame_editor.pack(side='left', fill='both', expand=True, padx=5, pady=5)

numeros_linea = tk.Text(frame_editor, width=4, state=tk.DISABLED)
numeros_linea.pack(side='left', fill='y')

editor = scrolledtext.ScrolledText(frame_editor, wrap='none', undo=True)
editor.pack(fill='both', expand=True)
editor.config(font=("Courier New", 11), background="white", foreground="black")

# Vincular eventos
editor.bind("<KeyRelease>", highlight_words_callback)
editor.bind("<Button-1>", highlight_words_callback)
editor.bind("<MouseWheel>", actualizar_numeros_linea)
editor.bind("<Configure>", actualizar_numeros_linea)

# Sección de análisis a la derecha
frame_analysis = ttk.Frame(content)
frame_analysis.pack(side='right', fill='y', padx=5, pady=5)

tab_control = ttk.Notebook(frame_analysis)
tab_lexico = ttk.Frame(tab_control)
tab_sintactico = ttk.Frame(tab_control)
tab_semantico = ttk.Frame(tab_control)
tab_valores = ttk.Frame(tab_control)  # Pestaña para la tabla de valores
tab_intermedio = ttk.Frame(tab_control)  # Pestaña para el código intermedio

tab_control.add(tab_lexico, text='Léxico')
tab_control.add(tab_sintactico, text='Sintáctico')
tab_control.add(tab_semantico, text='Semántico')
tab_control.add(tab_valores, text='Tabla de Valores')  # Agregado
tab_control.add(tab_intermedio, text='Código Intermedio')  # Agregado
tab_control.pack(fill='both', expand=True)

# Resultados léxicos, sintácticos y semánticos
label1 = scrolledtext.ScrolledText(tab_lexico, wrap='word', height=10)
label1.pack(fill='both', expand=True)

label4 = ttk.Label(tab_semantico, justify='left', anchor='nw')
label4.pack(fill='both', expand=True)

# Área para la tabla de valores
label_tabla_valores = scrolledtext.ScrolledText(tab_valores, wrap='word', height=10)
label_tabla_valores.pack(fill='both', expand=True)

# Área para el código intermedio
label_codigo_intermedio = scrolledtext.ScrolledText(tab_intermedio, wrap='word', height=10)
label_codigo_intermedio.pack(fill='both', expand=True)

# Sección de errores
frame_output = ttk.Frame(root)
frame_output.pack(side='bottom', fill='x', padx=5, pady=5)

frame_output_sub = ttk.Notebook(frame_output)
tab_errores = ttk.Frame(frame_output_sub)
tab_resultados = ttk.Frame(frame_output_sub)

frame_output_sub.add(tab_errores, text='Errores')
frame_output_sub.add(tab_resultados, text='Resultados')
frame_output_sub.pack(fill='x', expand=True)

text_errores = scrolledtext.ScrolledText(tab_errores, height=5)
text_errores.pack(fill='x', expand=True)
text_resultados = scrolledtext.ScrolledText(tab_resultados, height=5)
text_resultados.pack(fill='x', expand=True)

# Etiquetas para fila y columna
label_row = ttk.Label(frame_output, text="Fila: 1")
label_row.pack(side='left', padx=5)

label_col = ttk.Label(frame_output, text="Columna: 1")
label_col.pack(side='left')

root.mainloop()
