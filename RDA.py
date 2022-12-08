'''
S --> 'YOINKY' <stmt> 'SPLOINKY'
<stmt> --> <var_stmt> | <select_stmt> | <loop_stmt> | <block>
<var_stmt> --> 'id' { '=' <expr> }
<select_stmt> -->  'maybe' '(' <bool_expr> ')' <stmt> [ 'else' <stmt> ]
<loop> -->  'loop' '(' <bool_expr> ')' <stmt> 
<block> --> '{' { <stmt> } '}'


<expr> --> <term> { ('+'|'-') <term> }
<term> --> <factor> { ('*'|'/'|'%') <factor> }
<factor> --> 'id' | 'int_lit' | '(' <expr> ')'

<bool_inc> --> <bool_eval> { ('and'|'or') <bool_eval> }
<bool_eval> --> <bool_expr> { ('>'|'<'|'>='|'<='|'=='|'!=') <bool_expr>}
<bool_expr> --> <bool_term> { ('+'|'-') <bool_term> }
<bool_term> --> <bool_factor> { ('*'|'/'|'%') <bool_factor> }
<bool_factor> --> 'id' | 'int_lit' | 'bool_lit'

'''

####################### PARSER #######################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.curr_token = tokens[self.pos]
    
    def advance(self):
        self.pos += 1 
        self.curr_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        return self.curr_token

    # S --> 'YOINKY' <stmt> 'SPLOINKY'
    def start(self):
        if self.curr_token == 'YOINKY':
            self.advance()
            self.stmt()
            self.end()
        else:
            self.syntaxError('start')

    def stmt_list(self):
        while self.curr_token == 'IDENT' or self.curr_token == 'MAYBE' or self.curr_token == 'LOOP' or self.curr_token == '{':
            self.stmt()


    # <stmt> --> <var_stmt> | <select_stmt> | <loop_stmt> | <block>
    def stmt(self):
        match self.curr_token:
            case 'IDENT':   self.var_stmt()
            case 'MAYBE':   self.select_stmt()
            case 'LOOP':    self.loop_stmt()
            case '{':       self.block()
            case _:         pass

    # <var_stmt> --> 'id' { `=` <expr> }
    def var_stmt(self):
        while self.curr_token == 'IDENT':
            self.advance()
            if self.curr_token == '=': 
                self.advance()
                self.expr()
            else: pass

    # <expr> --> <term> { ('*'|'-') <term> }
    def expr(self):
        self.term()
        while self.curr_token == '*' or self.curr_token == '-':
            self.advance()
            self.term()

    # <term> --> <factor> { ('+'|'/'|'%') <factor> }
    def term(self):
        self.factor()
        while self.curr_token == '+' or self.curr_token == '/' or self.curr_token == '%':
            self.advance()
            self.factor()

    # <factor> --> 'id' | 'int_lit' | '(' <expr> ')'
    def factor(self):
        if self.curr_token == 'IDENT' or self.curr_token == 'INT_LIT' or self.curr_token == 'INT_LIT_1' or self.curr_token == 'INT_LIT_2' or self.curr_token == 'INT_LIT_4' or self.curr_token == 'INT_LIT_8':
            self.advance()
        elif self.curr_token == '(':
            self.advance()
            self.expr()
            if self.curr_token == ')':
                self.advance()
            else: 
                self.syntaxError('factor')
        else: 
            self.syntaxError('factor')

    # <select_stmt> -->  'maybe' '(' <bool_expr> ')' <stmt> [ 'else' <stmt> ]
    def select_stmt(self):
        if self.curr_token == 'MAYBE':
            self.advance()
            if self.curr_token == '(':
                self.advance()
                self.bool_inc()
                if self.curr_token == ')':
                    self.advance()
                    self.block()
                    while self.curr_token == 'ACTUALLY':
                        self.advance()
                        self.block()
                else:
                    self.syntaxError('select')
            else:
                self.syntaxError('select')
        else: 
            self.syntaxError('select')

    # <loop_stmt> --> 'loop' '(' <bool_expr> ')' <block>
    def loop_stmt(self):
        if self.curr_token == 'LOOP':
            self.advance()
            if self.curr_token == '(':
                self.advance()
                self.bool_inc()
                if self.curr_token == ')':
                    self.advance()
                    self.block()
                else:
                    self.syntaxError('loop')
            else:
                self.syntaxError('loop')
        else:
            self.syntaxError('loop')


    # <bool_inc> --> <bool_eval> { ('and'|'or') <bool_eval> }
    def bool_inc(self):
        self.bool_eval()
        while self.curr_token == 'AND' or self.curr_token == 'OR':
            self.advance()
            self.bool_eval()

    # <bool_eval> --> <bool_expr> { ('>'|'<'|'>='|'<='|'=='|'!=') <bool_expr>}
    def bool_eval(self):
        self.bool_expr()
        while self.curr_token == '>' or self.curr_token == '<' or self.curr_token == '>=' or self.curr_token == '<=' or self.curr_token == '==' or self.curr_token == '!=':
            self.advance()
            self.bool_expr()

    # <bool_expr> --> <bool_term> { ('+'|'-') <bool_term> }
    def bool_expr(self):
        self.bool_term()
        while self.curr_token == '+' or self.curr_token == '-':
            self.advance()
            self.bool_term()

    # <bool_term> --> <bool_factor> { ('*'|'/'|'%') <bool_factor> }
    def bool_term(self):
        self.bool_factor()
        while self.curr_token == '*' or self.curr_token == '/' or self.curr_token == '%':
            self.advance()
            self.bool_factor()

    # <bool_factor> --> 'id' | 'int_lit' | 'bool_lit'
    def bool_factor(self):
        if self.curr_token == 'IDENT' or self.curr_token == 'INT_LIT' or self.curr_token == 'INT_LIT_1' or self.curr_token == 'INT_LIT_2' or self.curr_token == 'INT_LIT_4' or self.curr_token == 'INT_LIT_8' or self.curr_token == 'NOCAP' or self.curr_token == 'CAP':
            self.advance()
        else:
            self.syntaxError('bool factor')

    
    # <block> --> '{' { <stmt> ';' } '}'
    def block(self):
        if self.curr_token == '{':
            self.advance()
            while self.curr_token == 'MAYBE' or self.curr_token == 'LOOP' or self.curr_token == 'IDENT' or self.curr_token == '{':
                self.stmt()
                if self.curr_token == ';':
                    self.advance()
                else:
                    self.syntaxError('stmt')
            if self.curr_token == '}':
                self.advance()
            else:
                self.syntaxError('block')
        else:
            self.syntaxError('block')    

    # end statement
    def end(self):
        if self.curr_token == 'SPLOINKY':
            print('BASED CODE')
        else:
            self.syntaxError('end') 

    def syntaxError(self, type):
        print(type + ' error')
    