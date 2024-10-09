import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import re
from prettytable import PrettyTable
from analisis_de_tokens import *
from sintactico import setup_syntax_analysis, sint_analyzer
from semantico import mostrar_tabla_simbolos, hash_table, fn_reset



#funciones
def posicion_cursor(self):
    posicion=editor.index(tk.INSERT)
    row, col =map(int, posicion.split('.'))
    label_col.config(text=f"Columna: {col}")
    label_row.config(text=f"Fila: {row}")


def actualizar_numeros_linea(self):
    conte=editor.get("1.0", tk.END)
    num_lineas=conte.count('\n')

    numeros_linea.config(state=tk.NORMAL)
    numeros_linea.delete("1.0",tk.END)
    numeros_linea.insert(tk.END, '\n'.join(map(str,range(1,num_lineas+1))))
    numeros_linea.config(state=tk.DISABLED)

    desplazamiento_y = editor.yview()[0]
    numeros_linea.yview_moveto(desplazamiento_y)
    




root = tk.Tk()
root.title("Kodiak")
root.iconbitmap("oso.ico")
#oso_path = resource_path("oso.ico")
#root.iconbitmap(oso_path)
root.resizable(False, False)

content = ttk.Frame(root, width=700, height=480)
frame_menu = ttk.Frame(content, width=700, height=20)
nombre = ttk.Frame(content, width=480, height=50)
frame = ttk.Frame(content, width=480, height=480, relief="ridge")
#frame1 = ttk.Frame(content, width=10, height=480, relief="ridge")
frame2 = ttk.Frame(content, width=200, height=480, relief="ridge")
frame_cont = ttk.Frame(content, width=480, height=50, relief="ridge")
frame3 = ttk.Frame(content, width=700, height=25, relief="ridge")

content.grid(column=0, row=0)
frame_menu.grid(column=0, row=0, columnspan=6, sticky=(tk.N,tk.W))
nombre.grid(column=0, row=1, columnspan=3, sticky=(tk.N,tk.W))
frame.grid(column=0, row=2, columnspan=3, rowspan=2, sticky=(tk.N,tk.S,tk.E,tk.W))
#frame1.grid(column=0, row=2, rowspan=2, sticky=(N,S,E,W))
frame2.grid(column=3, row=2, columnspan=3, sticky=(tk.N,tk.S,tk.E,tk.W))
frame_cont.grid(column=0, row=4, columnspan=3, sticky=(tk.N,tk.S,tk.E,tk.W))
frame3.grid(column=0, row=5, columnspan=6, rowspan=2, sticky=(tk.N,tk.W))

#editor = Text(frame)
#editor.pack()
editor = scrolledtext.ScrolledText(frame, wrap='none', undo=True, insertbackground="white",foreground="gray")
#editor.tag_add('colored','sel')
#editor.tag_configure("colored", foreground="red")
editor.pack(fill='both', expand=True, side=tk.RIGHT)
editor.config(font=("Courier New", 11),background="black")
# Crear una barra de desplazamiento horizontal
#scrollbar_horizontal = tk.Scrollbar(frame, orient='horizontal', command=editor.xview)
#scrollbar_horizontal.pack(fill='x')

# Configurar el área de texto para usar la barra de desplazamiento horizontal
#editor.config(xscrollcommand=scrollbar_horizontal.set)
"""
editor = tk.Text(frame, wrap="word", width=40, height=10)
editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
"""

path=''
nombre_archivo=''
nom_arch=''

