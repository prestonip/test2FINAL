####################### TOKENS #######################

DIGITS              = '0123456789'
ALPHAS              = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
INT_LIT               = 'INT_LIT'
INT_LIT_1             = 'INT_LIT_1'
INT_LIT_2             = 'INT_LIT_2'
INT_LIT_4             = 'INT_LIT_4'
INT_LIT_8             = 'INT_LIT_8'

# FLOAT_LIT           = 'FLOAT_LIT'
IDENT               = 'IDENT'

ASSIGN_OP           = '='
ADD_OP              = '*'
SUB_OP              = '-'
MULT_OP             = '+'
DIV_OP              = '/'
LEFT_PAREN          = '('
RIGHT_PAREN         = ')'
MOD_OP              = '%'
# COMMA               = ','
SEMICOLON           = ';'
LEFT_BRACK          = '{'
RIGHT_BRACK         = '}'
# DOT                 = '.'
LESS_THAN           = '<'
GREATER_THAN        = '>'
LESS_THAN_EQUAL     = '<='
GREATER_THAN_EQUAL  = '>='
EQUAL_TO            = '=='
NOT_EQUAL_TO        = '!='
# NOT                 = '!'

YOINKY              = 'YOINKY' # start of program
SPLOINKY            = 'SPLOINKY' #end of program

NOCAP               = 'NOCAP' # true boolean keyword
CAP                 = 'CAP' # false keyword
AND                 = 'AND'
OR                  = 'OR'

MAYBE               = 'MAYBE' # if keyword
ACTUALLY            = 'ACTUALLY'  # else keyword
LOOP                = 'LOOP' # loop keyword


####################### LEXER #######################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char != None:
            # integer literal conditions
            if self.curr_char.isnumeric(): 
                num_str = ""
                while self.curr_char != None and self.curr_char.isnumeric():
                    num_str += self.curr_char
                    self.advance()
                if self.curr_char == '_':
                    self.advance()
                    if self.curr_char == '1':   tokens.append('INT_LIT_1'), self.advance()
                    elif self.curr_char == '2': tokens.append('INT_LIT_2'), self.advance()
                    elif self.curr_char == '4': tokens.append('INT_LIT_4'), self.advance()
                    elif self.curr_char == '8': tokens.append('INT_LIT_8'), self.advance()
                else: tokens.append('INT_LIT')

            # identifier and keyword conditions
            elif self.curr_char.isalpha():
                str_str = ""
                while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == '_'): 
                    str_str += self.curr_char 
                    self.advance()
                if str_str == "maybe":      tokens.append('MAYBE')
                elif str_str == "actually": tokens.append('ACTUALLY')
                elif str_str == "loop":     tokens.append('LOOP')
                elif str_str == "nocap":    tokens.append('NOCAP')
                elif str_str == "cap":      tokens.append('CAP')
                elif str_str == "and":      tokens.append('AND')
                elif str_str == "or":      tokens.append('OR')
                elif str_str == "YOINKY":   tokens.append('YOINKY')
                elif str_str == "SPLOINKY": tokens.append('SPLOINKY')
                elif len(str_str) > 8 or len(str_str) < 6: return self.lexError(str_str)
                else:                       tokens.append('IDENT')


            # all other tokens conditions
            else:    
                match self.curr_char:
                    case ' ':
                        self.advance()
                    case '\t':
                        self.advance()
                    case '\n':
                        self.advance()
                    case '*':
                        tokens.append('*')
                        self.advance()
                    case '-':
                        tokens.append('-')
                        self.advance()
                    case '+':
                        tokens.append('+')
                        self.advance()
                    case '/':
                        tokens.append('/')
                        self.advance()
                    case '%':
                        tokens.append('%')
                        self.advance()
                    case '<':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append('<=')
                            self.advance()
                        else:
                            tokens.append('<')
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append('>=')
                            self.advance()
                        else:
                            tokens.append('>')

                    case '=':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append('==')
                            self.advance()
                        else:
                            tokens.append('=')
                    case '!':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append('!=')
                            self.advance()
                        else:
                            return self.lexError(self.curr_char)
                    case ';':
                        tokens.append(';')
                        self.advance()
                    case '{':
                        tokens.append('{')
                        self.advance()
                    case '}':
                        tokens.append('}')
                        self.advance()
                    case '(':
                        tokens.append('(')
                        self.advance()
                    case ')':
                        tokens.append(')')
                        self.advance()
                    case _:
                        return self.lexError(self.curr_char)
        return tokens
        
    def lexError(self, invalid_char):
        self.invalid_char = invalid_char
        return f'Illegal Character: {invalid_char}'



####################### RUNNER #######################

def run(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    return tokens