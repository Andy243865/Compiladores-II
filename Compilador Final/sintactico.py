import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import ttk, scrolledtext
from anytree import Node, RenderTree
from semantico import *
import re

#diccionario Temporal para variable y posiciones

simbolos={}

# Definición de la clase Node
class No:
    def __init__(self, type, value=None, children=None, lineno_start=None, lineno_end=None):
        self.type = type
        self.value = value
        self.children = [child for child in (children if children is not None else []) if child is not None]
        self.lineno_start = lineno_start
        self.lineno_end = lineno_end

    def __repr__(self):
        return self.print_node(0)

    def print_node(self, indent=0):
        indent_str = '│   ' * indent
        branch_str = '├── ' if self.children else '└── '

        if self.type!='type':
            representation = f"{indent_str}{branch_str} type: {self.type}, value: {self.value}\n"
        else:
            representation = f"{indent_str}{branch_str} type: {self.value}\n"
        
        for child in self.children:
            representation += child.print_node(indent + 1)
        return representation

# Definición del analizador léxico
reserved = {
    'int': 'INT',
    'for': 'FOR',
    'string': 'STRINGKY',
    'if': 'IF',
    'else': 'ELSE',
    'do': 'DO',
    'while': 'WHILE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'break': 'BREAK',
    'double': 'DOUBLE',
    'main': 'MAIN',
    'cout': 'COUT',
    'cin': 'CIN',
    'and': 'AND',
    'or': 'OR'
}

tokens = [
    'ID',
    'PLUSPLUS', 'PLUS', 'MINUSMINUS', 'MINUS', 'DIVIDE', 'TIMES', 'POW', 'MODULE',
    'REALNUMBER', 'NUMBER', 'LESSTEQ', 'GREATTEQ', 'DIFF', 'EQ', 'LESST', 'GREATT',
    'LCOR', 'RCOR', 'COMMA', 'PCOMMA', 'PEPE', 'LKEY', 'RKEY', 'LPAREN', 'RPAREN',
    'STRING', 'ASSIGN', 'foo_NUMBER'
] + list(reserved.values())

t_PLUSPLUS = r'\+\+'
t_PLUS = r'\+'
t_MINUSMINUS = r'\-\-'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POW = r'\^'
t_MODULE = r'%'
t_LESSTEQ = r'<='
t_GREATTEQ = r'>='
t_DIFF = r'!='
t_EQ = r'=='
t_LESST = r'<'
t_GREATT = r'>'
t_LCOR = r'\['
t_RCOR = r'\]'
t_COMMA = r','
t_PCOMMA = r';'
t_PEPE = r':'
t_LKEY = r'{'
t_RKEY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='

t_foo_NUMBER = r'\d+'

t_ignore = ' \t'

def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    pass

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_REALNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    
    print("Alv")
    print(t)

    global simbolos
    #if t.value not in reserved:
    if t.value in simbolos:
        # Accedemos a la entrada correspondiente en la tabla de símbolos
        variable = simbolos[t.value]
        print("Lineo")
        print(t.lineno)
        print("var")
        print(variable['lineas'])
        variable['lineas'].append(t.lineno)
    else:
        if t.type == "ID":
        # Si no está en la tabla de símbolos, lo agregamos
            simbolos[t.value] = {
                'tipo': t.type,
                'valor': t.value,
                'lineas': [t.lineno]  # Usamos t.lineno
            }
    
    return t



def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")

    t.lexer.skip(1)

lexer = lex.lex()

# Definición del analizador sintáctico
def p_program(p):
    '''program : main'''
    p[0] = Node('Codigo', children=[p[1]])

