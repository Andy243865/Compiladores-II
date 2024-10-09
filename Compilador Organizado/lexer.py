import ply.lex as lex

# Define the lexer
tokens = [
    'READ','MAIN', 'INT', 'FLOAT', 'BOOL', 'IDENTIFIER', 'NUMBER', 'FLOAT_NUMBER', 'BOOL_VALUE',
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

# Tabla para almacenar los hashes de cada variable (histórico)
hash_table = {}

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

def t_READ(t):
    r'read'
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
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# El token para los números flotantes debe estar antes que el de los números enteros
def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)  # Convertir a flotante
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convertir a entero
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