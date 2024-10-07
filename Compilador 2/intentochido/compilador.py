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
    'UNTIL', 'INCREMENT', 'DECREMENT', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVIDEEQUAL', 'STRING'
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
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_TIMESEQUAL = r'\*='
t_DIVIDEEQUAL = r'/='

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
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_STRING(t):
    r'\".*?\"'
    return t

lexer = lex.lex()

# Define the parser
def p_main(p):
    'main : MAIN LBRACE declarations statements RBRACE'
    p[0] = Node('main', children=[p[3], p[4]])

def p_declarations(p):
    '''declarations : declarations declaration
                    | empty'''
    if len(p) == 3:
        p[0] = Node('declarations', children=[p[1], p[2]])
    else:
        p[0] = Node('declarations')

def p_declaration(p):
    '''declaration : INT var_list SEMICOLON
                   | FLOAT var_list SEMICOLON
                   | BOOL var_list SEMICOLON'''
    for var in p[2].children:
        symbol_table[var.name] = p[1]  # Guardar el tipo de la variable
    p[0] = Node('declaration', children=[Node(p[1]), p[2]])

def p_var_list(p):
    '''var_list : var_list COMMA IDENTIFIER
                | IDENTIFIER'''
    if len(p) == 4:
        p[0] = Node('var_list', children=[p[1], Node(p[3])])
    else:
        p[0] = Node('var_list', children=[Node(p[1])])

def p_statements(p):
    '''statements : statement statements
                  | statement'''
    if len(p) == 3:
        p[0] = Node('statements', children=[p[1], p[2]])
    else:
        p[0] = Node('statement', children=[p[1]])

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | write_statement
                 | do_statement
                 | while_statement'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : IDENTIFIER EQUALS expression'''
    if p[1] not in symbol_table:
        raise SyntaxError(f"Error: Variable '{p[1]}' no declarada.")


def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN THEN LBRACE statements RBRACE ELSE LBRACE statements RBRACE FI
                    | IF LPAREN condition RPAREN THEN LBRACE statements RBRACE FI'''
    if len(p) == 13:
        p[0] = Node('if_statement', children=[p[3], p[7], p[11]])
    else:
        p[0] = Node('if_statement', children=[p[3], p[7]])

def p_write_statement(p):
    'write_statement : WRITE expression SEMICOLON'
    p[0] = Node('write_statement', children=[p[2]])

def p_do_statement(p):
    'do_statement : DO LBRACE statements RBRACE UNTIL LPAREN condition RPAREN SEMICOLON'
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
              | IDENTIFIER'''
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
    p[0] = Node('condition', children=[p[1], Node(p[2]), p[3]])

def p_empty(p):
    'empty :'
    p[0] = Node('empty')

def p_error(p):
    global errors
    if p:
        error_msg = f'Unexpected token: {p.value}'
        line = p.lineno
    else:
        error_msg = 'Unexpected end of input'
        line = 'EOF'
    errors.append((line, error_msg))

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

        format_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Formato", menu=format_menu)

        compile_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Compilar", menu=compile_menu)
        compile_menu.add_command(label="Compilar", command=self.run_analysis)

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        
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

        # Definir las pestañas del notebook
        self.tab_lexico = scrolledtext.ScrolledText(self.notebook)
        self.tab_sintactico = tk.Frame(self.notebook)  # Cambiado de ScrolledText a Frame
        self.tab_semantico = scrolledtext.ScrolledText(self.notebook)
        self.tab_codigo_intermedio = scrolledtext.ScrolledText(self.notebook)

        self.notebook.add(self.tab_lexico, text="Lexico")
        self.notebook.add(self.tab_sintactico, text="Sintactico")
        self.notebook.add(self.tab_semantico, text="Semantico")
        self.notebook.add(self.tab_codigo_intermedio, text="Codigo Intermedio")

        # Crear los widgets dentro de la pestaña "Sintactico"
        # Frame para el árbol sintáctico
        self.frame_syntax_tree = tk.Frame(self.tab_sintactico, borderwidth=2, relief=tk.GROOVE)
        self.frame_syntax_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview para el árbol sintáctico
        self.tree = ttk.Treeview(self.frame_syntax_tree, show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Opcional: Scrollbar para el Treeview
        self.tree_scroll = ttk.Scrollbar(self.frame_syntax_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side=tk.RIGHT, fill='y')

        # ScrolledText para mensajes de análisis sintáctico
        self.tab_sintactico_text = scrolledtext.ScrolledText(self.tab_sintactico, width=40)
        self.tab_sintactico_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

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
        try:
            self.source_code.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        try:
            self.source_code.edit_redo()
        except tk.TclError:
            pass
    
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
    
    def perform_syntax_analysis(self):
        # Limpiar resultados anteriores
        self.tab_sintactico_text.delete('1.0', tk.END)
        self.tab_errors.delete('1.0', tk.END)
        self.tab_results.delete('1.0', tk.END)
        self.tree.delete(*self.tree.get_children())
        
        # Obtener el código fuente
        source_code = self.source_code.get('1.0', tk.END)
        
        # Análisis sintáctico
        global errors
        errors = []
        result = parser.parse(source_code)
        
        if errors:
            for line, error_msg in errors:
                self.tab_sintactico_text.insert(tk.END, f'Line {line}: {error_msg}\n')
            self.tab_sintactico_text.insert(tk.END, 'Syntax analysis completed with errors.\n')
        else:
            self.tab_sintactico_text.insert(tk.END, 'Syntax analysis completed without errors.\n')
        
        if result:
            self.display_syntax_tree(result)
    
    def display_syntax_tree(self, tree):
        # Función auxiliar para insertar nodos en el Treeview
        def insert_node(parent, node):
            """Inserta un nodo y sus hijos de forma recursiva en el árbol sintáctico."""
            node_text = node.name if node.name else 'Unnamed Node'
            # Insertar el nodo actual en el Treeview
            node_id = self.tree.insert(parent, 'end', text=node_text)
        
            # Insertar cada hijo del nodo recursivamente
            for child in node.children:
                insert_node(node_id, child)

        # Limpiar cualquier árbol previo
        self.tree.delete(*self.tree.get_children())
    
        # Insertar el árbol sintáctico desde la raíz
        insert_node('', tree)

        # Expandir el primer nivel para que sea visible al usuario
        root_node = self.tree.get_children()
        if root_node:
            self.tree.item(root_node[0], open=True)
            self.expand_tree(root_node[0])

    def expand_tree(self, parent):
        """Expande todos los nodos en el árbol recursivamente."""
        # Expandir los hijos del nodo actual
        children = self.tree.get_children(parent)
        for child in children:
            self.tree.item(child, open=True)
            self.expand_tree(child)



if __name__ == "__main__":
    app = Application()
    app.mainloop()