#patrones definidos para el analisis lexico con los que se les dara color segun el tipo de token
patterns = [
    ('ERROR', r'.+',"red"),
    ('DESCONOCIDO',r'\..+',"red"),
    ('SYMBOL', r"[\[\];:,{}\(\)]", "green"),
    ('NUMBER', r'[+-]?\d+', "#FFFFFF"),
    ('NO_NUMBER',r"[+-]?\d+\.","red"),
    ('REALNUMBER',r"[+-]?\d+\.\d+", "#FFFFFF"),
    ('ASIGN_OPERATOR',r'=',"orange"),
    ('REL_OPERATOR',r'[<>!=][=]|[<>]',"#53f953"),
    ##Aqui
    ('OPERATOR', r'\+\+|--|[+\-*/%^]', "purple"),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b', "#25D9C8"),
    ("LOGIC_OPERATOR",r"and|or", "#FFFF00"),
    ('KEYWORD', r'\b(int|for|string|if|else|do|while|switch|case|double|main|cout|cin|break)\b', "#e94CC5"),
    ('STRING',r'\"([^"]*)\"', "#BDA820"),
    ('COMMENT_MULTI', r'/\*(.|\n)*?\*/', "#7D4218"),
    ('COMMENT_SINGLE', r'//.*', "#7D4218"),
    
]

numeros_linea = tk.Text(frame, width=4, height=10, bg="#f0f0f0", wrap="none", bd=2, relief=tk.FLAT, state=tk.DISABLED, font=("Courier New", 11))
numeros_linea.pack(side="left", fill="y")


editor.bind("<Motion>", actualizar_numeros_linea)
editor.bind("<Configure>", actualizar_numeros_linea)
editor.bind("<MouseWheel>", actualizar_numeros_linea)
editor.bind("<Return>", actualizar_numeros_linea)
editor.bind("<Enter>", actualizar_numeros_linea)
editor.bind("<FocusIn>", posicion_cursor)
editor.bind("<Button-1>", posicion_cursor)


lex_analy = ""
tokens=""

#funcion lexico
# Función léxico modificada
def lexico():
    global lex_analy
    global tokens
    unknow_tokens = ''
    lex_analy = ''
    
    # Obtiene el contenido del texto y llama a la función lex_analyzer
    content = editor.get("1.0", tk.END)
    tokens = lex_analyzer(content)
    
    # Se imprimen los tokens encontrados
    for token in tokens:
        # Si el token es un error, se guarda en la cadena de errores
        if token[0] == 'DESCONOCIDO' or token[0] == 'DESCONOCI2' or token[0] == 'NO_NUMBER':
            unknow_tokens += f'{token[0]}, {token[1]}\n'
        else:
            # Se guarda en los tokens coincidentes sin paréntesis ni comillas
            lex_analy += f'{token[0]}, {token[1]}\n'
    
    # Muestra los tokens en el widget correspondiente
    label1.delete('1.0', tk.END)
    label1.insert('1.0', lex_analy)
    
    # Guarda los tokens en el archivo correspondiente
    with open("Formato_lexico.txt", "w") as f:
        f.write(lex_analy)
    
    with open("errores_de_ejecucion.txt", "w") as f:
        f.write(unknow_tokens)

    sintactico()
    fn_reset()
    semantico()
    


