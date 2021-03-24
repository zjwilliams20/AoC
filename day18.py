#########################
# day 18
#########################

import ply.lex as lex
import ply.yacc as yacc

with open('input/day18', 'r') as file:
    homework = [line.strip() for line in file.readlines()]

class Lexer:

    tokens = (
        'NUMBER',
        'PLUS','TIMES',
        'LPAREN','RPAREN',
        )

    t_PLUS    = r'\+'
    t_TIMES   = r'\*'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    # Ignored characters
    t_ignore = " \t"
 
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)

L = Lexer()
L.build()
tokens = L.tokens

# Parsing rules
precedence = (
    ('left','TIMES'),
    ('left','PLUS'),
    )

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression TIMES expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def test():
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        print(parser.parse(s))

parser = yacc.yacc()

hwSum = 0
for line in homework:
    hwSum += parser.parse(line)

print(f'final sum: {hwSum}!')
