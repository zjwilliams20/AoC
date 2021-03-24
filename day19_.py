#########################
# day 19_
#########################

# couldn't resolve shift conflicts, archiving this

import ply.lex as lex
import ply.yacc as yacc
import numpy as np

with open('input/day19', 'r') as file:
    evth = [line.strip() for line in file.readlines()]

class Lexer:

    tokens = (
        'A', 'B',
        )

    t_A = r'a'
    t_B = r'b'

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

messages = [msg for msg in evth[130:]]

L = Lexer()
L.build()
tokens = L.tokens

def test():
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        try:
            result=parser.parse(s)
            print(f"{result=}")
        except Exception as ex:
            print(f'can\'t parse: {ex}')
            continue

def writeFunc(rule):
    '''write a PLY production function, e.g. p_13 for rule 13'''
    
    # format rule
    replMap = {':':' :', '|':'\n\t|', '"a"':'A', '"b"':'B'}
    for old, new in replMap.items():
        rule = rule.replace(old, new)

    # split rule into parts
    main, subs = rule.split(':')
    if 'A' in subs or 'B' in subs:
        nRecipes = [1]
    if '|' in rule:
        front, back = subs.split('|')
        front = [int(s) for s in front.split() if s.isdigit()]
        back  = [int(s) for s in back.split() if s.isdigit()]
        nRecipes = [len(front), len(back)]
    else:
        subs = [int(s) for s in subs.split() if s.isdigit()]
        nRecipes = [len(subs)]

    # write function
    title = f'def p_{main}(t):\n'
    doc = f"\t'''{rule}'''\n"

    # if recipes are different lengths
    if len(np.unique(nRecipes)) != 1:

        # if lengths are different
        body = ''
        for i, nNums in enumerate(nRecipes):
            if i == 0:
                body += '\tif'
            else:
                body += '\telif'
            body += f' len(t) == {nNums}:\n\t\tt[0] = t[1]'
            if nNums != 1:
                for i in range(nNums-1):
                    body += f' + t[{i+2}]'
            body += '\n'

    # if recipes are the same length
    else:
        body = '\tt[0] = t[1]'
        if nRecipes[0] != 1:
            for i in range(nRecipes[0]-1):
                body += f' + t[{i+2}]'
        body += '\n\n'

    return title + doc + body

# write file
with open('monster.py', 'w') as file:
    
    # write the top rule
    top = evth.pop(44)
    file.writelines(writeFunc(top))

    # write the rest of em
    for rule in evth[:128]:
        file.writelines(writeFunc(rule))
    errorFunc = 'def p_error(t):\n' + \
                '\tprint("Syntax error at \'%s\'" % t.value)\n\n'
    file.writelines(errorFunc)

from monster import *
parser = yacc.yacc()

test()