def p_main(p):
    '''main : MAIN LKEY declarations RKEY'''
    p[0] = Node('Main', children=p[3].children)

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = Node('Declaraciones', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Declaraciones', children=[p[1]])

def p_declaration(p):
    '''declaration : declaration_variable
                   | statement'''
    p[0] = p[1]

def p_declaration_variable(p):
    '''declaration_variable : type variable PCOMMA'''
    p[0] = Node('Declaracion', children=[p[1], p[2]])
    #for value in p:
   
    
    
    tipo = p[1]  # El tipo de dato de la variable
    tipo_var = str(tipo).split('/')[-1].strip("')")
    p[0] = Node('Declaracion', children=[p[1], p[2]], tipo=tipo_var)
    for hijo in p[0].children:
            hijo.tipo = tipo_var
    # Suponiendo que p[2].children contiene los nombres de las variables
    for var in p[2].children:
        if var:  # Si hay un valor (nombre de la variable)
            # Llama a la función insertar_variable con el nombre de la variable
            # Valor y línea pueden ser determinados como desees
            valor = None  # Aquí puedes definir el valor inicial, si lo tienes
            
            linea = p.lexpos(2) # Línea de la declaración
        
            variable_nombre = str(var).split('/')[-1].strip("')")
            
            if variable_nombre in simbolos:
                variable = simbolos[variable_nombre]
            
        
            insertar_variable(variable['valor'], tipo_var, valor, variable['lineas'],'dec') #asi
          
    
            var.tipo = tipo_var

def p_variable(p):
    '''variable : variable COMMA ID
                | ID'''
    if len(p) == 4:
        p[0] = Node('Variables', children=list(p[1].children) + [Node(p[3])])
    else:
        p[0] = Node('Variable', children=[Node(p[1])])

def p_type(p):
    '''type : INT
            | DOUBLE
            | STRINGKY'''
    p[0] = Node(p[1])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = Node('Statements', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Statements', children=[p[1]])

def p_statement(p):
    '''statement : compound_statement
                 | assign_statement
                 | select_statement
                 | iteration_statement
                 | cin_statement
                 | cout_statement
                 | switch_statement
                 | doublefacts'''
    p[0] = p[1]

def p_compound_statement(p):
   '''compound_statement : LKEY statements RKEY'''
   p[0] = Node('Bloque', children=p[2].children)

# ASSING
def p_assign_statement(p):
    '''assign_statement : ID ASSIGN expression PCOMMA'''
    p[0] = Node('Asignacion', children=[Node(p[1]), p[3]])
   
    getVal = fn_getValor(p[1])
    #if getVal != None and getVal['valor'] != None:
    if getVal != None:
        hijos = print_children(p[3])
        print("--------------CANTIDAD DE HIJOS",hijos)
        result = evaluate_expression(p[3])
        if hijos != 0:
            if getVal["tipo"] == 'double':
                result = float(result)
            elif getVal["tipo"] == 'int':
                result = int(result)
        insertar_variable(p[1], getVal["tipo"], result, getVal["lineas"],'asi')
        print(result,"aqui", getVal)

        """if getVal["tipo"] == 'int' and re.match(r'\-?\d+\.\d+', str(result)):
            p[0] = Node('Asignacion', children=[Node(p[1],tipo=getVal['tipo'], valor="err"), p[3]],tipo=getVal['tipo'], valor="err")
        else:
            p[0] = Node('Asignacion', children=[Node(p[1],tipo=getVal['tipo'], valor=result), p[3]],tipo=getVal['tipo'], valor=result)"""
        p[0] = Node('Asignacion', children=[Node(p[1],tipo=getVal['tipo'], valor=result), p[3]],tipo=getVal['tipo'], valor=result)
        """if getVal['tipo'] == 'int':
            p[0] = Node('Asignacion', children=[Node(p[1],tipo=getVal['tipo'], valor=int(result)), p[3]],tipo=getVal['tipo'], valor=int(result))
        else:
            p[0] = Node('Asignacion', children=[Node(p[1],tipo=getVal['tipo'], valor=float(result)), p[3]],tipo=getVal['tipo'], valor=float(result))"""
        print(p[0],"firus")
        print(p[0].children, "hijosp0")
    else:
        insertar_variable(p[1], 0, 0, 0,'asi')
        # for hijo in p[0].children:
        #    hijo.tipo = getVal['tipo']



def print_children(node):
    index = 0
    if node and hasattr(node, 'children') and len(node.children) > 0:
        # Usa un índice para iterar sobre los hijos
        
        while index < len(node.children):
            print_children(node.children[index])  # Llama a la función recursivamente
            index += 1
    return index

def evaluate_expression(node):
    # Verificar si el nodo es válido
    if node is None:
        return None
    
    
    nodo = node.valor
    # Verificamos si termina con cualquiera de las dos opciones
   
    if re.match(r'\-?\d+\.\d+', nodo):
        return float(nodo)
    elif re.match(r'\-?\d+',nodo):
        return int(nodo)
    else:
        # Si el nodo es una operación
        if nodo in ['+', '-', '*', '/', '^', '%']:
            # Evaluar los hijos
            left_value = evaluate_expression(node.children[0]) if len(node.children) > 0 else 0
            right_value = evaluate_expression(node.children[1]) if len(node.children) > 1 else 0
            
            if left_value == None or right_value == None:
                return None

            # Realizar la operación
            if nodo == '+':
                return left_value + right_value
            elif nodo == '-':
                return left_value - right_value
            elif nodo == '*':
                return left_value * right_value
            elif nodo == '/':
                res = left_value / right_value if right_value != 0 else float('inf')  # Evitar división por cero
                match = re.match(r'(\d)+\.0+$', str(res))
                if match:
                    return int(match.group(1))
                else:
                    return res
            elif nodo == '%':
                return left_value % right_value
            elif nodo == '^':
                return left_value ** right_value
            
            variable = fn_getValor(nodo)
            return variable["valor"]
        else:
            getVal = fn_getValor(nodo)
            if getVal != None:
                if getVal["valor"] == "None":
                    return None
                return getVal["valor"]
        # Devolver None si no se puede evaluar
        return nodo
        #return None


def p_select_statement(p):
    '''select_statement : IF LPAREN expression RPAREN compound_statement
                        | IF LPAREN expression RPAREN compound_statement ELSE compound_statement'''
    if len(p) == 6:
        p[0] = Node('If', children=[p[3], p[5]])
    else:
        p[0] = Node('If-Else', children=[p[3], p[5], p[7]])

def p_iteration_statement(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN compound_statement
                           | DO compound_statement WHILE LPAREN expression RPAREN PCOMMA'''
    if len(p) == 6:
        p[0] = Node('While', children=[p[3], p[5]])
    else:
        p[0] = Node('Do-While', children=[p[2], p[5]])

def p_switch_statement(p):
    '''switch_statement : SWITCH LPAREN expression RPAREN LKEY case_list RKEY'''
    p[0] = Node('Switch', children=[p[3]] + list(p[6].children))

def p_case_list(p):
    '''case_list : case_list case_statement 
                 | case_statement'''
    if len(p) == 3:
        p[0] = Node('Cases', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Case', children=[p[1]])

def p_case_statement(p):
    '''case_statement : CASE facts PEPE statements BREAK PCOMMA'''
    p[0] = Node('Declaracion Case', children=[p[2]] + list(p[4].children))

def p_cin_statement(p):
    '''cin_statement : CIN ID PCOMMA'''
    p[0] = Node('CIN', children=[Node(p[2])])

def p_cout_statement(p):
    '''cout_statement : COUT expression PCOMMA'''
    p[0] = Node('COUT', children=[p[2]])


def p_expression(p):
    '''expression : simple_expression relation_operator simple_expression
                  | simple_expression'''


   
    # Si es una expresión con operador relacional
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]],valor=fn_compare_expretion(p[1].valor,p[3].valor, p[2].cop))
        print (p[1].valor,p[3].valor, p[2],"<~~~~~~~~~~~~~~~~~~~~~~~~~~~~Comparaciones")
    # Si es una simple expresión
    else:
        p[0] = p[1]

    # for hijo in p[0].children:
    #         hijo.tipo = getVal['tipo']
#funciona para evaluar expresiones
def fn_compare_expretion(val1, val2, operador):

    val1=float(val1)
    val2=float(val2)
    if operador == "<":
        return val1 < val2
    elif operador == ">":
        return val1 > val2
    elif operador == "<=":
        return val1 <= val2
    elif operador == ">=":
        return val1 >= val2
    elif operador == "==":
        return val1 == val2
    elif operador == "!=":
        return val1 != val2
    elif operador == "and":
        return bool(val1) and bool(val2)
    elif operador == "or":
        return bool(val1) or bool(val2)
    else:
        raise ValueError("Operador no válido")
    

def p_relation_operator(p):
    '''relation_operator : EQ
                         | DIFF
                         | LESST
                         | LESSTEQ
                         | GREATT
                         | GREATTEQ
                         | AND
                         | OR'''
    if p[1] == '==':
        p[0] = Node('==')
    elif p[1] == '!=':
        p[0] = Node('!=')
    elif p[1] == '<':
        p[0] = Node('<')
    elif p[1] == '<=':
        p[0] = Node('<=')
    elif p[1] == '>':
        p[0] = Node('>')
    elif p[1] == '>=':
        p[0] = Node('>=')
    elif p[1] == 'and':
        p[0] = Node('and')
    elif p[1] == 'or':
        p[0] = Node('or')
    #p[0] = Node(p[1])
    p[0].cop=p[1]

def p_simple_expression(p):
    '''simple_expression : simple_expression sum_operator term
                         | term'''
    if len(p) == 4:
        if p[2] == '+':
            val = float(p[1].valor)+float(p[3].valor)

        elif p[2] == '-':
            val = float(p[1].valor)-float(p[3].valor)
        if(is_number(p[1].valor)=='int' and is_number(p[3].valor)=="int"):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='int', valor=str(int(val)))
        elif(is_number(p[1].valor)=='float' or is_number(p[3].valor)=='float'):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='double', valor=str(val))

    else:
        p[0] = p[1]


def p_sum_operator(p):
    '''sum_operator : PLUS
                    | MINUS'''
    p[0] = str(p[1])
 
def p_term(p):
    '''term : term mult_operator factor 
            | factor'''
    if len(p) == 4:
        val=0
        if p[2] == '*':
            val = float(p[1].valor)*float(p[3].valor)
        elif p[2] == '/':
            val = float(p[1].valor)/float(p[3].valor)
            print("-------------------------------------------")
            print(p[1], p[3])
        elif p[2] == '%':
            val = float(p[1].valor)%float(p[3].valor)
        

        if(is_number(p[1].valor)=='int' and is_number(p[3].valor)=="int"):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='int', valor=str(int(val)))
        elif(is_number(p[1].valor)=='float' or is_number(p[3].valor)=='float'):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='double', valor=str(val))
    else:
        p[0] = p[1]

def is_number(valor):
    try:
        # Intentar convertir a entero
        int_valor = int(valor)
        return "int"
    except ValueError:
        try:
            # Intentar convertir a flotante
            float_valor = float(valor)
            return "float"
        except ValueError:
            return "No es un número"


def p_mult_operator(p):
    '''mult_operator : TIMES
                     | DIVIDE
                     | MODULE'''
    p[0] = str(p[1])

def p_factor(p):
    '''factor : factor pot_operator component
              | component'''
    if len(p) == 4:
        val = float(p[1].valor)**float(p[3].valor)
        # p[0] = Node(p[2], children=[p[1], p[3]], tipo='double', valor=str(val))
        if(is_number(p[1].valor)=='int' and is_number(p[3].valor)=="int"):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='int', valor=str(int(val)))
        elif(is_number(p[1].valor)=='float' or is_number(p[3].valor)=='float'):
            p[0] = Node(p[2], children=[p[1], p[3]], tipo='double', valor=str(val))
    else:
        p[0] = p[1]

def p_pot_operator(p):
    '''pot_operator : POW'''
    p[0] = str(p[1])


def p_doublefacts(p):
    '''doublefacts : ID PLUSPLUS PCOMMA
                   | ID MINUSMINUS PCOMMA'''
    if p[2] == '++':
        p[0] = Node('PlusPlus', children=[Node(p[1]), Node('+', children=[Node(p[1], tipo='N/A', valor=p[1]), Node('1', tipo='N/A', valor='1')], tipo='N/A', valor='+')])
    elif p[2] == '--':
        p[0] = Node('MinusMinus', children=[Node(p[1]), Node('-', children=[Node(p[1], tipo='N/A', valor=p[1]), Node('1', tipo='N/A', valor='1')], tipo='N/A', valor='-')])

    getVal = fn_getValor(p[1])
    val_aux = getVal['valor']
    if getVal != None and getVal['valor'] != None:
        result = evaluate_expression(p[0].children[1])
        
        insertar_variable(p[1], getVal["tipo"], result, getVal["lineas"],'asi')
        
        if p[2] == '++':
            if getVal["tipo"] ==  'int':
                p[0] = Node('PlusPlus', children=[Node(p[1], tipo=getVal["tipo"], valor=int(result)), Node('+', children=[Node(p[1], tipo=getVal["tipo"], valor=int(val_aux)), Node('1', tipo='int', valor='1')], tipo=getVal["tipo"], valor=int(result))], tipo=getVal['tipo'], valor=int(result))
                #print(p[0])
            elif getVal["tipo"] == 'double':
                p[0] = Node('PlusPlus', children=[Node(p[1], tipo=getVal["tipo"], valor=float(result)), Node('+', children=[Node(p[1], tipo=getVal["tipo"], valor=float(val_aux)), Node('1', tipo='int', valor='1')], tipo=getVal["tipo"], valor=float(result))], tipo=getVal['tipo'], valor=float(result))
                #print(p[0])
        elif p[2] == '--':
            if getVal["tipo"] ==  'int':
                p[0] = Node('MinusMinus', children=[Node(p[1], tipo=getVal["tipo"], valor=int(result)), Node('-', children=[Node(p[1], tipo=getVal["tipo"], valor=int(val_aux)), Node('1', tipo='int', valor='1')], tipo=getVal["tipo"], valor=int(result))], tipo=getVal['tipo'], valor=int(result))
                #print(p[0])
            elif getVal["tipo"] == 'double':
                p[0] = Node('MinusMinus', children=[Node(p[1], tipo=getVal["tipo"], valor=float(result)), Node('-', children=[Node(p[1], tipo=getVal["tipo"], valor=float(val_aux)), Node('1', tipo='int', valor='1')], tipo=getVal["tipo"], valor=float(result))], tipo=getVal['tipo'], valor=float(result))
                #print(p[0])

def p_component(p):
    '''component : LPAREN expression RPAREN
                 | ID
                 | facts
                 | doublefacts'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        if re.match(r'\d+\.\d+', p[1]):
            p[0] = Node(p[1],tipo='double', valor=p[1])
        elif re.match(r'\d+', p[1]):
            p[0] = Node(p[1],tipo='int', valor=p[1])
        else:
            getVal = fn_getValor(p[1])
            p[0] = Node(p[1],tipo=getVal['tipo'], valor=str(getVal['valor']))

def p_facts(p):
    '''facts : NUMBER
             | REALNUMBER
             | STRING'''
    p[0] = str(p[1])
    #p[0] = p[1]

def p_empty(p):
    'empty : '
    p[0] = Node('empty')

def p_error(p):
    if p:
        with open("errores_de_ejecucion.txt", "a", encoding="utf-8") as f:
            f.write(f"Syntax error at '{p.value}' on line {p.lineno}\n")

        parser.errok()
    else:
        print("Syntax error at EOF")

# Construir el analizador sintáctico
parser = yacc.yacc()

def sint_analyzer(codigo):
    #print("PRIMERO")
    global simbolos
    simbolos={}
    lexer.lineno = 1  # Reiniciar el contador de líneas del lexer
    result = parser.parse(codigo, lexer=lexer)
    with open("arbol_sintactico.txt", "w", encoding="utf-8") as f:
        for pre, fill, n in RenderTree(result):
            f.write("%s%s (tipo: %s, valor: %s)\n" % (pre, n.name, getattr(n, "tipo", "N/A"), getattr(n, "valor", "N/A")))
    return result

def semantic_analyzer(codigo):
    lexer.lineno = 1  # Reiniciar el contador de líneas del lexer
    result = parser.parse(codigo, lexer=lexer)
    return result

def setup_syntax_analysis(tab2, code):
    for widget in tab2.winfo_children():
        widget.destroy()
    result = sint_analyzer(code)
    parser_app = ParserApp(tab2, result)
    generate_intermediate_code(result)
    fn_reset()

def generate_intermediate_code(ast_root):
    codegen = IntermediateCodeGenerator()
    codegen.generate(ast_root)
    instructions = codegen.get_instructions()
    # Guardar las instrucciones en un archivo
    with open("codigo_intermedio.txt", "w", encoding="utf-8") as f:
        for instr in instructions:
            f.write(instr + "\n")
    # También puedes imprimirlas en la consola si lo deseas
    print("Código Intermedio Generado:")
    for instr in instructions:
        print(instr)
    return instructions

    
class ParserApp:
    def __init__(self, root, result):
        
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame)
        self.tree.column("#0", minwidth = 1150)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        sb_vertical = ttk.Scrollbar(self.frame, orient = "vertical", command = self.tree.yview)
        sb_horizontal = ttk.Scrollbar(self.frame, orient = "horizontal", command = self.tree.xview)
        self.tree.configure(yscrollcommand = sb_vertical.set, xscrollcommand = sb_horizontal.set)

        self.build_tree('', result)
        
        tablas = mostrar_tabla_simbolos()
        

    def build_tree(self, parent, node):
        if node:
            # node_repr = f'{node.name}'
            node_repr = f'{node.name} (tipo: {getattr(node, "tipo", "N/A")}, valor: {getattr(node, "valor", "N/A")})'

            node_id = self.tree.insert(parent, 'end', text=node_repr)
            # Expande el nodo inmediatamente después de insertarlo
            self.tree.item(node_id, open=True)
            for child in node.children:
                self.build_tree(node_id, child)
    

class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions = []  # Lista para almacenar las instrucciones
        self.temp_counter = 0   # Contador para variables temporales
        self.label_counter = 0  # Contador para etiquetas

    def new_temp(self):
        """Genera un nuevo nombre temporal."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        """Genera una nueva etiqueta."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate(self, node):
        """Genera código intermedio a partir del nodo del AST."""
        if node is None:
            return None
        
        # Si el nodo es un número o identificador, devuelve su valor directamente
        if hasattr(node, 'tipo') and node.tipo == 'numero':
            return node.name  # Por ejemplo, '5', '10'
        elif hasattr(node, 'tipo') and node.tipo == 'identificador':
            return node.name  # Por ejemplo, 'x', 'y'

        node_type = node.name

        if node_type == 'Asignacion':
            # Lado izquierdo: Nombre de la variable
            var_name = node.children[0].name

            # Lado derecho: Procesar la expresión
            expr_node = node.children[1]
            if hasattr(expr_node, 'name') and expr_node.name in ['+', '-', '*', '/', '%', '^']:
                # Si es una operación, procesar recursivamente
                expr_result = self.generate(expr_node)
            elif hasattr(expr_node, 'valor'):
                # Si es un valor directo
                expr_result = expr_node.valor
            else:
                # Procesar recursivamente cualquier otro tipo de nodo
                expr_result = self.generate(expr_node)

            # Generar la instrucción de asignación
            self.instructions.append(f"{var_name} = {expr_result}")
            return var_name

        elif node_type in ['+', '-', '*', '/', '%', '^']:
            # Extraer valor del hijo izquierdo
            left_node = node.children[0]
            left = left_node.valor if hasattr(left_node, 'valor') else self.generate(left_node)

             # Extraer valor del hijo derecho
            right_node = node.children[1]
            right = right_node.valor if hasattr(right_node, 'valor') else self.generate(right_node)

            # Generar un nuevo temporal y la instrucción
            temp = self.new_temp()
            self.instructions.append(f"{temp} = {left} {node_type} {right}")
            return temp


        elif hasattr(node_type, 'cop') and node_type.cop in ['==', '!=', '<', '<=', '>', '>=']:
            # Obtener los nodos hijos (operandos izquierdo y derecho)
            left_node = node.children[0]
            right_node = node.children[1]

            print(f"DEBUG: Operando izquierdo - {left_node}")  # Para depuración

            # Procesar el operando izquierdo (si es una variable, tomar su nombre)
            if hasattr(left_node, 'name'):  # Si es una variable, tomar su nombre
                left = left_node.name
            else:
                left = left_node.valor if hasattr(left_node, 'valor') else self.generate(left_node)
            
            # Procesar el operando derecho (igual que el izquierdo)
            right = right_node.valor if hasattr(right_node, 'valor') else self.generate(right_node)

            # Generar un temporal para el resultado de la comparación
            temp = self.new_temp()
            self.instructions.append(f"{temp} = {left} {node_type.cop} {right}")
            return temp





        elif node_type == 'If':
            condition = self.generate(node.children[0])
            true_label = self.new_label()
            end_label = self.new_label()
            self.instructions.append(f"IF {condition} GOTO {true_label}"+"Hola")
            self.instructions.append(f"GOTO {end_label}")
            self.instructions.append(f"{true_label}:")
            self.generate(node.children[1])  # Bloque `if`
            if len(node.children) > 2:  # Bloque `else`
                else_label = self.new_label()
                self.instructions.append(f"GOTO {else_label}")
                self.instructions.append(f"{end_label}:")
                self.instructions.append(f"{else_label}:")
                self.generate(node.children[2])
                self.instructions.append(f"{end_label}:")
            else:
                self.instructions.append(f"{end_label}:")
            return None

        elif node_type == 'If-Else':
            # Nodo de la condición
            condition_node = node.children[0]
            
            # Procesar la condición para generar un temporal con el resultado
            condition = self.generate(condition_node)  # Este debe generar el temporal para la comparación

            true_label = self.new_label()
            false_label = self.new_label()
            end_label = self.new_label()

            # Instrucciones para manejar la condición y saltos
            self.instructions.append(f"IF {condition} GOTO {true_label}")
            self.instructions.append(f"GOTO {false_label}")

            # Bloque `if`
            self.instructions.append(f"{true_label}:")
            self.generate(node.children[1])  # Procesar el bloque `if`
            self.instructions.append(f"GOTO {end_label}")

            # Bloque `else`
            self.instructions.append(f"{false_label}:")
            self.generate(node.children[2])  # Procesar el bloque `else`

            # Etiqueta de fin
            self.instructions.append(f"{end_label}:")
            return None


        elif node_type == 'While':
            start_label = self.new_label()
            condition_label = self.new_label()
            end_label = self.new_label()
            self.instructions.append(f"{start_label}:")
            condition = self.generate(node.children[0])
            self.instructions.append(f"IF NOT {condition} GOTO {end_label}")
            self.generate(node.children[1])  # Bloque `while`
            self.instructions.append(f"GOTO {start_label}")
            self.instructions.append(f"{end_label}:")
            return None

        elif node_type == 'Do-While':
            start_label = self.new_label()
            self.instructions.append(f"{start_label}:")
            self.generate(node.children[0])  # Bloque `do`
            condition = self.generate(node.children[1])
            self.instructions.append(f"IF {condition} GOTO {start_label}")
            return None

        elif node_type == 'CIN':
            var_name = node.children[0].name
            self.instructions.append(f"READ {var_name}")
            return None

        elif node_type == 'COUT':
            expr = self.generate(node.children[0])
            self.instructions.append(f"WRITE {expr}")
            return None

        elif node_type == 'Switch':
            expr = self.generate(node.children[0])
            end_label = self.new_label()
            case_labels = []
            for case in node.children[1:]:
                case_val = self.generate(case.children[0])
                case_label = self.new_label()
                self.instructions.append(f"IF {expr} == {case_val} GOTO {case_label}")
                case_labels.append(case_label)
                self.instructions.append(f"{case_label}:")
                self.generate(case.children[1])  # Bloque del `case`
            self.instructions.append(f"{end_label}:")
            return None

        elif node_type == 'PlusPlus' or node_type == 'MinusMinus':
            var_name = node.children[0].name
            operation = '+' if node_type == 'PlusPlus' else '-'
            self.instructions.append(f"{var_name} = {var_name} {operation} 1")
            return var_name

        elif node_type == 'Declaracion':
            var_type = node.children[0].name
            var_names = [child.name for child in node.children[1].children]
            for var in var_names:
                self.instructions.append(f"DECLARE {var} : {var_type}")
            return None

        elif node_type == 'Codigo' or node_type == 'Bloque' or node_type == 'Declaraciones' or node_type == 'Statements':
            for child in node.children:
                self.generate(child)
            return None

        else:
            # Para nodos no manejados específicamente
            for child in node.children:
                self.generate(child)
            return None

    def print_instructions(self):
        """Imprime las instrucciones generadas."""
        for instr in self.instructions:
            print(instr)

    def get_instructions(self):
        """Retorna las instrucciones generadas."""
        return self.instructions
