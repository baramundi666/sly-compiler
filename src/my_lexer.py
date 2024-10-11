from sly import Lexer


class Scanner(Lexer):
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue ': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT',

    }

    # Set of token names.   This is always required
    tokens = ["ID", ] + list(
        reserved.values())

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIVIDE = r'\/'
    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.\-'
    DOTTIMES = r'\.\*'
    DOTDIVIDE = r'\.\/'
    ASSIGN = r'='
    PLUSEQ = r'\+='
    MINUSEQ = r'\-='
    TIMESEQ = r'\*='
    DIVIDEEQ = r'\/='
    EQ = r'=='
    NEQ = r'!='
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COLON = r':'
    TRANSPOSE = r"\'"
    COMMA = r','
    SEMICOLON = r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INT = r'\d+'
    FLOAT = r'\d+\.\d+([eE][-+]?\d+)?'
    STRING = r'\".*?\"|\'.*?\''
    SKIP = r'[ \t\n]+'
    COMMENT = r'\#.*'
    MISMATCH = r'.'

    KEYWORD = r'\b(?:if|else|for|while|break|continue|return|eye|zeros|ones|print)\b'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'








