import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, filedialog
from lexer import lexer
from parser import parser,symbol_table
from lexer import symbol_table
from hashing import update_variable_hash
from hashing import hash_table

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador R++")
        self.geometry("1000x600")
        self.file_path = None  # To track the current file path
        
        # Create a menu bar
        menubar = Menu(self)
        self.config(menu=menubar)

        # Create menu items
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar ", menu=edit_menu)
        edit_menu.add_command(label="Deshacer", command=self.undo)
        edit_menu.add_command(label="Rehacer", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cortar", command=self.cut)
        edit_menu.add_command(label="Copiar", command=self.copy)
        edit_menu.add_command(label="Pegar", command=self.paste)

        compile_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Compilar", menu=compile_menu)
        compile_menu.add_command(label="Compilar", command=self.run_analysis)

        # Layout
        self.frame_code = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.frame_code.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label_code = tk.Label(self.frame_code, text="Código a compilar")
        self.label_code.pack(anchor='nw')

        self.source_code = scrolledtext.ScrolledText(self.frame_code, width=60, height=20)
        self.source_code.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.source_code.bind("<KeyRelease>", self.on_key_release)
        
        self.notebook = ttk.Notebook(self.frame_code)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_lexico = scrolledtext.ScrolledText(self.notebook)
        self.tab_sintactico = scrolledtext.ScrolledText(self.notebook)
        self.tab_semantico = scrolledtext.ScrolledText(self.notebook)

        # Tab para el código intermedio con un Treeview
        self.frame_codigo_intermedio = tk.Frame(self.notebook)
        self.tree_codigo_intermedio = ttk.Treeview(self.frame_codigo_intermedio)
        self.tree_codigo_intermedio.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(self.tab_lexico, text="Lexico")
        self.notebook.add(self.tab_sintactico, text="Sintactico")
        self.notebook.add(self.tab_semantico, text="Semantico")
        self.notebook.add(self.frame_codigo_intermedio, text="Codigo Intermedio")
        
        self.frame_errors = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.frame_errors.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.notebook_errors = ttk.Notebook(self.frame_errors)
        self.notebook_errors.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_errors = scrolledtext.ScrolledText(self.notebook_errors)
        self.tab_results = scrolledtext.ScrolledText(self.notebook_errors)

        self.notebook_errors.add(self.tab_errors, text="Errores")
        self.notebook_errors.add(self.tab_results, text="Resultados")
    

    
    def new_file(self):
        self.source_code.delete('1.0', tk.END)
        self.file_path = None
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.source_code.delete('1.0', tk.END)
                self.source_code.insert(tk.END, content)
            self.file_path = file_path
    
    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                content = self.source_code.get('1.0', tk.END)
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as file:
                content = self.source_code.get('1.0', tk.END)
                file.write(content)
            self.file_path = file_path

    def undo(self):
        self.source_code.edit_undo()

    def redo(self):
        self.source_code.edit_redo()

    def cut(self):
        self.source_code.event_generate("<<Cut>>")

    def copy(self):
        self.source_code.event_generate("<<Copy>>")

    def paste(self):
        self.source_code.event_generate("<<Paste>>")
    
    def on_key_release(self, event):
        self.perform_lexical_analysis()
        self.perform_syntax_analysis()
    
    def run_analysis(self):
        self.perform_lexical_analysis()
        self.perform_syntax_analysis()
    
    def perform_lexical_analysis(self):
        # Clear previous results
        self.tab_lexico.delete('1.0', tk.END)
        self.source_code.tag_remove("blue", '1.0', tk.END)
        self.source_code.tag_remove("yellow", '1.0', tk.END)
        
        # Get the source code from the text widget
        source_code = self.source_code.get('1.0', tk.END)
        
        # Lexical analysis
        lexer.input(source_code)
        for token in lexer:
            self.tab_lexico.insert(tk.END, f'{token.type}: {token.value}\n')
            
            # Pintar tokens
            try:
                # Calcular la posición del token en el texto
                # Nota: Este método es aproximado y puede requerir ajustes
                try:
                    index = self.source_code.search(str(token.value), '1.0', tk.END)
                except Exception as e:
                    print(f"Error searching for token: {e}")

                if index:
                    end_index = f"{index}+{len(str(token.value))}c"
                    if token.type in ['INT', 'FLOAT', 'BOOL', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FI', 'WRITE', 'AND', 'OR', 'UNTIL']:
                        self.source_code.tag_add("blue", index, end_index)
                        self.source_code.tag_config("blue", foreground="blue")
                    elif token.type in ['NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE']:
                        self.source_code.tag_add("yellow", index, end_index)
                        self.source_code.tag_config("yellow", foreground="orange")
            except tk.TclError:
                pass  # Ignorar errores de búsqueda de índices

    def perform_syntax_analysis(self):
        # Clear previous error results
        self.tab_sintactico.delete('1.0', tk.END)
        self.tab_errors.delete('1.0', tk.END)
        self.tab_results.delete('1.0', tk.END)
        self.clear_tree(self.tree_codigo_intermedio)  # Clear previous tree
        
        # Get the source code from the text widget
        source_code = self.source_code.get('1.0', tk.END)
        
        # Syntax analysis
        global errors
        errors = []
        result = parser.parse(source_code)
        if errors:
            for line, error_msg in errors:
                self.tab_errors.insert(tk.END, f'Line {line}: {error_msg}\n')
            self.tab_sintactico.insert(tk.END, 'Syntax analysis completed with errors.\n')
        else:
            self.tab_sintactico.insert(tk.END, 'Syntax analysis completed without errors.\n')
            self.display_syntax_tree(result)
            #   Imprimir la tabla de símbolos en la pestaña semántica
            self.print_symbol_table()

    
    
    def print_symbol_table(self):
        """Imprime la tabla de símbolos y la tabla de hashes en la pestaña semántica."""
        self.tab_semantico.delete('1.0', tk.END)  # Limpiar contenido anterior
        self.tab_semantico.insert(tk.END, "Tabla de Símbolos:\n")
        self.tab_semantico.insert(tk.END, f"{'Variable':<20}{'Tipo':<15}{'Posición en Memoria':<20}{'Valor':<10}\n")
        self.tab_semantico.insert(tk.END, "-" * 65 + "\n")

        # Imprimir la tabla de símbolos
        for var_name, var_info in symbol_table.items():
            var_type = var_info.get('type', 'undefined')  # Tipo de variable
            position = id(var_info)  # Posición en memoria
            value = var_info.get('value', 'undefined')  # Valor de la variable

            # Imprimir la entrada en la tabla de símbolos
            self.tab_semantico.insert(tk.END, f"{var_name:<20}{var_type:<15}{position:<20}{value:<10}\n")

            # Actualizar el hash cuando se hace una asignación
            update_variable_hash(var_name, value)

        # Agregar una línea divisoria entre tablas
        self.tab_semantico.insert(tk.END, "\n" + "-" * 65 + "\n")
    
        # Imprimir la tabla de hashes debajo
        self.tab_semantico.insert(tk.END, "Tabla de Hashes (SHA-256) de las Variables:\n")
        self.tab_semantico.insert(tk.END, f"{'Variable':<20}{'Valor':<10}{'Hash (SHA-256)':<64}\n")
        self.tab_semantico.insert(tk.END, "-" * 95 + "\n")
    
        # Imprimir los hashes actuales
        for var_name, values in hash_table.items():
            for entry in values:
                self.tab_semantico.insert(tk.END, f"{var_name:<20}{entry['value']:<10}{entry['hash']:<64}\n")


    def clear_tree(self, tree):
        """Helper function to clear all items from a Treeview."""
        for item in tree.get_children():
            tree.delete(item)
    

    def display_syntax_tree(self, tree):
        """Display the syntax tree in the Treeview."""
        def add_node_to_tree(node, parent=''):
            tree_id = self.tree_codigo_intermedio.insert(parent, 'end', text=node.name)
            for child in node.children:
                add_node_to_tree(child, tree_id)

        if tree:
            add_node_to_tree(tree)