def sintactico():
    content = editor.get("1.0", tk.END)
    setup_syntax_analysis(tab2, content)
    #sintaxis = sint_analyzer(content)
    with open("errores_de_ejecucion.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        lbl_err.delete('1.0', tk.END)
        lbl_err.insert('1.0', contenido)

def semantico():
    global label4  # Declarar la variable global
    
    # Obtener los datos de la tabla hash
    data = text = hash_table()
    
    # Formatear la información en forma de tabla
    resultado = "Locación | Variable | Tipo | Valor | Líneas\n"
    resultado += "-" * 50 + "\n"  # Línea de separación
    resultado += data
    
    
    # Actualizar el label4 con la información formateada
    label4.config(text=resultado)
    
    # Imprimir en la consola
    print(resultado)
    
    # Mostrar errores en el widget de errores
    with open("errores_de_ejecucion.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        lbl_err.delete('1.0', tk.END)
        lbl_err.insert('1.0', contenido)


def highlight_words(text_widget, patterns):
    posiciones=[]
    #se obtienen el contenido del texto 
    content = text_widget.get("1.0", tk.END)
    #se recorre patrones onteniendo el tipo de token su expresion y su color
    for tag, pattern,color in patterns:
        #se remueven las etiquetas anteriones
        text_widget.tag_remove(tag, "1.0", tk.END)
        #se buscan concurrencias entre las expresiones regulares y el texto del codigo
        
        matches = re.finditer(pattern, content)
        #se recorren las conncurencias
        for match in matches:
            posiciones.append((match.start(),match.end()))
            #se busca el inicio y final de cada concurrencias
            start = match.start()
            end = match.end()

            #en base al inicio y fin se crea una etiquetan con el nombre del tipo de token

            text_widget.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c", )
            #a esta etiqueta se le asigna el color del token
            text_widget.tag_config(tag,foreground=color)

#se llama a la funcion que cambiara el color de los tokens indicandole el editor donde se cambiara el color
#y los patrones a buscar
def highlight_words_callback(self):
    text_widget = editor
    highlight_words(text_widget, patterns)
    posicion_cursor(self)


# Vincular la función de resaltado de token con el evento de teclas
editor.bind("<KeyRelease>",highlight_words_callback) #
editor.bind("<Button-1>",highlight_words_callback) #


# Crear un widget de desplazamiento vertical
yscroll = tk.Scrollbar(frame, command=editor.yview)
yscroll.pack(side=tk.RIGHT, fill=tk.Y)

# Conectar el desplazamiento vertical al área de edición de código
editor['yscrollcommand'] = yscroll.set

label_row=tk.Label(frame_cont, text="Fila: 1")
label_col=tk.Label(frame_cont, text="Columna: 1")

label_row.pack()
label_col.pack()


def open_file():
    global path
    global nombre_archivo
    path=askopenfilename(filetypes=[('Compilador Files','*.cm')])
    #print(path)

    nom = path.split("/")
    #print(nom)
    j=0
    for i in nom:
        j+=1
    #print(nom[j-1])
    nombre_archivo = nom[j-1]

    with open(path,'r+') as file:
        code=file.read()
        editor.delete('1.0',tk.END)
        editor.insert('1.0',code)
    
    nombres()

def save_as():
    path=asksaveasfilename(filetypes=[('Compilador Files','*.cm')])
    with open(path, 'w') as file:
        code=editor.get('1.0',tk.END)
        file.write(code)

def save_file():
    global path
    #print(path)
    if path!='':
        with open(path, 'w') as file:
            file.write(editor.get('1.0',tk.END))
    else:
        save_as()

def nombres():
    global nom_arch
    nom_arch.destroy()
    nom_arch = ttk.Notebook(nombre)
    nom = ttk.Frame(nom_arch)
    if nombre_archivo!='':
        nom_arch.add(nom, text=nombre_archivo)
    else:
        nom_arch.add(nom, text="Sin titulo.cm")
    nom_arch.pack(fill=tk.BOTH, expand=True)

def seleccionar_opcion(opcion):
    opcion_seleccionada.set(opciones[0]) 
    if opcion == "Open":
        open_file()
    elif opcion == "Save":
        save_file()
    elif opcion == "Save As":
        save_as()
    elif opcion == "Exit":
        exit()
    elif opcion == "Close":
        close()


def close():
    editor.delete('1.0',tk.END)
    global nom_arch
    nom_arch.destroy()
    nom_arch = ttk.Notebook(nombre)
    nom = ttk.Frame(nom_arch)
    nom_arch.add(nom, text="Sin titulo.com")
    nom_arch.pack(fill=tk.BOTH, expand=True)


nom_arch = ttk.Notebook(nombre)
nom = ttk.Frame(nom_arch)
if nombre_archivo!='':
    nom_arch.add(nom, text=nombre_archivo+".cm")
else:
    nom_arch.add(nom, text="Sin titulo.cm")
nom_arch.pack(fill=tk.BOTH, expand=True)

analisis = ttk.Notebook(frame2, width=200)

tab1 = ttk.Frame(analisis,width=200)
analisis.add(tab1, text="Léxico")
label1 = scrolledtext.ScrolledText(tab1, wrap="word",width=200)
label1.pack(padx=10, pady=10)

tab2 = ttk.Frame(analisis,width=200)
analisis.add(tab2, text="Sintáctico")
#label2 = ttk.Label(tab2, text="Análisis Sintáctico...")
#label2.pack(padx=10, pady=10)

tab3 = ttk.Frame(analisis,width=200)
analisis.add(tab3, text="Semántico")
label3 = ttk.Label(tab3, text="Análisis Semántico...")
label3.pack(padx=10, pady=10)

tab4 = ttk.Frame(analisis,width=200)
analisis.add(tab4, text="Tabla de Símbolos")
label4 = ttk.Label(tab4, text="Tabla de Símbolos...", justify='left', anchor='nw', wraplength=300)
label4.pack(padx=10, pady=10)

tab5 = ttk.Frame(analisis,width=200)
analisis.add(tab5, text="Código Intermedio")
label5 = ttk.Label(tab5, text="Código Intermedio...")
label5.pack(padx=10, pady=10)

analisis.pack(fill=tk.BOTH, expand=True)

inferior = ttk.Notebook(frame3, width=900, height=100)
resultado = ttk.Frame(inferior,width=900)
inferior.add(resultado, text="Resultado")
lbl_res = ttk.Label(resultado, text="Resultados...")
lbl_res.pack(padx=10, pady=10)
errores = ttk.Frame(inferior,width=900)
inferior.add(errores, text="Errores")
lbl_err = scrolledtext.ScrolledText(errores, wrap="word",height=100)
lbl_err.pack(padx=10, pady=10)
inferior.pack(fill=tk.BOTH, expand=True)






menu1 = tk.Frame(frame_menu, width=50, height=20)
menu2 = tk.Frame(frame_menu, width=50, height=20)
menu3 = tk.Frame(frame_menu, width=50, height=20)
menu4 = tk.Frame(frame_menu, width=50, height=20)
menu5 = tk.Frame(frame_menu, width=50, height=20)
menu1.grid(column=0, row=0, sticky=(tk.N,tk.W))
menu2.grid(column=1, row=0, sticky=(tk.N,tk.W))
menu3.grid(column=2, row=0, sticky=(tk.N,tk.W))
menu4.grid(column=3, row=0, sticky=(tk.N,tk.W))
menu5.grid(column=4, row=0, sticky=(tk.N,tk.W))

opciones = ["File", "Open", "Save", "Save As", "Close", "Exit"]
opcion_seleccionada = tk.StringVar(menu1)
opcion_seleccionada.set(opciones[0])  # Establecer la opción por defecto

# Crear el menú desplegable
menu_desplegable = tk.OptionMenu(menu1, opcion_seleccionada, *opciones)
menu_desplegable.pack()

opcion_seleccionada.trace("w", lambda *args: seleccionar_opcion(opcion_seleccionada.get()))

pixel = tk.PhotoImage(width=1, height=1)
btn_run = tk.Button(menu2, text='Run',height=20, width=22, image=pixel, compound="c")
btn_run.pack()
#save_path = resource_path("save.png")
img_save = ImageTk.PhotoImage(Image.open("save.png").resize((22, 22)))
#img_save = PhotoImage(save_path)
btn_save = tk.Button(menu3, image=img_save, command=save_file)
btn_save.pack()
#open_path = resource_path("open.png")
img_open = ImageTk.PhotoImage(Image.open("open.png").resize((22, 22)))
#img_open = PhotoImage(open_path)
btn_open = tk.Button(menu4, image=img_open, command=open_file)
btn_open.pack()
img_lex = ImageTk.PhotoImage(Image.open("lex.png").resize((22, 22)))
#img_open = PhotoImage(open_path)
btn_lex = tk.Button(menu5, image=img_lex, command=lexico)
btn_lex.pack()

root.mainloop()