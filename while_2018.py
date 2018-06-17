import sys

cpt = 0
def next():
    global cpt
    cpt = cpt + 1
    return cpt

op2asm = { '+' : 'add', '-' : 'sub', '*' : 'imul', '/' : 'idiv'}
class ast:
    def __init__(self, type, etiquette):
        self.type = type
        self.label = etiquette
        self.sucs = []

    def __str__(self):
        return "(%s:%s) [\n %s ]" % (self.type, self.label, ", ".join([str(x) for x in self.sucs]))
    
    def var_decls(self):
        vs = set(self.vars())
        decl = ""
        for v in vs:
            if v[0] == "string":
                decl += "%s: dq \"%s\", 0\n" %(v[1], v[1])
            else:
                decl += "%s: dq 0\n" % v[1]
        return decl
    
    def var_init(self):
        code = ""
        for i in range(len(self.sucs[0].sucs)):
            code += """
mov rdx, [rsp]
mov rdi, [rdx+%s]
call atoi
mov [%s], rax
""" % ((i+1)*8,  self.sucs[0].sucs[i][0])
        return code

    def vars(self):
        if self.type == "prg":
            return [("var", x[0]) for x in self.sucs[0].sucs] + self.sucs[1].vars() + self.sucs[2].vars()
        elif self.type == "command":
            return self.sucs[0].vars() + self.sucs[1].vars()
        else:
            #self.type == expr
            if len(self.sucs) == 2:
                return self.sucs[0].vars() + self.sucs[1].vars()
            else:
                if self.type == "var":
                    return [("var", self.label)]
                elif self.type == "string":
                    return [("string", self.label)]
                else:
                    return []
             
    def gamma(self):
        if self.type in ["expr", "var", "number", "len", "id_str", "string"]:
            if self.type == "id_str":
                return """
mov rax, [%s]
add rax, %s
""" % (self.label, self.sucs[0].label)
            elif self.sucs:
                print(self.label, self.type)
                code = "%s\n push rax\n %s\n pop rbx\n %s rax, rbx\n" % \
                (self.sucs[1].gamma(),self.sucs[0].gamma(), op2asm[self.label]) 
                return code
            elif self.type == "var":
                return "mov rax, [%s]\n" % self.label
            elif self.type == "string":
                return "mov rax, %s\n" % self.label
            elif self.type == "len":
                return """
mov rbx, [%s]
xor rdx, rdx
while:
mov al, byte [rbx+rdx]
cmp al, 0
je end
add rdx, 1
jmp while
end:
mov rax, rdx
""" % (self.label)
            else:
                return "mov rax, %s\n" % self.label
        elif self.type == "command":
            if self.label == "asgnt":
                if len(self.sucs[0].sucs) > 0:
                    return """
%s
mov rbx, rax
mov rax, [%s]
add rax, %s
mov rcx, [rbx] 
mov [rax], rcx
""" %(self.sucs[1].gamma(), self.sucs[0].label, self.sucs[0].sucs[0].label)
                else:
                    if len(self.sucs[1].sucs) > 0:
                        return """
%s
mov al, byte [rax]
mov [%s], al
""" %(self.sucs[1].gamma(), self.sucs[0].label)
                    else:
                        return """
%s
mov [%s], rax
""" % (self.sucs[1].gamma(), self.sucs[0].label)
                        
                
            elif self.label == "seq":
                return "%s\n%s\n" % (self.sucs[0].gamma(), self.sucs[1].gamma())
            else:
                id = next()
                code = """
              debut%s: 
              %s
              cmp rax, 0
              je fin%s
              %s
              jmp debut%s
              fin%s:
              """ % ( id, self.sucs[0].gamma(), id, self.sucs[1].gamma(), id, id)
                return code
        elif self.type == "prg":
            return self.sucs[1].gamma()
        else:
            print("no return %s" % str(self))

