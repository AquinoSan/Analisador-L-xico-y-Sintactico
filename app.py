import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de tokens
tokens = (
    'FOR', 'INT', 'IDENTIFIER', 'NUMBER', 'LESS_EQUAL', 'PLUS', 'PLUS_PLUS',
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON',
    'SYSTEM', 'OUT', 'PRINTLN', 'STRING', 'DOT'
)

# Reglas de expresión regular para los tokens simples
t_LESS_EQUAL = r'<='
t_PLUS = r'\+'
t_PLUS_PLUS = r'\+\+'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_DOT = r'\.'

def t_FOR(t):
    r'for'
    return t

def t_INT(t):
    r'int'
    return t

def t_SYSTEM(t):
    r'System'
    return t

def t_OUT(t):
    r'out'
    return t

def t_PRINTLN(t):
    r'println'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
    'program : for_loop'
    pass

def p_for_loop(p):
    'for_loop : FOR LPAREN INT IDENTIFIER EQUALS NUMBER SEMICOLON IDENTIFIER LESS_EQUAL NUMBER SEMICOLON increment RPAREN LBRACE statement RBRACE'
    pass

def p_increment(p):
    '''increment : IDENTIFIER PLUS_PLUS
                 | IDENTIFIER PLUS EQUALS NUMBER'''
    if len(p) == 3 and p[2] == '+':
        raise SyntaxError(f"Error en la línea {p.lineno(2)}: '{p[1]}+' no está bien definido. Use '{p[1]}++' o '{p[1]} += 1'.")

def p_statement(p):
    'statement : SYSTEM DOT OUT DOT PRINTLN LPAREN STRING PLUS IDENTIFIER RPAREN SEMICOLON'
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis en la línea {p.lineno}, token '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis al final del archivo")

parser = yacc.yacc()

def analyze_code(code):
    tokens_list = []
    lexer.lineno = 1  # Reiniciar el número de línea
    lexer.input(code)

    # Recopilar todos los tokens
    for token in lexer:
        tokens_list.append({"token": token.type, "lexema": str(token.value), "linea": token.lineno})

    syntax_error = None  # Inicializar la variable de error
    try:
        parser.parse(code, lexer=lexer)
    except SyntaxError as e:
        syntax_error = str(e)  # Captura el mensaje de error

    # Retornar la lista de tokens y el mensaje de error
    return tokens_list, syntax_error


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json['code']
    tokens, error = analyze_code(code)
    return jsonify({"tokens": tokens, "error": error})

if __name__ == '__main__':
    app.run(debug=True)
