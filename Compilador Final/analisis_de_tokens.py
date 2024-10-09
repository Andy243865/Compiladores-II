import re #libreia con lo necesario para la declaracion de expresiones regulares

def lex_analyzer(code):#definimos la funcion en la cual se hara el analisis
    tokens = []#array en donde se guardaran los tokens
    
    #array de tuplas con el tipo de token y su expresion regular
    patterns = [ 
        ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
        ('COMMENT_SINGLE', r'//.*'),
        ('COMMENT_MULTI', r'/\*(.|\n)*?\*/'),
        ('VACIO', r''),
        ('DESCONOCIDO',r'#|°|¬|$|&|\||¨|@|`|~|\?|\¿|\¡|\´|\\'),
        ('OPERATOR', r'\+\+|--|[+\-*/%^]'),
        ('REALNUMBER',r"[+-]?\d+\.\d+"),
        ('NO_NUMBER',r"[+-]?\d+\."),
        ('NUMBER', r'[+-]?\d+'),
        ('REL_OPERATOR',r'[<>!=][=]|[<>]'),
        ('SYMBOL', r"[\[\]\;\:\,\{\}\(\)]"),
        ('STRING',r'\"([^"]*)\"'),
        ('KEYWORD', r'\b(int|for|string|if|else|do|while|switch|case|double|main|cout|cin|break)\b'),
        ('ASIGN_OPERATOR',r'='),
        ("LOGIC_OPERATOR",r"and|or"),
        ('BLANK', r'\s'),
        ('LINE', r'\n|\n$'),
        ('DESCONOCI2', r'\.+'),
    ]
    #Esta línea de código crea una expresión regular compleja a partir de un conjunto de patrones y nombres de grupos.
    #for pair in patterns: Esto itera sobre cada par de patrones en la lista patterns.
    #'(?P<%s>%s)' % pair: Aquí se formatea cada par de patrones en una cadena con el formato (?P<nombre_grupo>patron) donde nombre_grupo
    #  es el nombre del grupo capturado y patron es el patrón de expresión regular.
    #'|'.join(...): Se unen todas estas cadenas formateadas usando el operador |, que en una expresión regular significa "o".
    #  Por ejemplo, si tienes dos patrones, esto se convertirá en patron1|patron2.
    regex = '|'.join('(?P<%s>%s)' % pair for pair in patterns)
    

    #se busca en en el codigo code las coincidencia con las expresiones regulares en regex
    for match in re.finditer(regex, code):
        #se asigna tipo y valor de token
        # por ejemplo 3.14159 seria un REALNUMBER con valro 3.1416
        token_type = match.lastgroup
        token_value = match.group()
        #se eliminan saltos de linea en los tokens
        token_value=token_value.replace('\n','')
        #si el tipo de token es un comentario, un espacio en blnaco o un caracter nulo no se guarda
        if token_type == 'COMMENT_MULTI' or token_type== 'COMMENT_SINGLE' or token_type == 'BLANK' or token_type == 'LINE' or token_type == 'VACIO':
            continue
        #si existe un token desconocido o error a este se le agrega la linea y columna donde se encontro
        if token_type=='DESCONOCIDO' or token_type=='DESCONOCI2' or token_type =='NO_NUMBER':
            start_pos = match.start()
            end_pos = match.end()
            column = start_pos - code.rfind('\n', 0, start_pos)
            line = code.count('\n', 0, start_pos) + 1

            token_value="Token desconocido: '{}' en la línea {} y columna {}".format(token_value,line, column)
        #guardamos los tokens en un nuevo array y este se retorna
        tokens.append((token_type, token_value))
            
    return tokens




codigo_c1 = """
int _i
int _j;                //Variables contadoras del ciclo.
int _lista[Nelementos]={6,9,3,1}; //Declaracion e inicializacion de un arreglo de 4 elementos.
int _temp=0;             //Variable temporal.
string _str1="the fear inside won't let me go";

for (i=1;i<Nelementos;i++)
{
       for (j=0; j < Nelementos-i ;j++) // for(j=0; j < Nelementos-i; j++) es menor y no menor igual
       {
          if (lista[j] > lista[j+1])//Condicion mayor-menor
          {
            temp=lista[j];
            lista[j]=lista[j+1];
            lista[j+1]=temp;
          }
       }
}
//Para cambiar el modo de ordenamiento solo debemos cambiar la condicion < ó >
/*maldita sea firus 
  esto no deberia funcionar
*/
flot 3.1416
"""
codigo_c=""" for (int i=0; i<n: i++){
cout<< i;
}"""

codigo_rev="""main sum@r 3.14+main)if{32.algo
34.34.34.34
{
int x,y,z;
real a,b,c;
suma=45;
x=32.32;
x=23;
y=2+3-1;
z=y+7;
y=y+1;
a=24.0+4-1/3*2+34-1;
x=(5-3)*(8/2);
y=5+3-2*4/7-9;
z=8/2+15*4;
y=14.54;
if(2>3)then
        y=a+3;
  else
      if(4>2 && )then
             b=3.2;
       else
           b=5.0;
       end;
       y=y+1;
end;
a+

+;
c--;
x=3+4;
do
   y=(y+1)*2+1;
   while(x>7){x=6+8/9*8/3;   
    cin x; 
   mas=36/7; 
   };

 until(y=


=



5);
 while(y==0){
    cin mas;
    cout x;
};
}"""
"""
tokens = lex_analyzer(codigo_rev)
for token in tokens:
    print(token)
"""