import ply
from ply.lex import lex
keywords = {'if' : 'IF', 'while' : 'WHILE', 'main' : 'MAIN', 'return' : 'RETURN', 'len' : 'LEN'}
tokens = ('OPBIN','LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LCRO', 'RCRO', 'SEMICOLUMN', 'COMMA', 'EQUAL', 'ID', 'NUMBER', 'STRING') + tuple(keywords.values())
t_OPBIN = r'[\+\-\*]' #import re
t_LPAREN = r'[(]'
t_LBRACE = r'[{]'
t_LCRO = r'[[]'
t_RPAREN = r'[)]'
t_RBRACE = r'[}]'
t_RCRO = r'[]]'
t_EQUAL = r'='
t_SEMICOLUMN = r'[;]'
t_COMMA = r'[,]'
#t_ID = r'[a-zA-Z_][a-zA-Z0-9]*'
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9]*'
    t.type = keywords.get(t.value, 'ID')
    if t.type == 'ID':
        t.value = (t.value, 'var')
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = (t.value, 'number')
    return t

def t_STRING(t):
    r'"[a-zA-Z]*"'
    t.value = (t.value[1:-1], 'string')
    return t
    
t_ignore = r' '

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    print('not known %s' % t.value[0])
    t.lexer.skip(1)

lexer = lex()

w1 = "main(x,y) { while(x) { x = x - 1 ; y = y + 1 } return y;}"
w2 = '''main(x) {chaine = "abcd"; chaine[2] = "e" ; x = chaine[2] return x;}'''
w3 = '''main(x) {chaine = "abcqsdqsdqsdqdqdqd" ; x = len(chaine) return x;}'''
w4 = '''main(x) {chaine = "abcdef" ; chaine2 = "ghijkl" ; chaine[3] = chaine2[5] ; x = chaine[3] return x;}'''
w = w4

if len(sys.argv) > 1:
    file = open(sys.argv[1], 'r')
    w = file.read()
    file.close()

lexer.input(w)
for tok in lexer:
    print("%s %s %s %s" % (tok.type, tok.value, tok.lineno, tok.lexpos))


from ply.yacc import yacc

def p_program(p):
    ''' program : MAIN LPAREN variables RPAREN LBRACE command RETURN expression SEMICOLUMN RBRACE
    '''
    p[0] = ast("prg", "prg")
    p[0].sucs = [p[3], p[6], p[8]]

def p_variables(p):
    '''
    variables : ID
              | ID COMMA variables
    '''
    p[0] = ast("vars","vars")
    p[0].sucs = []
    if len(p) == 2:
        p[0].sucs.append(p[1])
    else:
        p[0].sucs.append(p[1])
        p[0].sucs = p[0].sucs + p[3].sucs

    
def p_command(p):
    '''command : lhs EQUAL expression
	       | WHILE LPAREN expression RPAREN LBRACE command RBRACE
               | command SEMICOLUMN command
    '''
    if len(p) == 4:
        if p[2] == '=':
            p[0] = ast("command", "asgnt")
            p[0].sucs = [p[1],p[3]]
        else:
            p[0] = ast("command", "seq")
            p[0].sucs = [p[1],p[3]]
    else:
        p[0] = ast("command", "while")
        p[0].sucs = [p[3], p[6]]

def p_expression(p):
    '''expression : NUMBER
                | STRING
                | lhs
                | expression OPBIN expression
                | LEN LPAREN ID RPAREN'''
    if len(p) == 2:
        if type(p[1]) == tuple:
            (value, typeOf) = p[1]
            p[0] = ast(typeOf, value)
        else:
            p[0] = p[1]
    elif len(p) == 5:
        p[0] = ast("len", p[3][0])
    else:
        p[0] = ast("expr", p[2])
        p[0].sucs = [p[1],p[3]]

def p_lhs(p):
    '''lhs : ID
          | ID LCRO NUMBER RCRO'''
    if len(p) == 2:
        (value, type) = p[1]
        p[0] = ast(type, value)
    else:
        p[0] = ast("id_str", p[1][0])
        (value, typeOf) = p[3]
        p[0].sucs = [ast(typeOf, value)]

yacc = yacc(start='program')
x = yacc.parse(input=w, lexer=lexer)
print(x)

print(set(x.vars()))

moule = open("moule.asm", "r")
code = moule.read()
moule.close()

code = code.replace("VAR_DECLS", x.var_decls())
code = code.replace("VAR_INIT", x.var_init())
code = code.replace("BODY", x.gamma())
code = code.replace("RET_EXPR", x.sucs[2].gamma())

out = open("sortie.asm", "w")
out.write(code)
out.close()

print(code)

