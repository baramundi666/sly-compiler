import sly


Lexer = sly.Lexer

class MyToken(sly.lex.Token):
    def __repr__(self):
        return f"({self.lineno}): {self.type}({self.value})"

sly.lex.Token = MyToken


class Scanner(Lexer):
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT',
    }

    tokens = [
        "DOTPLUS", "DOTMINUS", "DOTTIMES", "DOTDIVIDE", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
        "EQ", "NEQ", "LE", "GE", "LT", "GT",
        "ID", "INTNUM", "FLOATNUM", "STRING", "SKIP", "COMMENT"
    ] + list(reserved.values())

    literals = { '+', '-', '*', '/',
                 '(', ')', '[', ']', '{', '}',
                 ':', '\'', ',', ';' ,
                 '='}

    # Regular expression rules for tokens
    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.\-'
    DOTTIMES = r'\.\*'
    DOTDIVIDE = r'\.\/'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'\-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'\/='

    EQ = r'=='
    NEQ = r'!='
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = 'IF'
    ID['else'] = 'ELSE'
    ID['for'] = 'FOR'
    ID['while'] = 'WHILE'
    ID['break'] = 'BREAK'
    ID['continue'] = 'CONTINUE'
    ID['return'] = 'RETURN'
    ID['eye'] = 'EYE'
    ID['zeros'] = 'ZEROS'
    ID['ones'] = 'ONES'
    ID['print'] = 'PRINT'

    FLOATNUM = r'[-+]?(?:(?:\d*\.\d+)|(?:\d+\.\d*)|(?:\d+))(?:[eE][-+]?\d+)?'
    INTNUM = r'\d+'
    STRING = r'\".*?\"|\'.*?\''

    SKIP = r'[ \t\n]+'
    COMMENT = r'\#.*'

    @_(r'[-+]?(?:(?:\d*\.\d+)|(?:\d+\.\d*)|(?:\d+))(?:[eE][-+]?\d+)?')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'\#.*')
    def COMMENT(self, t):
        pass

    @_(r'[ \t\n]+')
    def SKIP(self, t):
        self.lineno += t.value.count('\n')
        pass


    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1