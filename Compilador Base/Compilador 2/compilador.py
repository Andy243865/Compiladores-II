import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, filedialog
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree

# Define the lexer
tokens = [
    'MAIN', 'INT', 'FLOAT', 'BOOL', 'IDENTIFIER', 'NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON', 'COMMENT', 'MULTILINE_COMMENT', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO',
    'FI', 'WRITE', 'AND', 'OR', 'EQUALS', 'NOTEQUALS', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL',
    'UNTIL', 'STRING'
]

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATER = r'>'
t_GREATEREQUAL = r'>='

# Token para cadenas
t_STRING = r'\"([^\\\n]|(\\.))*?\"'


# Ignored characters
t_ignore = ' \t'

# Symbol table
symbol_table = {}

def t_MAIN(t):
    r'main'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_BOOL(t):
    r'bool'
    return t

def t_BOOL_VALUE(t):
    r'true|false'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_UNTIL(t):
    r'until'
    return t

def t_FI(t):
    r'fi'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_MULTILINE_COMMENT(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    global errors
    error_msg = f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}"
    errors.append((t.lexer.lineno, error_msg))
    print(error_msg)
    t.lexer.skip(1)

lexer = lex.lex()

# Define the parser
def p_main(p):
    'main : MAIN LBRACE declarations statements RBRACE'
    p[0] = Node('main', children=[p[3], p[4]])

def p_declarations(p):
    '''declarations : declarations declaration
                    | empty'''
    if len(p) == 3:
        print(p[1].children)
        p[0] = Node('declarations', children=[p[1], p[2]])
    else:
        p[0] = Node('declarations')

def p_declaration(p):
    '''declaration : INT var_list SEMICOLON
                   | FLOAT var_list SEMICOLON
                   | BOOL var_list SEMICOLON'''  # Añadido BOOL para variables booleanas
    p[0] = Node('declaration', children=[Node(p[1]), p[2]])

def p_var_list(p):
    '''var_list : var_list COMMA IDENTIFIER
                | IDENTIFIER'''
    if len(p) == 4:
        p[0] = Node('var_list', children=[p[1], Node(p[3])])
    else:
        p[0] = Node('var_list', children=[Node(p[1])])

def p_do_until_statement(p):
    '''do_until_statement : DO LBRACE statements RBRACE UNTIL LPAREN condition RPAREN SEMICOLON'''
    # Aquí puedes agregar una validación de errores si lo deseas.
    p[0] = Node('do_until_statement', children=[p[3], p[7]])

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    if len(p) == 3:
        p[0] = Node('statements', children=[p[1], p[2]])
    else:
        p[0] = Node('statements')

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | write_statement
                 | do_statement
                 | while_statement
                 | do_until_statement'''  # Nueva opción
    p[0] = p[1]

def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression SEMICOLON'
    if p[1] not in symbol_table:
        print(f"Error: Variable '{p[1]}' no declarada.")
    elif (symbol_table[p[1]] == 'int' and not p[3].isdigit()) or \
         (symbol_table[p[1]] == 'float' and not is_float(p[3])) or \
         (symbol_table[p[1]] == 'bool' and p[3].name not in ['true', 'false']):  # Validación para booleanos
        print(f"Error: Mismatch en la asignación a la variable '{p[1]}'.")
    p[0] = Node('assignment', children=[Node(p[1]), Node(p[2]), p[3]])

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN THEN LBRACE statements RBRACE ELSE LBRACE statements RBRACE FI
                    | IF LPAREN condition RPAREN THEN LBRACE statements RBRACE FI'''
    if len(p) == 13:
        p[0] = Node('if_statement', children=[p[3], p[7], p[11]])
    else:
        p[0] = Node('if_statement', children=[p[3], p[7]])

def p_write_statement(p):
    '''write_statement : WRITE expression SEMICOLON
                       | WRITE STRING SEMICOLON'''
    if len(p) == 4:
        p[0] = Node('write_statement', value=p[2])
    else:
        p[0] = Node('write_statement', value=p[2])  # Asigna la cadena literal como valor

def p_do_statement(p):
    '''do_statement : DO LBRACE statements RBRACE WHILE LPAREN condition RPAREN SEMICOLON'''
    if p[7] == 'empty':
        print(f"Error: Incomplete 'while' condition at line {p.lineno}.")
    p[0] = Node('do_statement', children=[p[3], p[7]])

