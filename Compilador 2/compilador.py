import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
import ply.lex as lex
import ply.yacc as yacc

# Define the lexer
tokens = [
    'PROGRAM', 'INT', 'FLOAT', 'BOOL', 'IDENTIFIER', 'NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON', 'COMMENT', 'MULTILINE_COMMENT', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO',
    'FI', 'WRITE', 'AND', 'OR', 'EQUALS', 'NOTEQUALS', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL',
    'UNTIL'
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

# Ignored characters
t_ignore = ' \t'

# Symbol table
symbol_table = {}

def t_PROGRAM(t):
    r'program'
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

lexer = lex.lex()

# Define the parser
def p_program(p):
    'program : PROGRAM LBRACE declarations statements RBRACE'
    pass

def p_declarations(p):
    '''declarations : declarations declaration
                    | empty'''
    pass

def p_declaration(p):
    '''declaration : INT var_list SEMICOLON
                   | FLOAT var_list SEMICOLON
                   | BOOL var_list SEMICOLON'''
    pass

def p_var_list(p):
    '''var_list : var_list COMMA IDENTIFIER
                | IDENTIFIER'''
    pass

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    pass

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | write_statement
                 | do_statement
                 | while_statement'''
    pass

def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression SEMICOLON'
    if p[1] not in symbol_table:
        print(f"Error: Variable '{p[1]}' not declared.")
    elif p[1] in symbol_table and symbol_table[p[1]] == 'bool' and p[3] not in ['true', 'false']:
        print(f"Error: Cannot assign non-boolean value '{p[3]}' to boolean variable '{p[1]}'.")
    pass

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN THEN LBRACE statements RBRACE ELSE LBRACE statements RBRACE FI
                    | IF LPAREN condition RPAREN THEN LBRACE statements RBRACE FI'''
    pass

def p_write_statement(p):
    'write_statement : WRITE expression SEMICOLON'
    pass

def p_do_statement(p):
    'do_statement : DO LBRACE statements RBRACE UNTIL LPAREN condition RPAREN SEMICOLON'
    pass

def p_while_statement(p):
    'while_statement : WHILE LPAREN condition RPAREN LBRACE statements RBRACE'
    pass

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    pass

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    pass

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | FLOAT_NUMBER
              | IDENTIFIER'''
    pass

def p_condition(p):
    '''condition : expression EQUALS expression
                 | expression NOTEQUALS expression
                 | expression LESS expression
                 | expression LESSEQUAL expression
                 | expression GREATER expression
                 | expression GREATEREQUAL expression
                 | expression AND expression
                 | expression OR expression'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    global errors
    line = p.lineno if p else 'EOF'
    error_msg = f' Unexpected token: {p.value if p else "end of file"}'
    errors.append((line, error_msg))

parser = yacc.yacc()

# Define the GUI
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador R++")
        self.geometry("1000x600")
        
        # Create a menu bar
        menubar = Menu(self)
        self.config(menu=menubar)

        # Create menu items
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
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
        
        self.source_code = scrolledtext.ScrolledText(self, width=60, height=20)
        self.source_code.pack(side=tk.LEFT, padx=10, pady=10)
        self.source_code.bind("<KeyRelease>", self.on_key_release)
        
        self.token_table = ttk.Treeview(self, columns=("Type", "Value"), show="headings")
        self.token_table.heading("Type", text="Token Type")
        self.token_table.heading("Value", text="Token Value")
        self.token_table.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.error_table = ttk.Treeview(self, columns=("Line", "Error"), show="headings")
        self.error_table.heading("Line", text="Line")
        self.error_table.heading("Error", text="Error")
        self.error_table.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.run_button = tk.Button(self, text="Analizar", command=self.run_analysis)
        self.run_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Configurar colores de los tokens
        self.source_code.tag_configure("blue", foreground="blue")
        self.source_code.tag_configure("yellow", foreground="yellow")
    
    def new_file(self):
        self.source_code.delete('1.0', tk.END)
    
    def open_file(self):
        pass  # Aquí se implementaría la funcionalidad para abrir un archivo
    
    def save_file(self):
        pass  # Aquí se implementaría la funcionalidad para guardar un archivo

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
        self.token_table.delete(*self.token_table.get_children())
        self.source_code.tag_remove("blue", '1.0', tk.END)
        self.source_code.tag_remove("yellow", '1.0', tk.END)
        
        # Get the source code from the text widget
        source_code = self.source_code.get('1.0', tk.END)
        
        # Lexical analysis
        lexer.input(source_code)
        for token in lexer:
            self.token_table.insert("", "end", values=(token.type, token.value))
            
            # Pintar tokens
            start = self.source_code.index(f"{token.lineno}.{lexer.lexpos - len(token.value)}")
            end = self.source_code.index(f"{token.lineno}.{lexer.lexpos}")
            if token.type in ['INT', 'FLOAT', 'BOOL', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FI', 'WRITE', 'AND', 'OR', 'UNTIL']:
                self.source_code.tag_add("blue", start, end)
            elif token.type in ['NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE']:
                self.source_code.tag_add("yellow", start, end)
    
    def perform_syntax_analysis(self):
        # Clear previous error results
        self.error_table.delete(*self.error_table.get_children())
        
        # Get the source code from the text widget
        source_code = self.source_code.get('1.0', tk.END)
        
        # Syntax analysis
        global errors
        errors = []
        parser.parse(source_code)
        for line, error_msg in errors:
            self.error_table.insert("", "end", values=(line, error_msg))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
