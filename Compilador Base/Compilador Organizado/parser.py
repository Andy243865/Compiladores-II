import ply.yacc as yacc
from anytree import Node
from lexer import tokens, lexer, symbol_table

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

def p_read_statement(p):
    'read_statement : READ IDENTIFIER SEMICOLON'
    var_name = p[2]
    
    p[0] = Node('read_statement', children=[Node(var_name)])


def p_declaration(p):
    '''declaration : INT var_list SEMICOLON
                   | FLOAT var_list SEMICOLON
                   | BOOL var_list SEMICOLON'''
    var_type = p[1]
    var_list = p[2].children

    for var in var_list:
        var_name = var.name

        if var_name in symbol_table:
            existing_type = symbol_table[var_name]['type']
            if existing_type != var_type:
                print(f"Error: Variable '{var_name}' declarada como '{existing_type}' y luego como '{var_type}'.")
        else:
            symbol_table[var_name] = {'type': var_type, 'value': None}   # Agregar las variables con su tipo a la tabla de símbolos

    p[0] = Node('declaration', children=[Node(p[1]), p[2]])



def p_var_list(p):
    '''var_list : var_list COMMA IDENTIFIER
                | IDENTIFIER'''
    if len(p) == 4:
        # Lista de variables (en caso de múltiples variables separadas por coma)
        p[0] = Node('var_list', children=[*p[1].children, Node(p[3])])
    else:
        # Un solo identificador
        p[0] = Node('var_list', children=[Node(p[1])])


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
                 | read_statement 
                 | do_statement
                 | while_statement'''
    p[0] = p[1]



def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression SEMICOLON'
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Error: Variable '{var_name}' no declarada.")
    else:
        var_type = symbol_table[var_name]
        variable_type = var_type['type']
        expr_type = 'float' if isinstance(p[3].value, float) else 'int'
        print(p[3])
        if variable_type  != expr_type:
            print(f"Error: Type mismatch. Expected '{var_type}', got '{expr_type}'.")
        else:
            # Asigna el valor resultante de la expresión a la variable en la tabla de símbolos
            if var_name in symbol_table:
                symbol_table[var_name]['value'] = p[3].value
    p[0] = Node('assignment', children=[Node(var_name), Node(p[2]), p[3]])



def get_expression_type(node):
    print(node)
    print(f"el nodo es ´{node.type}´" )
    if node.type == 'int':  # Para números enteros
        return 'int'
    elif node.type == 'float':  # Para números de punto flotante
        return 'float'
    elif node.name == 'IDENTIFIER':  # Para identificadores
        return symbol_table.get(node.children[0].name, 'unknown')  # Se busca en la tabla de símbolos
    elif node.name == 'expression':  # Si es una expresión, evaluamos su tipo
        left_type = get_expression_type(node.children[0])
        operator = node.children[1].name
        right_type = get_expression_type(node.children[2])
        
        # Determinamos el tipo según el operador
        if operator in ['+', '-', '*', '/']:
            if left_type == 'float' or right_type == 'float':
                return 'float'
            return 'int'
    
    return 'unknown'

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
    'write_statement : WRITE expression SEMICOLON'
    p[0] = Node('write_statement', children=[p[2]])

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
        # Realiza la operación aritmética según el operador
        if p[2] == '+':
            p[0] = Node('expression', value=p[1].value + p[3].value)
        elif p[2] == '-':
            p[0] = Node('expression', value=p[1].value - p[3].value)
    else:
        p[0] = p[1]  # Devuelve el valor del término en caso de no haber más operaciones


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        # Realiza la operación aritmética según el operador
        if p[2] == '*':
            p[0] = Node('term', value=p[1].value * p[3].value)
        elif p[2] == '/':
            p[0] = Node('term', value=p[1].value / p[3].value)
    else:
        p[0] = p[1]  # Devuelve el valor del factor si no hay más operaciones


def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | FLOAT_NUMBER
              | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[2]  # Valor de la expresión entre paréntesis
    else:
        if isinstance(p[1], int):
            p[0] = Node('factor', value=p[1])
        elif isinstance(p[1], float):
            p[0] = Node('factor', value=p[1])
        else:
            var_name = p[1]
            if var_name in symbol_table:
                p[0] = Node('factor', value=symbol_table[var_name])  # Retorna el valor de la variable desde la tabla de símbolos
            else:
                print(f"Error: Variable '{var_name}' no declarada.")


def p_condition(p):
    '''condition : expression EQUALS expression
                 | expression NOTEQUALS expression
                 | expression LESS expression
                 | expression LESSEQUAL expression
                 | expression GREATER expression
                 | expression GREATEREQUAL expression
                 | expression AND expression
                 | expression OR expression'''
    if len(p) < 4:
        print(f"Error: Incomplete condition in line {p.lineno}.")
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

    # Importar 'errors' aquí para evitar la dependencia circular
    from guis import errors
    errors.append((line, error_msg))

def p_expression_incomplete(p):
    '''expression : expression PLUS empty
                  | expression MINUS empty'''
    print(f"Error: Incomplete expression at line {p.lineno}.")

parser = yacc.yacc()