def p_while_statement(p):
    'while_statement : WHILE LPAREN condition RPAREN LBRACE statements RBRACE'
    p[0] = Node('while_statement', children=[p[3], p[6]])

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) == 4:
        p[0] = Node('expression', children=[p[1], Node(p[2]), p[3]])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        p[0] = Node('term', children=[p[1], Node(p[2]), p[3]])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | FLOAT_NUMBER
              | IDENTIFIER
              | BOOL_VALUE'''  # Añadido BOOL_VALUE para valores true/false
    if len(p) == 4:
        p[0] = Node('factor', children=[p[2]])
    else:
        p[0] = Node('factor', children=[Node(p[1])])


def p_condition(p):
    '''condition : expression EQUALS expression
                 | expression NOTEQUALS expression
                 | expression LESS expression
                 | expression LESSEQUAL expression
                 | expression GREATER expression
                 | expression GREATEREQUAL expression
                 | expression AND expression
                 | expression OR expression'''
    # Validación opcional para tipos booleanos
    if p[2] in ['and', 'or'] and (p[1].name not in ['true', 'false'] or p[3].name not in ['true', 'false']):
        print(f"Error: Operador lógico solo permitido con booleanos en la línea {p.lineno}.")
    p[0] = Node('condition', children=[p[1], Node(p[2]), p[3]])

def p_empty(p):
    'empty :'
    p[0] = Node('empty')

def p_error(p):
    global errors
    if p:
        error_msg = f"Error: Unexpected token '{p.value}' at line {p.lineno}"
        errors.append((p.lineno, error_msg))
        print(error_msg)
        # Insertar un nodo de error para mantener el árbol en ejecución
        p.parser.errok()  # Reanudar el análisis
        p[0] = Node('error', children=[Node(f"error_token: {p.value}")])
    else:
        error_msg = "Error: Unexpected end of input"
        errors.append(('EOF', error_msg))
        print(error_msg)
        # Nodo de error para el fin inesperado
        p[0] = Node('error', children=[Node('unexpected EOF')])

def p_expression_incomplete(p):
    '''expression : expression PLUS empty
                  | expression MINUS empty'''
    print(f"Error: Incomplete expression at line {p.lineno}.")

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = Node('string', value=p[1])

parser = yacc.yacc()

# Define the GUI
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
        menubar.add_cascade(label="Editar", menu=edit_menu)
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
        self.notebook.add(self.frame_codigo_intermedio, text="Arbol sintactico")
        
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
                index = self.source_code.search(token.value, '1.0', tk.END)
                if index:
                    end_index = f"{index}+{len(token.value)}c"
                    if token.type in ['INT', 'FLOAT', 'BOOL', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FI', 'WRITE', 'AND', 'OR', 'UNTIL']:
                        self.source_code.tag_add("blue", index, end_index)
                        self.source_code.tag_config("blue", foreground="blue")
                    elif token.type in ['NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE']:
                        self.source_code.tag_add("yellow", index, end_index)
                        self.source_code.tag_config("yellow", foreground="orange")
            except tk.TclError:
                pass  # Ignorar errores de búsqueda de índices
            
    # Función de análisis sintáctico
    def perform_syntax_analysis(self):
        # Limpiar los resultados anteriores
        self.tab_sintactico.delete('1.0', tk.END)
        self.tab_errors.delete('1.0', tk.END)
        self.tab_results.delete('1.0', tk.END)
        self.clear_tree(self.tree_codigo_intermedio)  # Limpiar el árbol anterior

        # Obtener el código fuente del widget de texto
        source_code = self.source_code.get('1.0', tk.END)

        # Análisis sintáctico
        global errors
        errors = []
        result = parser.parse(source_code)  # Ejecutar el parser
    
        if errors:
            for line, error_msg in errors:
                self.tab_errors.insert(tk.END, f'Line {line}: {error_msg}\n')
            self.tab_sintactico.insert(tk.END, 'Syntax analysis completed with errors.\n')
        else:
            self.tab_sintactico.insert(tk.END, 'Syntax analysis completed without errors.\n')

        # Mostrar el árbol de sintaxis, incluso si hay errores
        if result:
            self.display_syntax_tree(result)
        else:
            self.tab_sintactico.insert(tk.END, 'Error: No se pudo generar el árbol sintáctico.\n')
            
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

if __name__ == "__main__":
    app = Application()
    app.mainloop()